from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Add install requirements
setup(
    author="Fabio Caffarello",
    description="Data science oriented tools package",
    name="data-tools-traders-club",
    version="0.0.2",
    packages=find_packages(include=["data_tools", "data_tools.*"]),
    long_description=long_description,
    long_description_content_type='text/markdown',
    author_email="fabio.caffarello@tc.com.br",
    install_requires=[
        'pandas>=1.2',
        'SQLAlchemy>=1.4',
        'dnspython>=2.1',
        'pymongo>=3.11',
        'PyMySQL>=1.0',
        'inflection>=0.5',
        'py-make>=0.1',
        'python-dotenv>=0.17',
        'Pyment>=0.3'
    ],
    python_requires=">=3.6",
)
