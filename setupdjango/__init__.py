import argparse
import logging
import os
import platform
import subprocess

from cookiecutter.main import cookiecutter
from cookiecutter.exceptions import CookiecutterException

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def create_project(project_name, project_path, **kwargs):
    """
    Creates a Django project setup using Cookiecutter from a GitHub repository.

    :param project_name: The name of the project.
    :param project_path: The path where the project will be created.
    """

    # Construct the correct GitHub raw template URL
    template_url = "https://github.com/anupam8nith/django_template_basic"

    try:
        if not os.path.exists(project_path):
            os.makedirs(project_path)

        print("Generating Django project setup...")
        cookiecutter(
            template_url,  # Use the raw URL
            output_dir=project_path,
            no_input=False,
        )
        logging.info("Django project setup generated successfully!")

    except CookiecutterException as e:
        logging.error("Cookiecutter error: %s", e)
    except OSError as e:
        logging.error("Error accessing the template or project path: %s", e)
    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)


def install_dependencies(project_path, requirements=None, venv=None, **kwargs):
    """Installs dependencies, finding and activating a virtual environment (with optional name).

    param: project_path (str): The root path of the project.
        requirements (str, optional): The path to the requirements file.
                                      Defaults to 'requirements.txt' in project_path.
    param: venv (str, optional): The name of the virtual environment.
                                   If not provided, the function will search for likely named directories.
    """
    if requirements is None:
        requirements = os.path.join(project_path, "requirements.txt")

    if os.path.exists(requirements):
        if venv:
            venv_path = os.path.join(project_path, venv)
            if not os.path.exists(venv_path):
                print(f"Virtual environment '{venv}' not found.")
                return  # Exit early if specified venv does not exist

        else:  # break
            print("Virtual environment name not  provided.")
            return

        # Determine OS-specific activation script
        if platform.system() == "Windows":
            activate_this = os.path.join(venv_path, "Scripts", "activate.bat")
        else:
            activate_this = os.path.join(venv_path, "bin", "activate")

        subprocess.call([activate_this, "&&", "pip", "install", "-r", requirements])

    else:
        print(f"Requirements file not found at: {requirements}")


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
    install_parser.add_argument("project_path", nargs="?", default=os.getcwd())
    install_parser.add_argument(
        "-r", "--requirements", type=str, help="Path to requirements.txt"
    )
    install_parser.add_argument(
        "-v", "--venv", type=str, help="Name of the virtual environment"
    )
    install_parser.set_defaults(func=install_dependencies)

    args = parser.parse_args()

    try:
        args.func(**vars(args))
    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    print("Creating Project Setup")
    main()
