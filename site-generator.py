#! /usr/bin/env python3

#######################################################################
#                        Static Site Generator                        #
#######################################################################

# This program inserts common components into the site files. It uses templates
# put in the source like "<!-- REPLACE: component_name -->" to tell where to put
# what. The component_name is taken from the file name, sans extension of the
# component. The components are under the components_folder and the program
# operates on the source_files folder. The program writes the outputted files
# to the build folder.

import argparse
import re
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, UTC
from pathlib import Path
from shutil import copytree, rmtree
from typing import Generator

import marko
from bs4 import BeautifulSoup


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source", type=Path, default="src", help="path to source folder"
    )
    parser.add_argument(
        "--output", type=Path, default="build", help="path to output folder"
    )
    parser.add_argument(
        "--components",
        type=Path,
        default="components",
        help="path to components folder",
    )
    parser.add_argument(
        "--templates", type=Path, default="templates", help="path to templates folder"
    )
    parser.add_argument(
        "-c",
        "--clean",
        action="store_true",
        help="remove preexisting files from the output directory.",
    )
    return parser.parse_args()


def list_files(directory: Path, include_dirs: bool = False) -> list:
    """
    Helper function to return the files in specified directory, and below.

    Args:
        directory: Path - The path of the directory under which to find files.
        include_dirs: bool = False - Whether to also include directories.

    Return:
        list[Path] - List of the files under the supplied directory.
    """
    files = []
    for file in directory.rglob("*"):
        if not include_dirs and not file.is_file():
            continue
        files.append(file)
    return files


def load_components(components_dir: Path) -> dict:
    """
    Loads the components from the components directory.

    Args:
        components_dir: Path - The directory to load the components from.

    Returns:
        dict[str] - Dict of components.
    """
    print("Loading components:")
    component_files = list_files(components_dir)
    components = {}
    for component_file in component_files:
        component_name = component_file.stem
        print(component_name)
        components[component_name] = component_file.read_text("UTF-8")
    return components


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.casefold()).strip("-")


class URL:
    url: str

    def __init__(self, url: str):
        # Basic sanity check.
        if not re.fullmatch(r"https?://.+\..+", url, flags=re.IGNORECASE):
            raise ValueError(f"URL must be a HTTP or HTTPS URL, not {url}")
        self.url = url

    def __str__(self) -> str:
        return self.url

    def join(self, path: str):
        """Join the path to the URL."""
        new_url = urllib.parse.urljoin(self.url, path)
        return self.__class__(new_url)


class BlogEntry:
    url: URL
    title: str
    date: datetime
    category: str

    def __init__(self, url: URL, title: str, category: str, date: datetime):
        if not (
            isinstance(url, URL)
            and isinstance(title, str)
            and isinstance(category, str)
            and isinstance(date, datetime)
        ):
            raise TypeError("Invalid argument types for BlogEntry.")
        self.url = url
        self.title = title
        self.category = category
        self.date = date

    def __str__(self) -> str:
        return (
            f"BlogEntry:\n\tURL: {self.url}\n\tTitle: {self.title}\n"
            f"\tDate: {self.date}\n\tCategory: {self.category})"
        )

    def atom_entry(self) -> ET.Element:
        """Return an Atom entry element for this post."""
        entry = ET.Element("entry")
        ET.SubElement(entry, "title").text = self.title
        ET.SubElement(entry, "link", {"href": str(self.url)})
        ET.SubElement(entry, "id").text = str(self.url)
        ET.SubElement(entry, "updated").text = self.date.isoformat(timespec="seconds")
        ET.SubElement(entry, "published").text = self.date.isoformat(timespec="seconds")
        ET.SubElement(
            entry, "category", {"term": slugify(self.category), "label": self.category}
        )
        ET.SubElement(
            entry, "summary", {"type": "html"}
        ).text = f'Read this post at <a href="{self.url}">{self.url}</a>'
        return entry


def get_entries(blog_index: Path) -> Generator[BlogEntry]:
    with open(blog_index, "rt") as fp:
        soup = BeautifulSoup(fp, "html.parser")
    for article in soup.find_all("article"):
        url = URL("https://www.frost.cx/").join(article.h2.a["href"])
        title = article.h2.string
        # Add timezone to date.
        date = datetime.fromisoformat(article.time["datetime"]).replace(tzinfo=UTC)
        # Hard coded for now.
        category = "Blog"
        yield BlogEntry(url, title, category, date)


def generate_feed(feed_path: str, blog_index: Path):
    # Build XML atom feed.
    feed = ET.Element("feed", {"xmlns": "http://www.w3.org/2005/Atom"})
    # Constant elements.
    ET.SubElement(feed, "id").text = "urn:uuid:1a927772-32dd-42a1-8291-3002a6c67d4b"
    ET.SubElement(feed, "title").text = "James Frost's Blog"
    ET.SubElement(
        feed, "link", {"href": "https://www.frost.cx/feed/blog.xml", "rel": "self"}
    )
    ET.SubElement(feed, "icon").text = "https://www.frost.cx/favicon.ico"
    author = ET.SubElement(feed, "author")
    ET.SubElement(author, "name").text = "James Frost"
    ET.SubElement(author, "uri").text = "https://www.frost.cx/"
    ET.SubElement(author, "email").text = "contact@frost.cx"
    ET.SubElement(feed, "rights").text = "CC BY 4.0"
    ET.SubElement(feed, "subtitle").text = (
        "James Frost's blog. This website is for me to host my projects, "
        "write some blog posts, and do anything else I decide to do with it."
    )
    ET.SubElement(
        feed, "generator", {"uri": "https://github.com/Fraetor/www.frost.cx"}
    ).text = "Slightly less horrible hand-coded feed generator"
    # Add update time.
    ET.SubElement(feed, "updated").text = datetime.now(tz=UTC).isoformat(
        timespec="seconds"
    )

    # Loop to generate and add entries.
    for entry in get_entries(blog_index):
        print("Adding entry to feed:", entry)
        feed.append(entry.atom_entry())

    # Write XML document.
    with open(feed_path, "wt", encoding="utf-8") as fp:
        # Manually write XML header to allow adding a stylesheet.
        fp.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n<?xml-stylesheet href="atom-style.xsl" type="text/xsl"?>\n'
        )
        tree = ET.ElementTree(feed)
        # Format nicely.
        ET.indent(tree)
        tree.write(fp, encoding="unicode", xml_declaration=False)


def rewrite_files(build_dir: Path, components: dict, template_dir: Path):
    """
    Rewrites the files in the specified directory using the components.

    Args:
        build_dir: Path - The directory of files to rewrite.
        components: list[dict[str]] - List of component dictionaries.
    """
    print("\nProcessing files:")
    files = list_files(build_dir)
    markdown = marko.Markdown(extensions=["toc", "footnote", "codehilite"])
    for file in files:
        print(file)
        try:
            page = file.read_text("UTF-8")
        except UnicodeDecodeError:
            # Skip files that aren't text.
            continue
        # Convert Markdown to HTML.
        if file.suffix == ".md":
            components["content"] = markdown.convert(page)
            components["title"] = file.stem.replace("_", " ").title()
            page = template_dir.joinpath("basic.html").read_text("UTF-8")
            file.unlink()
            file = file.with_suffix(".html")
        # Insert components into page.
        for component in components:
            page = page.replace(f"<!-- REPLACE: {component} -->", components[component])
        file.write_text(page, "UTF-8")


def main():
    args = parse_args()
    if args.clean:
        print("Cleaning build directory...\n")
        # Delete preexisting files in build folder.
        rmtree(args.output, ignore_errors=True)
    copytree(args.source, args.output, dirs_exist_ok=True)
    components = load_components(args.components)
    rewrite_files(args.output, components, args.templates)
    generate_feed(args.output / "feed/blog.xml", args.output / "blog.html")


if __name__ == "__main__":
    main()
