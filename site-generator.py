#######################################################################
#                        Static Site Generator                        #
#######################################################################

# This program inserts common components into the site files. It uses
# templates put in the source like "<!-- REPLACE: component_name -->"
# to tell where to put what. The component_name is taken from the file
# name, sans extension of the component. The components are under the
# components_folder and the program operates on the www_files folder.
# The program overwrites in place, so it should only be run on a copy
# of the source files, such as during a CI action.

component_folder = "components"
www_files = "docs"




# TODO: Implement command line configuration of paths.
# from sys import argv

from pathlib import Path


def list_files(root: Path, include_dirs: bool = False):
    """
    root: Path - The path of the root under which to find files.
    include_dirs: bool = False - Whether to also include directories.

    Returns a list of the files under the supplied root.
    """
    files = []
    for p in root.rglob("*"):
        if not include_dirs and not p.is_file():
            continue
        files.append(p)
    return files


print("Loading components:\n")
components = list_files(Path(component_folder), False)
component_text = []
component_name = []

for component in components:
    component_name.append(component.stem)
    print(component.stem)
    with open(component, "rt", encoding="utf-8") as f:
        component_text.append(f.read())


print("\nProcessing files:\n")
files = list_files(Path(www_files), False)
for file in files:
    with open(file, "r+t", encoding="utf-8") as f:
        print(file)
        try:
            page = f.read()
        except UnicodeDecodeError:
            continue

        for i in range(len(component_name)):
            page = page.replace(
                f"<!-- REPLACE: {component_name[i]} -->", component_text[i])

        f.write(page)

