import copy
import sys
from pathlib import Path

import typer
from typer import Option

from secure.cli.commands.commons import EXPORTED_FILE_PATTERN, get_output_filepath, MODE_IMPORT, ex_handler
from secure.cli.commands.commons import get_filepaths_from_folder_path
from secure.cli.commands.commons import is_valid_filepath
from secure.importer import SecureImporter

# Override function
get_filepaths_from_folder_path_overridden = lambda root_input_folder: get_filepaths_from_folder_path(
    root_input_folder, EXPORTED_FILE_PATTERN, True
)


def import_(paths: list[Path],
            password: str = Option(..., "-p", prompt=True, hide_input=True, confirmation_prompt=True),
            output_root: str = Option("imported", "-o", "--output")):
    if len(paths) == 0:
        raise ValueError("Given paths are empty, at least one path should be given!")

    root_input_folder = None

    filepaths = [Path(path) for path in paths]

    root_output_folder = Path(output_root)
    root_output_folder.mkdir(parents=True, exist_ok=True)

    if filepaths[0].exists() and filepaths[0].is_dir():
        root_input_folder = copy.copy(filepaths[0])

        typer.echo("⚠️ Warning: the first given path is a folder, following paths will be ignored!")
        typer.echo(f"⚠️ Using as root path: {root_input_folder.absolute()}")

        filepaths = get_filepaths_from_folder_path_overridden(root_input_folder)

    # Filter filepaths
    filepaths = list(filter(is_valid_filepath, filepaths))
    if len(filepaths) == 0:
        typer.echo("❌ No given filepath was valid: export failed!")
        sys.exit(1)

    importer = SecureImporter(password)

    for filepath in filepaths:
        with open(filepath, "r") as fp_reader:
            output_filepath = get_output_filepath(MODE_IMPORT, filepath, root_input_folder, root_output_folder)
            output_filepath.parent.mkdir(parents=True, exist_ok=True)

            with open(output_filepath, "wb") as fp_writer:
                fp_writer.write(
                    importer.resolve(fp_reader.read(), ex_handler)
                )
