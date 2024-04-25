import argparse
from cookiecutter.main import cookiecutter
from cookiecutter.exceptions import CookiecutterException
import json
import logging
import os
import subprocess
import unittest
import logging
import os

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def create_project(project_name, project_path, **kwargs):
    """
    Creates a Django project using Cookiecutter.
    :param project_name: The name of the project.
    :param project_path: The path where the project will be created.
    """
    print("Received arguments:", project_name, project_path, kwargs)
    
    if not os.path.exists(project_path):
        os.makedirs(project_path)

    # Determine template path dynamically because we will generate files from here.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, 'templates', 'base_django_project')
    
    print(template_path)
    print(project_path)

    if not os.path.exists(template_path):
        logging.error("Template path does not exist:  %s", template_path)
        return

    try:
        print("Generating project...")
        cookiecutter(
            template_path,
            no_input=False,
        )
        logging.info("Project generated successfully!")
    except CookiecutterException as e:  
        logging.error("Cookiecutter error: %s", e)  
    except OSError as e:  
        logging.error("Error accessing the template or project path: %s", e)
    except Exception as e: 
        logging.error("An unexpected error occurred: %s", e)


def install_dependencies(project_path):
    """
    Installs dependencies from a requirements.txt file.
    :param project_path: The path to the generated Django project.
    """
    requirements_file = os.path.join(project_path, 'requirements.txt')

    try:
        print("Installing dependencies")
        subprocess.check_call(['pip', 'install', '-r', requirements_file])
    except subprocess.CalledProcessError as e:
        print(f"Dependency installation failed: {e}")

def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="Setup a ready-to-code Django environment")
    subparsers = parser.add_subparsers()

    # 'create' command
    create_parser = subparsers.add_parser('create')
    create_parser.add_argument('project_name')
    create_parser.add_argument('project_path', nargs='?', default=os.getcwd(), help="The desired location for your project (Defaults to the current directory).")
    create_parser.set_defaults(func=create_project)

    # 'install' command
    install_parser = subparsers.add_parser('install')
    install_parser.add_argument('-r', '--requirements', type=str, help="Path to requirements.txt")
    install_parser.set_defaults(func=install_dependencies)

    args = parser.parse_args()

    try:
        args.func(**vars(args))
    except Exception as e:
        logging.error(f"An error occurred: {e}")

# class TestSetupDjango(unittest.TestCase):
#     def test(self):
#         # Test Case 1: Successful project creation
#         print("Test Case 1:")
#         # logging.info("Test Case 1: project creation started")
#         subprocess.check_call(['setupdjango', 'create', 'test_project', '/Users/anupamkumar/Documents/myProjects/'])

#         # Adjust the assertion
#         project_path = os.path.join('/Users/anupamkumar/Documents/myProjects/', 'test_project')
#         print(project_path)
#         self.assertTrue(os.path.exists(project_path))
#         self.assertTrue(os.path.isfile(os.path.join(project_path, 'manage.py')))

#         # Test Case 2: Project creation with a different path
#         print("Test Case 2:")
#         test_dir = "my_projects"
#         os.makedirs(test_dir)
#         subprocess.check_call(['setupdjango', 'create', 'another_project', test_dir])
#         self.assertTrue(os.path.exists(os.path.join(test_dir, 'another_project')))

#         # Test Case 3: Handling errors (e.g., template not found)
#         print("Test Case 3:")
#         old_template = os.environ.get('COOKIECUTTER_TEMPLATE')  # Store original setting
#         os.environ['COOKIECUTTER_TEMPLATE'] = 'nonexistent_template'  # Simulate error
#         with self.assertRaises(subprocess.CalledProcessError):  # Expect an error
#             subprocess.check_call(['setupdjango', 'create', 'error_project', '.'])
#         os.environ['COOKIECUTTER_TEMPLATE'] = old_template  # Restore setting

# if __name__ == '__main__':
#     unittest.main()
    # create_project('test_project', "/Users/anupamkumar/Documents/myProjects/")
    
if __name__ == "__main__":
    print("Creating Project Setup")
    main()