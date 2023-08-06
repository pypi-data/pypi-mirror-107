# Python Library Imports
from typing import List

# 3rd party imports
import click
from cookiecutter.main import cookiecutter

# Project Imports
from zephyr.zephyr_utils import zephyr_utils


def create_module_string(module_name: str, next_step: str) -> str:
    """
    Purpose:
        Creates a moudle string
    Args:
        module_name - name of module
        next_step - next module to run
    Returns:
        module_string - code to run module string
    """
    module_string = "\n"
    module_string += f"    @step\n"
    module_string += f"    def {module_name}_step(self):\n"
    module_string += f'        """\n'
    module_string += f"        Runs module {module_name}\n"
    module_string += f'        """\n'
    module_string += f"        # TODO insert your module processes here\n"
    module_string += f'        logging.info("Starting module {module_name}")\n'
    module_string += f"        self.next(self.{next_step})\n"

    return module_string


def replace_pipeline_file(
    pipeline_file: str, modules: List[str], project_name: str, pipeline_name: str
) -> None:
    """
    Purpose:
        Replace placeholders in pipeline file
    Args:
        pipeline_file - file to replace
        modules - modules to add
        project_name - name of the project
    Returns:
        N/A
    """
    # Get file data
    file_data = zephyr_utils.read_from_file(pipeline_file)

    # replace project imports
    file_data = file_data.replace("REPLACE_PROJECT_IMPORT", f"import {project_name}")

    # replace flow name
    file_data = file_data.replace(
        "REPLACE_PIPELINE_NAME", f"{pipeline_name.capitalize()}"
    )

    # replace start next
    file_data = file_data.replace(
        "REPLACE_START_STEP", f"self.next(self.{modules[0]}_step)"
    )

    modules_length = len(modules)
    module_replace_string = ""
    # For each module generate the code
    for index, module in enumerate(modules):

        if index + 1 == modules_length:
            next_step = "end"
        else:
            next_step = f"{modules[index + 1]}_step"

        module_string = create_module_string(module, next_step)
        module_replace_string += module_string

    # replace module holder
    file_data = file_data.replace("REPLACE_MODULES", module_replace_string)

    # Replace file with new code
    zephyr_utils.write_to_file(pipeline_file, file_data)


def create_pipeline(project_name: str) -> None:
    """
    Purpose:
        Create a zephyr pipeline
    Args:
        project - name of the project
    Returns:
        N/A
    """
    # Load zephyr config
    zephyr_config = zephyr_utils.load_json(".zephyr/config.json")
    zephyr_moudles = zephyr_config["modules"]

    click.echo(f"Current modules: {zephyr_moudles}")
    moudle_list = click.prompt("Enter comma sepearted modules for pipeline", type=str)
    modules = moudle_list.split(",")

    # check if valid modules
    for module in modules:
        if module not in zephyr_moudles:
            click.echo(f"Invalid module : {module}")
            return

    click.confirm(
        f"Do you want to continue? with these modules: {modules}",
        abort=True,
        default=True,
    )

    full_dir_path = cookiecutter(
        "https://github.com/banjtheman/cookiecutter-zephyr-pipeline",
        output_dir=f"pipelines/",
    )

    pipeline_name = full_dir_path.split("/")[-1]
    pipeline_full_name = f"{full_dir_path}/{pipeline_name}_pipeline.py"

    replace_pipeline_file(pipeline_full_name, modules, project_name, pipeline_name)

    # update the config json with the pipeline
    zephyr_config["pipelines"].append(pipeline_name)
    zephyr_utils.save_json(".zephyr/config.json", zephyr_config)

    click.echo("Pipeline created")
    click.echo(f"Test with...")
    click.echo(f"python {pipeline_full_name} run")
