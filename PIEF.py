import imghdr
import pathlib
from pathlib import Path
from argparse import ArgumentParser
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
                try:
                    image.rename(image.with_suffix(file_extension_detected))

                except FileExistsError:
                    continue

            edited_files_count += 1
            edited_files.append(image)

    return FilesEditionResult(edited_files_count, edited_files)

parser = ArgumentParser(
    "Image extensions fixer",
    description="Fixes images extensions in folders"
)
parser.add_argument(
    "--folders", "-f", action="store", dest="folders",
    type=Path, required=True, nargs='+',
    help="List folders that you want to fix images extensions of"
)
parser.add_argument(
    "--dry", "-dry", action="store_true", dest="dry_run",
    required=False, default=False,
    help="Runs program without renaming files on disk to see if everything is fine"
)

args, unknown = parser.parse_known_args()
collected_edits: FilesEditionResult = FilesEditionResult(0, [])

for path in args.folders:
    edits: FilesEditionResult = fix_folders_images_extensions(
        path, dry=args.dry_run
    )
    collected_edits = FilesEditionResult(
        collected_edits.number_of_edits + edits.number_of_edits,
        collected_edits.edited_files + edits.edited_files
    )

print(f"Total files edited: {edits.number_of_edits}")

if args.dry_run:
    print("Edited:", *edits.edited_files, sep="\n")
