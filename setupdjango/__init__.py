import argparse
import json
import logging
import os
import subprocess
import unittest

from cookiecutter.main import cookiecutter
from cookiecutter.exceptions import CookiecutterException

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def create_project(project_name, project_path, **kwargs):
    """
    Creates a Django project using Cookiecutter.
    :param project_name: The name of the project.
    :param project_path: The path where the project will be created.
    """
    # print("Received arguments:", project_name, project_path, kwargs)

    if not os.path.exists(project_path):
        os.makedirs(project_path)

    # Determine template path dynamically because we will generate files from here.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, "templates", "base_django_project")

    # print(template_path)
    # print(project_path)

    if not os.path.exists(template_path):
        logging.error("Template path does not exist:  %s", template_path)
        return

    try:
        print("Generating project...")
        cookiecutter(
            template_path,
            output_dir=project_path,
            no_input=False,
        )
        logging.info("Project generated successfully!")
    except CookiecutterException as e:
        logging.error("Cookiecutter error: %s", e)
    except OSError as e:
        logging.error("Error accessing the template or project path: %s", e)
    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)


def install_dependencies(project_path, requirements_file):
    """
    Installs dependencies from a requirements.txt file.
    :param project_path (str): The path to the generated Django project.
    :param requirements_file (str, optional): The path to the requirements.txt file.
                                       Defaults to 'requirements.txt' in the project path.
    """
    if requirements_file is None:
        requirements_file = os.path.join(project_path, "requirements.txt")

    try:
        print("Installing dependencies")
        subprocess.check_call(["pip", "install", "-r", requirements_file])
    except subprocess.CalledProcessError as e:
        print(f"Dependency installation failed: {e}")


def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(
        description="Setup a ready-to-code Django environment"
    )
    subparsers = parser.add_subparsers()

    # 'create' command
    create_parser = subparsers.add_parser("create-at")
    create_parser.add_argument("project_name")
    create_parser.add_argument(
        "project_path",
        nargs="?",
        default=os.getcwd(),
        help="The desired location for your project (Defaults to the current directory).",
    )
    create_parser.set_defaults(func=create_project)

    # 'install' command
    install_parser = subparsers.add_parser("install")
    install_parser.add_argument('-r', '--requirements', type=str, help="Path to requirements.txt")
    install_parser.set_defaults(func=install_dependencies)


    args = parser.parse_args()

    try:
        args.func(**vars(args))
    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    print("Creating Project Setup")
    main()
