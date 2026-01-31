# Manages project tasks.
# Assumes pydoit is installed globally.

from pathlib import Path
from pprint import pprint
import zipfile

from doit.task import clean_targets


def task_style():
    files = []
    files.extend(Path("./").glob("*.R"))
    files.extend(Path("./").glob("*.qmd"))
    files.extend(Path("./data/").glob("*.R"))
    files = [str(f) for f in files]
    actions = [f"Rscript -e \"styler::style_file('{F}')\" " for F in files]
    return{
        "file_dep": files,
        "actions": actions,
    }


def task_review():
    # Serves the slides for the review lecture.
    target = "./last-week-tonight.html"
    action = "./last-week-tonight.qmd"

    files = []
    files.extend(Path("./data/").glob("*.csv"))
    files.extend(action)
    files = [str(f) for f in files]
    
    return{
        "file_dep": files,
        "targets": [target],
        "actions": [f"quarto preview {action}"],
        "clean": True
    }


def task_lecture():
    # Serves a rendered version of the lecture notes.
    target = "./lecture.html"
    action = "./lecture.qmd"

    files = []
    files.extend(Path("./data/").glob("*.csv"))
    files.extend(action)
    
    return{
        "file_dep": files,
        "targets": [target],
        "actions": [f"quarto preview {action}"],
        "clean": True
    }


def create_zip(target_zip, files):
    """Used by task_zip to create the zip file."""
    with zipfile.ZipFile(target_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for fs in files:
            file_path = Path(".") / fs
            archive_name = file_path.relative_to(".")
            zf.write(file_path, arcname = archive_name)


def task_zip():
    """Creates the ZIP file to give to students."""
    files = []
    files.extend(Path("./data/").glob("*"))
    files.extend(Path("./includes/").glob("*"))
    files.extend(Path(".").glob("*.R"))
    files.extend(Path(".").glob("*.Rproj"))
    files.extend(Path(".").glob("*.md"))
    files.extend(Path(".").glob("*.qmd"))
    files.remove(Path("./lab-answers-week-02.qmd"))
    files = [f.relative_to(Path(".")) for f in files]
    pprint(files)
    target = Path("week-02.zip")
    return{
        "file_dep": files,
        "targets": [target],
        "actions": [(create_zip, [], {"target_zip": target, "files": files})],
    }
