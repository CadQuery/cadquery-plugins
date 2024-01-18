import os
from pathlib import Path
import pytest
from plugins.freecad_import.freecad_importer import (
    import_freecad_part,
    get_freecad_part_parameters,
)


def test_static_import():
    """
    Imports a sample model without trying to change its parameters.
    """

    # We need to find the path to our FreeCAD test files
    test_dir_path = Path(__file__).resolve().parent
    static_file_path = os.path.join(test_dir_path, "testdata", "box.FCStd")

    # Perform the import of the FreeCA file into CadQuery
    result = import_freecad_part(static_file_path)

    # Make sure the box quacks like a box
    assert result.vertices().size() == 8
    assert result.edges().size() == 12
    assert result.faces().size() == 6


def test_parametric_import():
    """
    Imports a sample model while altering its parameters.
    """

    # We need to find the path to our FreeCAD test files
    test_dir_path = Path(__file__).resolve().parent
    parametric_file_path = os.path.join(test_dir_path, "testdata", "base_shelf.FCStd")

    # First import the model with default parameters and make sure the volume is as expected
    result = import_freecad_part(parametric_file_path)
    vol = result.val().Volume()
    assert vol > 46742 and vol < 46743

    # Import the model with modified parameters and make sure the volume has decreased by the appropriate amount
    result = import_freecad_part(
        parametric_file_path, parameters={"mount_dia": {"value": 4.8, "units": "mm"}}
    )
    vol = result.val().Volume()
    assert vol > 46634 and vol < 46635


def test_get_parameters():
    """
    Retrieves parameters from a model.
    """

    # We need to find the path to our FreeCAD test files
    test_dir_path = Path(__file__).resolve().parent
    parametric_file_path = os.path.join(test_dir_path, "testdata", "base_shelf.FCStd")

    # Get the parameters from the objectr
    params = get_freecad_part_parameters(
        parametric_file_path, name_column_letter="A", value_column_letter="B"
    )

    # Make sure that the correct numbers of parameters are present and do a spot check on the presence of parameters
    assert len(params) == 20
    assert "mount_dia" in params
    assert "internal_rail_spacing" in params
