import traceback
from pathlib import Path
from typing import Literal

import typer

MODE_EXPORT = "e"

MODE_IMPORT = "i"

EXPORTED_FILE_EXTENSION = ".out.txt"

EXPORTED_FILE_PATTERN = f"*{EXPORTED_FILE_EXTENSION}"


def get_output_filepath(mode: Literal['e', 'i'], fp: Path, root_input_folder: Path, root_output_folder: Path) -> Path:
    if root_input_folder:
        fp_relative = root_output_folder / fp.relative_to(root_input_folder).parent
    else:
        fp_relative = root_output_folder

    filename = fp.name
    if mode == MODE_EXPORT:
        filename += EXPORTED_FILE_EXTENSION
    else:
        filename = filename.removesuffix(EXPORTED_FILE_EXTENSION)

    return fp_relative / filename


def get_filepaths_from_folder_path(root_path: Path, file_pattern: str, search_recursive: bool) -> list[Path]:
    method = "rglob" if search_recursive else "glob"
    return [
        filepath
        for filepath in getattr(root_path, method)(file_pattern)
    ]


def is_valid_filepath(filepath: Path) -> bool:
    if not filepath.exists():
        typer.echo(f"❌ This file does not exists, will be skipped: {filepath.absolute()}")
        return False

    if filepath.is_dir():
        typer.echo(f"⚠️ This file is a folder and will be ignored: {filepath.absolute()}")
        return False

    return True


def ex_handler(ex: Exception):
    typer.echo(f"❌ Something went wrong: {ex}")
    typer.echo(traceback.format_exc())
