from setuptools import setup
from importlib import import_module

def get_version():
    return import_module("vaccine-notifier.__version__").__version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    url = "https://github.com/panchal999/vaccine-notifier",
    author="Parth Panchal",
    author_email="parthnp98@gmail.com",
    long_description = long_description,
    long_description_content_type="text/markdown",
    name='vaccine-notifier',
    version=get_version(),
    description='Notify vaccination availability - Play Music/Song and Send Desktop Notifaction for vaccine availability',
    py_modules=["trigger"],
    package_dir={'': 'vaccine-notifier'},
    install_requires = [
       "requests>=2.25.1",
       "pydub>=0.3.3",
       "notify-py>=0.3.3"
    ],
    extras_require = {
        "dev":[
            "wheel>=0.34.2",
            "twine>=3.1.1",
            "pip-tools>=4.4.1"
        ],
    },
    entry_points={
        "console_scripts": [
            "vaccine-notifier=trigger:main"
        ]
    }   

)