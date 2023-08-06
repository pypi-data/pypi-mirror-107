# Python Library Imports
import os

# 3rd party imports
import nbformat as nbf
import click
from cookiecutter.main import cookiecutter

# Project Imports
from zephyr.zephyr_utils import zephyr_utils


def create_project():
    """
    Purpose:
        Create a zephyr project
    Args:
        N/A
    Returns:
        N/A
    """
    project_path = cookiecutter("https://github.com/banjtheman/cookiecutter-zephyr")
    project_name = project_path.split("/")[-1]

    create_starter_notebook(project_name)

    click.echo(f"Project {project_name} created")


def create_custom_project(url):
    """
    Purpose:
        Create a custom zephyr project
    Args:
        project - name of the project
    Returns:
        N/A
    """
    project_path = cookiecutter(url)
    project_name = project_path.split("/")[-1]

    custom_json = {
        "project_name": f"{project_name}",
        "custom_project": "True",
        "project_desc": "custom project",
        "pipelines": [],
        "modules": [],
    }

    # make custom .zephyr dir
    cmd = f"mkdir -p {project_name}/.zephyr/"
    os.system(cmd)

    # make custom pipelines dir
    cmd = f"mkdir -p {project_name}/pipelines/"
    os.system(cmd)
    
    # make custom modules dir
    cmd = f"mkdir -p {project_name}/modules/"
    os.system(cmd)

    # if file doesnt exist save
    config_path = f"{project_name}/.zephyr/config.json"
    if not os.path.exists(config_path):
        zephyr_utils.save_json(config_path, custom_json)

    click.echo(f"Custom Project {project_name} created")


def create_starter_notebook(project_name: str):
    """
    Purpose:
        Create a juptyer notebook to start
    Args:
        project - name of the project
    Returns:
        N/A
    """

    nb = nbf.v4.new_notebook()

    starter_text = f"""\
# {project_name} Sample Notebook
This is a starter notebook to facilitate experimentation
    """

    imports = f"""\
%load_ext autoreload
%autoreload 2
# common notebook imports

import json
import pandas as pd
import numpy as np
from IPython.display import display

# Project import
import {project_name}

    """

    blank_cell = f"""\
# TODO: begin my experimentation

    """

    nb["cells"] = [
        nbf.v4.new_markdown_cell(starter_text),
        nbf.v4.new_code_cell(imports),
        nbf.v4.new_code_cell(blank_cell),
    ]

    nbf.write(nb, f"{project_name}/notebooks/example_notebook.ipynb")
