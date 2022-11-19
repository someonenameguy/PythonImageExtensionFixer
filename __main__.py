from pathlib import Path
from argparse import ArgumentParser

from folder_fixer import fix_folders_images_extensions, FilesEditionResult


parser = ArgumentParser(
    "Image extensions fixer",
    description="Fixes images extensions in folders"
)
parser.add_argument(
    "--folders", "-f", action="store", dest="folders",
    type=Path, required=True, nargs='+',
    help="Sets path to config file to launch Gaby with"
)
parser.add_argument(
    "--dry", "-dry", action="store_true", dest="dry_run",
    required=False, default=False,
    help="Sets path to config file to launch Gaby with"
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

