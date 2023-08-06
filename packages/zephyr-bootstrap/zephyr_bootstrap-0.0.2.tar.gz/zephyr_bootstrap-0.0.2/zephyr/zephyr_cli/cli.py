# Python Library Imports
import os
import sys
import logging
import click


# Local Python Library Imports
from zephyr.zephyr_state.zephyr_state import ZephyrState
from zephyr.zephyr_utils import zephyr_utils, init_utils, module_utils, pipeline_utils


# Setup Zephyr Logging
LOGLEVEL = logging.INFO
logging.basicConfig(
    format="%(asctime)s | %(levelname)s : %(message)s",
    level=LOGLEVEL,
    stream=sys.stdout,
)
LOGGER = logging.getLogger("zephyr-log")


@click.group(invoke_without_command=False)
@click.version_option("0.0.1")
@click.pass_context
def zephyr_cli(cli_context: click.Context) -> None:
    """
    A Modular Pipeline Scaffolding Tool
    """

    cli_context.obj = ZephyrState()

    return None


@click.command("init")
@click.option("--custom", help="Your custom cookie cutter url", required=False)
def init_command(custom: str) -> None:
    """Create and initialize zephyr folder"""
    """
    Purpose:
        Create and initialize zephyr project
    Args:
        N/A
    Returns:
        N/A
    """

    if custom:
        click.echo("Building custom cookie cutter")
        init_utils.create_custom_project(custom)
        return

    LOGGER.info(f"initializing project...")
    init_utils.create_project()


# Module Command Group
@zephyr_cli.group("module")
def module_commands():
    """Module related commands"""
    pass


@module_commands.command(name="create", help="creates new module")
@click.option("--custom", help="Your custom cookie cutter url", required=False)
def module_create(custom: str) -> None:
    """Create and initialize zephyr module"""
    """
    Purpose:
        Create and initialize zephyr module
    Args:
        N/A
    Returns:
        N/A
    """

    # Check if in project
    if zephyr_utils.check_if_in_project():

        if custom:
            click.echo("Building custom module")
            module_utils.create_custom_module(custom)
            return

        # get module json
        project_json = zephyr_utils.load_json(".zephyr/config.json")
        project_name = project_json["project_name"]

        LOGGER.info(f"Creating module...")
        module_utils.create_module(project_name)


@module_commands.command(name="delete", help="deletes a module")
def module_delete() -> None:
    """Deletes a zephyr module"""
    """
    Purpose:
        Delete a zephyr module
    Args:
        N/A
    Returns:
        N/A
    """

    # Check if in project
    if zephyr_utils.check_if_in_project():

        # get module json
        zephyr_config = zephyr_utils.load_json(".zephyr/config.json")
        project_name = zephyr_config["project_name"]
        zephyr_moudles = zephyr_config["modules"]

        click.echo(f"Current modules: {zephyr_moudles}")
        module = click.prompt("Type module to delete", type=str)

        # check if valid module
        if module not in zephyr_moudles:
            click.echo(f"Invalid module : {module}")
            return

        click.confirm(
            f"Do you want to delete {module}",
            abort=True,
            default=False,
        )

        LOGGER.info(f"Deleting module...{module}")
        module_utils.delete_module(project_name, module)


# Pipeline Command Group
@zephyr_cli.group("pipeline")
def pipeline_commands():
    """Pipeline related commands"""
    pass


@pipeline_commands.command(name="create", help="creates new pipeline")
def pipeline_create() -> None:
    """Create and initialize zephyr pipeline"""
    """
    Purpose:
        Create and initialize zephyr pipeline
    Args:
        N/A
    Returns:
        N/A
    """

    # Check if in project
    if zephyr_utils.check_if_in_project():

        # get module json
        project_json = zephyr_utils.load_json(".zephyr/config.json")
        project_name = project_json["project_name"]

        LOGGER.info(f"Creating pipeline...")
        pipeline_utils.create_pipeline(project_name)


def setup_zephyr_cli() -> None:
    """
    Purpose:
        Build Command Groups for Zephyr CLI.
    Args:
        N/A
    Returns:
        N/A
    """

    # zephyr commands
    zephyr_cli.add_command(init_command)
    module_commands.add_command(module_create)
    module_commands.add_command(module_delete)
    pipeline_commands.add_command(pipeline_create)


if __name__ == "__main__":

    try:
        setup_zephyr_cli()
    except Exception as error:
        print(f"{os.path.basename(__file__)} failed due to error: {error}")
        raise error
