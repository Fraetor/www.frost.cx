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
from pathlib import Path
from shutil import copytree, rmtree

import marko


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default="src",
                        help="path to source folder")
    parser.add_argument("--output", type=Path, default="build",
                        help="path to output folder")
    parser.add_argument("--components", type=Path, default="components",
                        help="path to components folder")
    parser.add_argument("--templates", type=Path, default="templates",
                        help="path to templates folder")
    parser.add_argument("-c", "--clean", action="store_true",
                        help="remove preexisting files from the output directory.")
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


def rewrite_files(build_dir: Path, components: list, template_dir: Path):
    """
    Rewrites the files in the specified directory using the components.

    Args:
        build_dir: Path - The directory of files to rewrite.
        components: list[dict[str]] - List of component dictionaries.
    """
    print("\nProcessing files:")
    files = list_files(build_dir)
    markdown = marko.Markdown(extensions=['toc', 'footnote', 'codehilite'])
    for file in files:
        print(file)
        try:
            page = file.read_text("UTF-8")
        except UnicodeDecodeError:  # Skip files that aren't text.
            continue
        if file.suffix == ".md":
            components["content"] = markdown.convert(page)
            components["title"] = file.stem.replace("_", " ").title()
            page = template_dir.joinpath("basic.html").read_text("UTF-8")
            file.unlink()
            file = file.with_suffix(".html")
        for component in components:
            page = page.replace(
                f"<!-- REPLACE: {component} -->", components[component])
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


if __name__ == "__main__":
    main()
