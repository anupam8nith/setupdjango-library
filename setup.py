from setuptools import setup, find_packages 

setup(
    name='setupdjango',               
    version='0.1.0',                  # Initial version
    description='A tool to create ready-to-code Django projects', 
    author='Anupam Kumar', 
    author_email='anupamkumar.nith@gmail.com',  
    packages=find_packages(),             # Auto-find the 'setupdjango' package
    install_requires=[                    # Required dependencies
        'Django',
        'cookiecutter',
        'argparse' 
    ],
    entry_points={ 
        'console_scripts': [
            'setupdjango=setupdjango.__init__:main'   # Entry point for commands
        ]
    }
)
