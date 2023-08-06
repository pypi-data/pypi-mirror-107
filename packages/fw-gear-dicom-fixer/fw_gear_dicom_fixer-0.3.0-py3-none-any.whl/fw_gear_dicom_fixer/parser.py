"""Parser module to parse gear config.json."""

import typing as t

from flywheel_gear_toolkit import GearToolkitContext


def parse_config(
    gear_context: GearToolkitContext,
) -> t.Dict:
    """Parses gear_context config.json file and returns relevant inputs and
    options."""

    return gear_context.get_input("dicom")
