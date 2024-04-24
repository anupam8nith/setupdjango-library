import argparse
from cookiecutter import generate
import os
import subprocess
import venv

def create_project(project_name, project_path, create_venv=False):  
    """
    Creates a new Django project using Cookiecutter. Provides the option for virtual environment setup.

    Args:
        project_name (str): The name of the project.
        project_path (str): The path where the project should be created.
        create_venv (bool): Whether to create a virtual environment (default: False)
    """
    cwd = os.getcwd()

    # Print the current working directory
    print(cwd)
    
    template_path = 'base_django_project'

    try:
        generate.generate_files(  # Using Cookiecutter's generator 
            repo_dir=template_path,
            output_dir=project_path
        ) 

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

    create_project(args.project_name, args.project_path, args.venv)  # Pass venv option

if __name__ == "__main__":
    main()