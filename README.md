# setuptemplate: Python Project Setup Made Easy

**setuptemplate** is a Python library designed to streamline the process of setting up new Python projects. It provides a simple command-line utility and supporting structure for quickly establishing a well-organized foundation for your projects.

## Key Features

* **Structure Generation:**  Creates basic project scaffolding, including essential directories  and files for Django, Flask and FastAPI.
* **Templating:** Supports customizable templates to match your project's preferences or framework-specific requirements.
* **Simplicity:** Aims to be intuitive and user-friendly. 

## Installation

1. Cloning the repository branch

```bash
git clone --single-branch --branch <branch_name> <repository_url>
```
2. Navigate to the cloned repository branch on command line and run the following command:
```
pip install -e .
```
Now we are good to go!  

## Setting up a Python framework Template

1. Navigate to the desired directory where you want to create your project on command line
2. Run the following command in your terminal:

```bash
setuptemplate at <path-of-desired-location>
```

## Example

If the setup has to be created in the current directory then we can use:

``` bash
setuptemplate at .
```
Follow the instructions provided on the command line screen and setup template will be created!

## Installing dependencies in the virtual environment using requirement.txt

1. Navigate to the root directory where the template is generated.
2. Create a virtual environment using:
```bash
python -m venv <name-of-virtualenv>
```
3. Run the following command:
```bash
setuptemplate install -v <name-of-virtualenv> -r <path-of-requiremnts.txt-file>
```

## Supported Features

1. Generation of Python webframework templates.
2. Automatically activate the virtual environment and install dependencies mentioned in requirements.txt

