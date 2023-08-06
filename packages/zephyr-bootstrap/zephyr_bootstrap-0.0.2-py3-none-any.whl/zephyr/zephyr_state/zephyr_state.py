# mypy: ignore-errors
"""
    Purpose:
        The ZephyrState is responsible for holding state information for the CLI
"""

# Python Library Imports
# N/A

# Local Python Library Imports
from zephyr.zephyr_utils import zephyr_utils
from zephyr.zephyr_config.config import Config


class ZephyrState:
    """
    Purpose:
        The ZephyrState is responsible for holding state information for the CLI
    """

    ###
    # Attributes
    ###

    # Base Config Option
    config = None

    ###
    # Lifecycle Methods
    ###

    def __init__(self) -> None:
        """
        Purpose:
            Initialize the ZephyrState object.
        Args:
            N/A
        Returns:
            Zephyr_state_obj (ZephyrState Obj): State object
        """

        self.config = zephyr_utils.load_configs()

    def __repr__(self) -> str:
        """
        Purpose:
            Representation of the ZephyrState object.
        Args:
            N/A
        Returns:
            str_ZephyrState: String representation of ZephyrState
        """

        return f"<ZephyrState (version {Config.VERSION})>"