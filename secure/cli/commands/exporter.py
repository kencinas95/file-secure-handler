import copy
import sys
from pathlib import Path
from typing import List

import typer
from typer import Option

from secure.cli.commands.commons import is_valid_filepath, get_filepaths_from_folder_path, get_output_filepath, \
    MODE_EXPORT
from secure.exporter import SecureExporter


def export(paths: List[str],
           password: str = Option(..., "--password", "-p", prompt=True, hide_input=True,
                                  confirmation_prompt=True),
           output_root: str = Option("output", "--output", "-o"),
           file_pattern: str = Option("*.*", "--file-pattern", "-fp"),
           search_recursive: bool = Option(False, "--search-recursive", "-r", is_flag=True)):
    # Initializes input folder path
    root_input_folder = None

    # Validates paths
    if len(paths) == 0:
        raise ValueError("Given paths are empty, at least one path should be given!")

    # Output folder root
    root_output_folder = Path(output_root)
    root_output_folder.mkdir(parents=True, exist_ok=True)

    # Converts path strings to Path objects
    filepaths = [Path(path) for path in paths]

    if filepaths[0].exists() and filepaths[0].is_dir():
        root_input_folder = copy.copy(filepaths[0])

        typer.echo("⚠️ Warning: the first given path is a folder, following paths will be ignored!")
        typer.echo(f"⚠️ Using as root path: {root_input_folder.absolute()}")
        typer.echo(f"⚠️ Using file pattern: {file_pattern}")
        typer.echo(f"⚠️ Search recursive?: {'Yes' if search_recursive else 'No'}")

        # Get the filepaths from the folder path by using the given filepattern
        filepaths = get_filepaths_from_folder_path(root_input_folder, file_pattern, search_recursive)

    # Filter filepaths
    filepaths = list(filter(is_valid_filepath, filepaths))
    if len(filepaths) == 0:
        typer.echo("❌ No given filepath was valid: export failed!")
        sys.exit(1)

    exporter = SecureExporter(password)
    for filepath in filepaths:
        with open(filepath, "rb") as fp_reader:
            # Get the output filepath
            output_filepath = get_output_filepath(MODE_EXPORT, filepath, root_input_folder, root_output_folder)

            # Writes the export file
            output_filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(output_filepath, "w") as fp_writer:
                fp_writer.write(
                    exporter.export(fp_reader.read())
                )
