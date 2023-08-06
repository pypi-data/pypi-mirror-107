# Python Library Imports
import click
import shutil

# 3rd party imports
from cookiecutter.main import cookiecutter

# Project Imports
from zephyr.zephyr_utils import zephyr_utils


def create_module(project_name: str) -> None:
    """
    Purpose:
        Create a zephyr module
    Args:
        project - name of the project
    Returns:
        N/A
    """
    full_dir_path = cookiecutter(
        "https://github.com/banjtheman/cookiecutter-zephyr-module",
        output_dir=f"{project_name}/modules/",
        extra_context={"project_name": project_name},
    )

    # Add module to __init__.py
    init_path = f"{project_name}/modules/__init__.py"
    module_name = full_dir_path.split("/")[-1]
    import_text = f"from . import {module_name}\n"

    zephyr_utils.append_to_file(init_path, import_text)

    # update the config json with the modules
    zephyr_config = zephyr_utils.load_json(".zephyr/config.json")
    zephyr_config["modules"].append(module_name)
    zephyr_utils.save_json(".zephyr/config.json", zephyr_config)

    # append to docker-compose.yml
    docker_compose_text = f"""\
  {module_name}:
    build: {project_name}/modules/{module_name}/.\n"""
    zephyr_utils.append_to_file("./docker-compose.yml", docker_compose_text)

    click.echo(f"Module {module_name} created")


def create_custom_module(url: str) -> None:
    """
    Purpose:
        Create a zephyr module
    Args:
        project - name of the project
    Returns:
        N/A
    """
    full_dir_path = cookiecutter(
        url,
        output_dir=f"modules/",
    )

    module_name = full_dir_path.split("/")[-1]

    # update the config json with the modules
    zephyr_config = zephyr_utils.load_json(".zephyr/config.json")
    zephyr_config["modules"].append(module_name)
    zephyr_utils.save_json(".zephyr/config.json", zephyr_config)

    click.echo(f"Custom module {module_name} created")


def delete_module(project_name: str, module_name: str) -> None:
    """
    Purpose:
        delete a zephyr module
    Args:
        project - name of the project
        module_name - name of module
    Returns:
        N/A
    """

    moudle_path = f"{project_name}/modules/{module_name}"
    shutil.rmtree(moudle_path, ignore_errors=True)

    zephyr_config = zephyr_utils.load_json(".zephyr/config.json")

    # If custom module then exit
    if "custom_project" in zephyr_config:
        return

    # Remove module to __init__.py
    init_path = f"{project_name}/modules/__init__.py"
    import_text = f"from . import {module_name}\n"

    # Get file data
    file_data = zephyr_utils.read_from_file(init_path)

    # replace project imports
    file_data = file_data.replace(import_text, f"")
    zephyr_utils.write_to_file(init_path, file_data)

    # update the config json with the modules
    zephyr_config["modules"].remove(module_name)
    zephyr_utils.save_json(".zephyr/config.json", zephyr_config)

    # remove from docker-compose.yml
    docker_compose_text = f"""\
  {module_name}:
    build: {project_name}/modules/{module_name}/.\n"""

    file_data = zephyr_utils.read_from_file("./docker-compose.yml")

    # replace docker build
    file_data = file_data.replace(docker_compose_text, f"")
    zephyr_utils.write_to_file("./docker-compose.yml", file_data)

    click.echo(f"Module {module_name} deleted")
