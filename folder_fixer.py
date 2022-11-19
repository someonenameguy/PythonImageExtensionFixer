import imghdr
import pathlib
from typing import Optional, NamedTuple


class FilesEditionResult(NamedTuple):
    number_of_edits: int
    edited_files: list[pathlib.Path]


def fix_folders_images_extensions(
    folder: pathlib.Path, dry: bool = False
) -> FilesEditionResult:
    """
    Goes around folder and looks for images files which extension in name
    mismatch detected image extension and fixes that.

    :param folder: an folder path wrapped in pathlib.Path.
    :param dry: doesn't actually edit files names.
    :return: amount of edited files and which files has been edited.
    """
    edited_files_count: int = 0
    edited_files: list[pathlib.Path] = []

    if not folder.is_dir():
        raise ValueError("Must get an actual folder to fix images")

    for image in folder.iterdir():
        if not image.is_file():
            continue

        possible_extension: Optional[str] = imghdr.what(image)
        if possible_extension is None:
            continue

        file_extension_detected: str = f".{possible_extension}"
        if image.suffix != file_extension_detected:
            if not dry:
                image.rename(image.with_suffix(f".{file_extension_detected}"))
            edited_files_count += 1
            edited_files.append(image)

    return FilesEditionResult(edited_files_count, edited_files)
