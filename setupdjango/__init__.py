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
        print("Generating Django project setup...")
        cookiecutter(
            template_path,
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


def install_dependencies(project_path, requirements=None):
    """Installs dependencies, automatically finding and activating a virtual environment.

    Args:
        project_path (str): The root path of the project.
        requirement_file_path (str, optional): The path to the requirements file. 
                                               Defaults to 'requirements.txt' in project_path.
    """
    if requirements is None:
        requirements = os.path.join(project_path, 'requirements.txt')

    if os.path.exists(requirements):
        possible_venv_paths = [
            os.path.join(project_path, 'venv'),
            os.path.join(project_path, '.venv'),
            os.path.join(project_path, 'env'),
            os.path.join(project_path, '.venv'),
        ]

        for venv_path in possible_venv_paths:
            if os.path.exists(venv_path):
                print("Virtual environment found ...")
                # subprocess.call(["pip", "install", "--upgrade", "pip"])
                subprocess.call([venv_path+"/Scripts/pip", "install", "-r", requirements]) 
                return 

        # Virtual environment not found, provide guidance
        print("Virtual environment not found.")
        print(f"Please create a virtual environment in your project directory with one of the following names: {', '.join(possible_venv_names)}")
        print("Instructions:")
        if platform.system() == "Windows":
            print("  1. Open a command prompt in your project directory")
            print("  2. Run (for example): python -m venv venv") 
        else:
            print("  1. Open a terminal in your project directory")
            print("  2. Run (for example): python3 -m venv venv")
        print("  3. Rerun the installation script.")

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
