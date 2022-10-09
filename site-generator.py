#######################################################################
#                        Static Site Generator                        #
#######################################################################

# This program inserts common components into the site files. It uses templates
# put in the source like "<!-- REPLACE: component_name -->" to tell where to put
# what. The component_name is taken from the file name, sans extension of the
# component. The components are under the components_folder and the program
# operates on the source_files folder. The program writes the outputted files
# todd the build folder.

from pathlib import Path
from shutil import copytree, rmtree
from sys import argv


def _list_files(directory: Path, include_dirs: bool = False) -> list[Path]:
    """
    Helper function to return the files in specified directory.

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


def clean_build_dir(build_dir: Path):
    """
    Removes any preexisting files from the build directory.

    Args:
        build_dir: Path - The directory to clean
    """
    if "-c" or "--clean" in argv:
        # Delete preexisting files in build folder.
        rmtree(build_dir, ignore_errors=True)


def copy_to_build_dir(source_dir: Path, build_dir: Path):
    """
    Copies files from source to build directory.

    Args:
        source_dir: Path - The directory to copy from.
        build_dir: Path - The directory to copy to.
    """
    copytree(source_dir, build_dir, dirs_exist_ok=True)


def load_components(components_dir: Path) -> list[dict[str]]:
    """
    Loads the components from the components directory.

    Args:
        components_dir: Path - The directory to load the components from.

    Returns:
        list[dict[str]] - List of components. Keys are "name" and "text".
    """
    print("Loading components:")
    component_files = _list_files(components_dir)
    components = []
    for component_file in component_files:
        component_name = component_file.stem
        print(component_name)
        with open(component_file, "rt", encoding="UTF-8") as f:
            component_text = f.read()
        components.append({"name": component_name, "text": component_text})
    return components


def rewrite_files(build_dir: Path, components: list[dict[str]]):
    """
    Rewrites the files in the specified directory using the components.

    Args:
        build_dir: Path - The directory of files to rewrite.
        components: list[dict[str]] - List of component dictionaries.
    """
    print("\nProcessing files:")
    files = _list_files(build_dir)
    for file in files:
        with open(file, "rt", encoding="UTF-8") as f:
            print(file)
            try:
                page = f.read()
            except UnicodeDecodeError:  # Skip files that aren't text.
                continue
            for component in components:
                page = page.replace(
                    f"<!-- REPLACE: {component['name']} -->", component['text'])
        with open(file, "wt", encoding="UTF-8") as f:
            f.write(page)


def main():
    # TODO: Implement command line configuration of paths.
    component_folder = Path("components")
    source_folder = Path("src")
    output_folder = Path("build")

    clean_build_dir(output_folder)
    copy_to_build_dir(source_folder, output_folder)
    components = load_components(component_folder)
    rewrite_files(output_folder, components)


if __name__ == "__main__":
    main()
