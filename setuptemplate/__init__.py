import argparse
import logging
import os
from pathlib import Path
import platform
import subprocess
import tempfile

import git

from cookiecutter.main import cookiecutter
from cookiecutter.exceptions import CookiecutterException

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def create_project(project_path: str, framework: str) -> None:
    """
    Creates a project setup using Cookiecutter from a GitHub repository.

    :param project_path (str): The path where the project will be created.
    :param framework (str): The selected branch that consists the framework template.
    """
    
    template_url = "git@bitbucket.org:q3info/q3_architecture.git" #repo url containing templates in branches
    try:
        if not os.path.exists(project_path):
            os.makedirs(project_path)

        print("Generating project setup...")
        cookiecutter(template_url, checkout=framework, output_dir=project_path, no_input=False)
        logging.info(f"{framework} project setup generated successfully!")

    except CookiecutterException as e:
        logging.error("Cookiecutter error: %s", e)
    except OSError as e:
        logging.error("Error accessing the template or project path: %s", e)
    except Exception as e:
        logging.error("Error: %s", e)


def install_dependencies(project_path: str, requirements: str = None, venv: str = None) -> None:
    """Installs dependencies, finding and activating a virtual environment (with optional name).

    :param project_path (str): The root path of the project.
    :param requirements (str, optional): The path to the requirements file.
                                      Defaults to 'requirements.txt' in project_path.
        venv (str, optional): The name of the virtual environment.
    """
    project_path = Path(project_path)
    if requirements is None:
        requirements_file = project_path / "requirements.txt" 
    else:
        requirements_file = Path(requirements)

    if venv:
        venv_path = project_path / venv
        if not venv_path.exists():
            logging.error(f"Virtual environment '{venv}' not found.")
            return

    # OS-specific activation script
    if platform.system() == "Windows":
        activate_this = os.path.join(venv_path, "Scripts", "activate.bat")
    else:
        activate_this = os.path.join(venv_path, "bin", "activate")

    subprocess.call([activate_this, "&&", "pip", "install", "-r", requirements_file])

def get_filtered_branches(repo_link):
    with tempfile.TemporaryDirectory() as temp_repo_dir:
        try:
            repo = git.Repo.clone_from(repo_link, temp_repo_dir)
            filtered_branches = []

            for branch in (b.name.split('/')[-1] for b in repo.refs):
                if "template_3." in branch:
                    filtered_branches.append(branch)
            return filtered_branches

        except git.GitCommandError as e:
            print("Error:", e)
            return None 
        
def get_framework_choice(framework_names):
    """Displays available frameworks and manages user selection."""
    n = len(framework_names)
    for i in range(n):
        print(f"{i+1}: {framework_names[i]}")

    while True:
        try:
            choice = int(input(f"Enter your choice (1-{n}): "))
            if 1 <= choice <= n:
                return framework_names[choice - 1]
            else:
                print(f"Invalid choice. Please select between 1 and {n}.\n")
        except ValueError:
            print("Invalid input. Please enter a number.\n")
            

def handle_command(args):
    """Dispatches actions based on the parsed arguments."""
    repo_link = "git@bitbucket.org:q3info/q3_architecture.git"
    framework_names = get_filtered_branches(repo_link)

    if args.subcommand == "at":
        if args.project_path:
            selected_framework = get_framework_choice(framework_names)
            args.func(args.project_path, selected_framework)
        else:
            args.func(**vars(args))
    elif args.subcommand == "install":
        install_dependencies(project_path=args.project_path, requirements=args.requirements, venv=args.venv)
    else:  
        args.func(**vars(args))


def main():
    parser = argparse.ArgumentParser(description="Setup a ready-to-code project environment")
    subparsers = parser.add_subparsers(help="Project setup actions", dest="subcommand")

    # 'create' command
    create_parser = subparsers.add_parser("at")
    create_parser.add_argument("project_path", help="The desired location for your project.")
    create_parser.set_defaults(func=create_project)

    # 'install' command
    install_parser = subparsers.add_parser("install")
    install_parser.add_argument(
        "project_path",
        nargs="?",
        default=os.getcwd(),
        help="Project root directory (defaults to current directory)",
    )
    install_parser.add_argument("-r", "--requirements", type=str, help="Path to requirements.txt")
    install_parser.add_argument("-v", "--venv", type=str, help="Name of the virtual environment")
    install_parser.set_defaults(func=install_dependencies)

    args = parser.parse_args()
    handle_command(args)


if __name__ == "__main__":
    main()