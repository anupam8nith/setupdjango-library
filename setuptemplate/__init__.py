import argparse
import logging
import os
from pathlib import Path
import platform
import subprocess

from cookiecutter.main import cookiecutter
from cookiecutter.exceptions import CookiecutterException

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def create_project(project_path, framework):
    """
    Creates a project setup using Cookiecutter from a GitHub repository.

    :param project_path (str): The path where the project will be created.
    :param framework (str): The selected backend framework ("Django", "Flask", or "FastAPI").
    """
    
    template_url = "https://github.com/anupam8nith/templates.git" #repo url containing templates in branches
    checkout = None

    framework_mapping = {
        "Django": "django_template",
        "Flask": "flask_template",
        "FastAPI": "fastapi_template",
    }

    if framework not in framework_mapping:
        logging.error("Invalid framework choice.")
        return

    checkout = framework_mapping[framework]

    try:
        if not os.path.exists(project_path):
            os.makedirs(project_path)

        print("Generating project setup...")
        cookiecutter(template_url, checkout, output_dir=project_path, no_input=False)
        logging.info(f"{framework} project setup generated successfully!")

    except CookiecutterException as e:
        logging.error("Cookiecutter error: %s", e)
    except OSError as e:
        logging.error("Error accessing the template or project path: %s", e)
    except Exception as e:
        logging.error("Error: %s", e)


def install_dependencies(project_path, requirements=None, venv=None):
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

    if not requirements_file.exists():
        logging.error(f"Requirements file not found at: {requirements_file}")
        return

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


def main():
    parser = argparse.ArgumentParser(
        description="Setup a ready-to-code project environment"
    )
    subparsers = parser.add_subparsers(help="Project setup actions", dest="subcommand")

    # 'create' command
    create_parser = subparsers.add_parser("at")
    create_parser.add_argument(
        "project_path", help="The desired location for your project."
    )
    create_parser.set_defaults(func=create_project)

    # 'install' command
    install_parser = subparsers.add_parser("install")
    install_parser.add_argument(
        "project_path",
        nargs="?",
        default=os.getcwd(),
        help="Project root directory (defaults to current directory)",
    )
    install_parser.add_argument(
        "-r", "--requirements", type=str, help="Path to requirements.txt"
    )
    install_parser.add_argument(
        "-v", "--venv", type=str, help="Name of the virtual environment"
    )
    install_parser.set_defaults(func=install_dependencies)

    args = parser.parse_args()

    if args.subcommand == "at":
        if args.project_path:  # Path given directly
            print("\nSelect your framework:")
            print("1. Django")
            print("2. Flask")
            print("3. FastAPI\n")

            while True:
                try:
                    choice = int(input("Enter your choice (1-3): \n"))
                    if 1 <= choice <= 3:
                        break
                    else:
                        print("Invalid choice. Please select between 1 and 3.\n")
                except ValueError:
                    print("Invalid input. Please enter a number.\n")

            framework_mapping = {1: "Django", 2: "Flask", 3: "FastAPI"}
            selected_framework = framework_mapping[choice]
            args.func(args.project_path, selected_framework)
        else:
            args.func(**vars(args))  # No path, use interactive selection
    else:
        # Handle other commands (if any)
        args.func(**vars(args))


if __name__ == "__main__":
    main()