import os, sys
import glob
import zipfile
import tempfile
import cadquery as cq


def _fc_path():
    """
    Pulled from cadquery-freecad-module.
    Used to find the FreeCAD installation so that it can be imported in Python.
    Parameters:
        None
    Returns:
        Path to any FreeCAD installation that was found.
    """

    # Look for FREECAD_LIB env variable
    _PATH = os.environ.get("FREECAD_LIB", "")
    if _PATH and os.path.exists(_PATH):
        return _PATH

    # Try to guess if using Anaconda
    if "env" in sys.prefix:
        if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
            _PATH = os.path.join(sys.prefix, "lib")
            # return PATH if FreeCAD.[so,pyd] is present
            if len(glob.glob(os.path.join(_PATH, "FreeCAD.so"))) > 0:
                return _PATH
        elif sys.platform.startswith("win"):
            _PATH = os.path.join(sys.prefix, "Library", "bin")
            # return PATH if FreeCAD.[so,pyd] is present
            if len(glob.glob(os.path.join(_PATH, "FreeCAD.pyd"))) > 0:
                return _PATH

    if sys.platform.startswith("linux"):
        home_dir = os.environ["HOME"]

        # Make some dangerous assumptions...
        for _PATH in [
            os.path.join(os.path.expanduser("~"), "lib/freecad/lib"),
            "/usr/local/lib/freecad/lib",
            "/usr/lib/freecad/lib",
            "/opt/freecad/lib/",
            "/usr/bin/freecad/lib",
            "/usr/lib/freecad-daily/lib",
            "/usr/lib/freecad",
            "/usr/lib64/freecad/lib",
            str(home_dir) + "/mambaforge/envs/freecad/lib/",
            str(home_dir) + "/miniforge/envs/freecad/lib/",
            str(home_dir) + "/conda/envs/freecad/lib/",
            str(home_dir) + "/condaforge/envs/freecad/lib/",
        ]:
            if os.path.exists(_PATH):
                return _PATH

    elif sys.platform.startswith("win"):
        # Try all the usual suspects
        for _PATH in [
            "c:/Program Files/FreeCAD0.12/bin",
            "c:/Program Files/FreeCAD0.13/bin",
            "c:/Program Files/FreeCAD0.14/bin",
            "c:/Program Files/FreeCAD0.15/bin",
            "c:/Program Files/FreeCAD0.16/bin",
            "c:/Program Files/FreeCAD0.17/bin",
            "c:/Program Files (x86)/FreeCAD0.12/bin",
            "c:/Program Files (x86)/FreeCAD0.13/bin",
            "c:/Program Files (x86)/FreeCAD0.14/bin",
            "c:/Program Files (x86)/FreeCAD0.15/bin",
            "c:/Program Files (x86)/FreeCAD0.16/bin",
            "c:/Program Files (x86)/FreeCAD0.17/bin",
            "c:/apps/FreeCAD0.12/bin",
            "c:/apps/FreeCAD0.13/bin",
            "c:/apps/FreeCAD0.14/bin",
            "c:/apps/FreeCAD0.15/bin",
            "c:/apps/FreeCAD0.16/bin",
            "c:/apps/FreeCAD0.17/bin",
            "c:/Program Files/FreeCAD 0.12/bin",
            "c:/Program Files/FreeCAD 0.13/bin",
            "c:/Program Files/FreeCAD 0.14/bin",
            "c:/Program Files/FreeCAD 0.15/bin",
            "c:/Program Files/FreeCAD 0.16/bin",
            "c:/Program Files/FreeCAD 0.17/bin",
            "c:/Program Files (x86)/FreeCAD 0.12/bin",
            "c:/Program Files (x86)/FreeCAD 0.13/bin",
            "c:/Program Files (x86)/FreeCAD 0.14/bin",
            "c:/Program Files (x86)/FreeCAD 0.15/bin",
            "c:/Program Files (x86)/FreeCAD 0.16/bin",
            "c:/Program Files (x86)/FreeCAD 0.17/bin",
            "c:/apps/FreeCAD 0.12/bin",
            "c:/apps/FreeCAD 0.13/bin",
            "c:/apps/FreeCAD 0.14/bin",
            "c:/apps/FreeCAD 0.15/bin",
            "c:/apps/FreeCAD 0.16/bin",
            "c:/apps/FreeCAD 0.17/bin",
            "C:/Miniconda/envs/freecad/bin",
        ]:
            if os.path.exists(_PATH):
                return _PATH

    elif sys.platform.startswith("darwin"):
        # Assume we're dealing with a Mac
        for _PATH in [
            "/Applications/FreeCAD.app/Contents/lib",
            "/Applications/FreeCAD.app/Contents/Resources/lib",
            os.path.join(
                os.path.expanduser("~"), "Library/Application Support/FreeCAD/lib"
            ),
        ]:
            if os.path.exists(_PATH):
                return _PATH

    raise ImportError("Unable to determine freecad library path")


def import_part_static(fc_part_path):
    """
    Imports without parameter handling by extracting the brep file from the FCStd file.
    Does NOT require FreeCAD to be installed.
    Parameters:
        fc_part_path - Path to the FCStd file to be imported.
    Returns:
        A CadQuery Workplane object or None if the import was unsuccessful.
    """

    res = None

    # Make sure that the caller gave a valid file path
    if not os.path.isfile(fc_part_path):
        print("Please specify a valid path.")
        return None

    # A temporary directory is required to extract the zipped files to
    with tempfile.TemporaryDirectory() as temp_dir:
        # Extract the contents of the file
        with zipfile.ZipFile(fc_part_path, "r") as zip_ref:
            zip_ref.extractall(temp_dir)

        # Open the file with CadQuery
        res = cq.Workplane(cq.Shape.importBrep(os.path.join(temp_dir, "PartShape.brp")))

    return res


def import_part_parametric(fc_part_path, parameters=None):
    """
    Uses FreeCAD to import a part and update it with altered parameters.
    Requires FreeCAD to be installed and importable in Python.
    Parameters:
        fc_part_path - Path to the FCStd file to be imported.
        parameters - Model parameters that should be used to modify the part.
    Returns:
        A CadQuery Workplane object or None if the import was unsuccessful.
    """

    # If the caller did not specify any parameters, might as well call the static importer
    if parameters == None:
        return import_part_static(fc_part_path)

    try:
        # Attempt to include the FreeCAD installation path
        path = _fc_path()
        sys.path.insert(0, path)

        # It should be possible to import FreeCAD now
        import FreeCAD
    except Exception as err:
        print(
            "FreeCAD must be installed, and it must be possible to import it in Python."
        )
        return None

    # Open the part file in FreeCAD and get the spreadsheet so we can update it
    doc = FreeCAD.openDocument(fc_part_path)

    # Get a reference to the the spreadsheet
    sheet = doc.getObject("Spreadsheet")

    # Update each matching item in the spreadsheet
    for key in parameters.keys():
        sheet.set(key, "=" + str(parameters[key]["value"]) + parameters[key]["units"])
        sheet.recompute()

    # We need to touch each model to have it update
    for object in doc.Objects:
        object.touch()

    # Make sure the 3D object is updated
    FreeCAD.ActiveDocument.recompute()

    # We use the local directory for now because FreeCAD does not seem to want to open files from the /tmp directory
    updated_path = "updated_part.FCStd"

    # Save the document and then re-open it as a static part
    doc.saveAs(updated_path)
    FreeCAD.ActiveDocument.saveAs(updated_path)

    # Re-import the model statically
    res = import_part_static(updated_path)

    # Close the open document
    FreeCAD.closeDocument(doc.Name)

    return res


def import_freecad_part(fc_part_path, parameters=None):
    """
    Wrapper method that chooses whether or not to do a static import based on whether
    or not parameters are passed.
    Parameters:
        fc_part_path - Path to the FCStd file to be imported.
        parameters - Model parameters that should be used to modify the part.
    Returns:
        A CadQuery Workplane object or None if the import was unsuccessful.
    """

    res = None

    # If there are no parameters specified, we can do a static import
    if parameters == None:
        res = import_part_static(fc_part_path)
    else:
        res = import_part_parametric(fc_part_path, parameters)

    return res


def get_freecad_part_parameters(fc_part_path, name_column_letter, value_column_letter):
    """
    Extracts the parameters from the spreadsheet inside the FCStd file.
    Does NOT require FreeCAD to be installed.
    Parameters:
        fc_part_path - Path to the FCStd file to be imported.
        name_column_letter - Allows the caller to specify the column of the spreadsheet where the parameter name can be found.
        value_column_letter - Allows the caller to specify the column of the spreadsheet where the parameter value can be found.
    Returns:
        A dictionary of the parameters, their initial values and the units of the values.
    """

    # Make sure that the caller gave a valid file path
    if not os.path.isfile(fc_part_path):
        print("Please specify a valid path.")
        return None

    # This will keep the collection of the parameters and their current values
    parameters = {}

    # To split units from values
    import re

    # So that the XML file can be parsed
    import xml.etree.ElementTree as ET

    # A temporary directory is required to extract the zipped files to
    with tempfile.TemporaryDirectory() as temp_dir:
        # Extract the contents of the file
        with zipfile.ZipFile(fc_part_path, "r") as zip_ref:
            zip_ref.extractall(temp_dir)

        # parse the Document.xml file that holds metadata like the spreadsheet
        tree = ET.parse(os.path.join(temp_dir, "Document.xml"))
        root = tree.getroot()
        objects = root.find("ObjectData")
        for object in objects.iter("Object"):
            if object.get("name") == "Spreadsheet":
                props = object.find("Properties")
                for prop in props.iter("Property"):
                    if prop.get("name") == "cells":
                        for cell in prop.find("Cells").iter():
                            if cell is None or cell.get("content") is None:
                                continue

                            # Determine whether we have a parameter name or a parameter value
                            if "=" not in cell.get("content"):
                                # Make sure we did not get a description
                                if (
                                    cell.get("address")[0] != name_column_letter
                                    and cell.get("address")[0] != value_column_letter
                                ):
                                    continue

                                # Start a parameter entry in the dictionary
                                parameters[cell.get("content")] = {}
                            elif "=" in cell.get("content"):
                                # Extract the units
                                units = "".join(
                                    re.findall("[a-zA-Z]+", cell.get("content"))
                                )
                                if units is not None:
                                    parameters[cell.get("alias")]["units"] = units
                                else:
                                    parameters[cell.get("alias")]["units"] = "N/A"

                                # Extract the parameter value and store it
                                value = (
                                    cell.get("content")
                                    .replace("=", "")
                                    .replace(units, "")
                                )
                                parameters[cell.get("alias")]["value"] = value
                break
            else:
                continue

        return parameters


# Patch the FreeCAD import functions into CadQuery's importers package
cq.importers.import_freecad_part = import_freecad_part
cq.importers.get_freecad_part_parameters = get_freecad_part_parameters
