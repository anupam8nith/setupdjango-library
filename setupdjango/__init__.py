import argparse
from cookiecutter import generate
from cookiecutter.cli import main
import json
import os
import subprocess
import venv
import shutil
import tempfile  # For creating a temporary directory

def create_project(project_name, project_path, create_venv=False):
    """
    Creates a new Django project using Cookiecutter. Provides the option for virtual environment setup.

    Args:
        project_name (str): The name of the project.
        project_path (str): The path where the project should be created.
        create_venv (bool): Whether to create a virtual environment (default: False)
    """
    os.makedirs(project_path, exist_ok=True)
    
    #create a temporary file cookiecutter.json  and provide value of project_name by the user in cookiecutter.json and copy inside the project

    # Assuming template is within 'setupdjango'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, 'templates', 'base_django_project')

    try:
        # Generate into a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            generate.generate_files(
                repo_dir=template_path,
                context={'cookiecutter.project_name': project_name},  # Pass context 
                output_dir=project_path,
                overwrite_if_exists=True 
            )
 

            # Copy the generated project to the target location
            shutil.copytree(temp_dir, project_path)

        if create_venv: 
            create_venv(project_path, '.venv')  
        
        install_dependencies(project_path)  

    except Exception as e:
        print(f"An error occurred: {e}")


def create_venv(project_path, virtual_env_name):
    """
    Creates a virtual environment and activates it.

    param: project_path (str): The path to the Django project.
    param: virtual_env_name (str): The name of the virtual environment.
    """
    env_path = os.path.join(project_path, virtual_env_name)
    venv.create(env_path, with_pip=True)  # Create the virtual environment

    # Activation scripts differ across operating systems
    if os.name == 'nt':  # Windows
        activate_script = os.path.join(env_path, 'Scripts', 'activate.bat')
    else:  # Linux/macOS
        activate_script = os.path.join(env_path, 'bin', 'activate')

    try:
        subprocess.check_call(['source', activate_script])
    except subprocess.CalledProcessError as e:
        print(f"Virtual environment activation failed: {e}")



def install_dependencies(project_path):
    """
    Installs dependencies from a requirements.txt file.

    param: project_path (str): The path to the generated Django project.
    """
    requirements_file = project_path + '/requirements.txt' 

    try:
        subprocess.check_call(['pip', 'install', '-r', requirements_file])
    except subprocess.CalledProcessError as e:
        print(f"Dependency installation failed: {e}")


def main():
    parser = argparse.ArgumentParser(description="Create a ready-to-code Django project setup.")
    parser.add_argument("project_name", help="The name of your Django project.")
    parser.add_argument("project_path", default=os.getcwd(), help="The desired location for your project.")
    parser.add_argument("--venv", action="store_true", help="Create and activate a virtual environment.")

    args = parser.parse_args()
    print("Starting to create....")
    create_project(args.project_name, args.project_path, args.venv)  # Pass venv option

if __name__ == "__main__":
    print("Calling Main")
    main()
    