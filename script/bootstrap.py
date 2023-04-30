"""
This script is used to bootstrap the project. It will:
1. Install poetry if not installed with pip outside of a virtualenv
2. Install pre-commit if not installed
3. Run poetry init to create a pyproject.toml file
"""

import os
import subprocess
import sys
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


def color_print(text, color):
    """Print text in color"""
    print(f"\033[{COLORS[color]}m{text}\033[0m")


def clean_repository():
    """Clean the repository"""
    subprocess.run(
        ["rm", "-rf", "tests", "python_template", "python-template"],
        stdout=subprocess.DEVNULL,
    )


def check_install(tool, installation_method):
    """Check if tool is installed"""
    if installation_method not in ["pip", "brew"]:
        raise ValueError("Installation method not supported")
    color_print(f"  {tool}: checking installation  ".center(LINE_LENGTH, "="), "yellow")
    try:
        subprocess.check_output([tool, "--version"])
        color_print(
            f"\u2705 {tool} is installed \u2705".center(LINE_LENGTH, " "), "green"
        )
    except OSError:
        color_print(
            f"\u26A0 {tool} is not installed. Installing {tool} ... \u26A0".center(
                LINE_LENGTH, " "
            ),
            "yellow",
        )
        if installation_method == "pip":
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", tool],
                stdout=subprocess.DEVNULL,
            )
        elif installation_method == "brew":
            subprocess.check_call(["brew", "install", tool], stdout=subprocess.DEVNULL)
        # add white checkmark
        color_print(
            f"\u2705 {tool} has been installed \u2705".center(LINE_LENGTH, " "), "green"
        )
    print()


def get_git_root_folder_name():
    try:
        git_root = (
            subprocess.check_output(["git", "rev-parse", "--show-toplevel"])
            .decode("utf-8")
            .strip()
        )
        return Path(git_root).name

    except subprocess.CalledProcessError:
        color_print(
            "Not in a git repository. Exiting ...".center(LINE_LENGTH, " "),
            "red",
        )
        sys.exit(1)


def create_new_poetry_project():
    """Initialize a poetry project"""
    color_print("  Creating a new poetry project  ".center(LINE_LENGTH, "="), "yellow")
    git_root_folder_name = get_git_root_folder_name()

    if git_root_folder_name:
        subprocess.check_call(
            ["poetry", "new", git_root_folder_name], stdout=subprocess.DEVNULL
        )
        color_print(
            "\u2705 Poetry project created \u2705".center(LINE_LENGTH, " "), "green"
        )

    color_print(
        "Copying files from template folder that do not exist".center(LINE_LENGTH, " "),
        "yellow",
    )
    for file_name in os.listdir(git_root_folder_name):
        source = os.path.join(git_root_folder_name, file_name)
        destination = os.path.join(".", file_name)
        if not os.path.exists(destination):
            subprocess.check_call(
                ["cp", "-r", source, destination], stdout=subprocess.DEVNULL
            )
            color_print(f"  {file_name} copied  ".center(LINE_LENGTH, " "), "green")
    color_print("\u2705 Files copied \u2705".center(LINE_LENGTH, " "), "green")

    color_print("Removing the template folder".center(LINE_LENGTH, " "), "yellow")
    subprocess.check_call(
        ["rm", "-rf", git_root_folder_name], stdout=subprocess.DEVNULL
    )
    color_print(
        "\u2705 Template folder removed \u2705".center(LINE_LENGTH, " "), "green"
    )

    color_print("Adding pytest to test dependencies".center(LINE_LENGTH, " "), "yellow")
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
