"""
This script is used to bootstrap the project. It will:
1. Install poetry if not installed with pip outside of a virtualenv
2. Install pre-commit if not installed
3. Run poetry init to create a pyproject.toml file
"""

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

COLORS = {
    "red": "31",
    "green": "32",
    "yellow": "33",
    "blue": "34",
    "purple": "35",
    "cyan": "36",
}


LINE_LENGTH = 80


def color_print(text, color, end="\n"):
    """Print text in color"""
    print(f"\033[{COLORS[color]}m{text}\033[0m", end=end)


def print_progress(func):
    """Print progress"""

    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args {args} and kwargs {kwargs}")
        color_print(f"🔄 {func.__doc__}", "yellow", end="\r")
        time.sleep(1)
        result = func(*args, **kwargs)
        print("\033[K", end="")
        color_print(f"✅ {func.__doc__}", "green")
        return result

    return wrapper


@print_progress
def clean_repository():
    """Removing python_template and tests folder"""
    subprocess.run(
        ["rm", "-rf", "tests", "python_template", "python-template"],
        stdout=subprocess.DEVNULL,
    )


@print_progress
def check_install(tool, installation_method):
    """Checking if tool is installed with installation_method"""
    if installation_method not in ["pip", "brew"]:
        raise ValueError("Installation method not supported")
    try:
        subprocess.check_output([tool, "--version"])
    except OSError:
        if installation_method == "pip":
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", tool],
                stdout=subprocess.DEVNULL,
            )
        elif installation_method == "brew":
            subprocess.check_call(["brew", "install", tool], stdout=subprocess.DEVNULL)


@print_progress
def get_git_root_folder_name():
    """Getting the name of the git root folder"""
    try:
        git_root = (
            subprocess.check_output(["git", "rev-parse", "--show-toplevel"])
            .decode("utf-8")
            .strip()
        )
        return Path(git_root).name

    except subprocess.CalledProcessError:
        color_print("Not in a git repository", "red")
        sys.exit(1)


@print_progress
def create_new_poetry_project():
    """Initialize a poetry project and add pytest"""
    git_root_folder_name = get_git_root_folder_name()

    if git_root_folder_name:
        subprocess.check_call(
            ["poetry", "new", git_root_folder_name], stdout=subprocess.DEVNULL
        )

    temp_folder_name = "temp"
    shutil.copytree(git_root_folder_name, temp_folder_name, dirs_exist_ok=True)
    shutil.rmtree(git_root_folder_name)
    files = os.listdir(temp_folder_name)
    for file_name in files:
        if os.path.isdir(os.path.join(temp_folder_name, file_name)):
            shutil.copytree(os.path.join(temp_folder_name, file_name), file_name)
        else:
            shutil.copy2(os.path.join(temp_folder_name, file_name), file_name)
    shutil.rmtree(temp_folder_name)

    subprocess.check_call(
        ["poetry", "add", "--group", "test", "pytest"], stdout=subprocess.DEVNULL
    )


def main():
    """Main function"""
    clean_repository()
    check_install("poetry", "pip")
    check_install("pre-commit", "brew")
    create_new_poetry_project()


if __name__ == "__main__":
    main()
