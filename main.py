#!/usr/bin/env -S uv run

from datetime import datetime
import os
from pathlib import Path
from typing import Annotated
from typer import Option
import typer


extension_conversions = {
    ".gdoc": ".docx",
    ".gsheet": ".xlsx",
    ".gslide": ".pptx",
}
files_to_exclude = {"desktop.ini"}


def main(
    google_dir: Annotated[Path, Option(help="Google Drive dir to sync from")],
    sync_dir: Annotated[Path, Option(help="dir to sync to")],
) -> None:
    print(f"syncing {str(sync_dir)} from {str(google_dir)}")
    for google_path in sorted(google_dir.rglob("*"), reverse=True):
        rel_path = google_path.relative_to(google_dir)
        if rel_path.name in files_to_exclude:
            continue
        if rel_path.suffix in extension_conversions:
            rel_path = rel_path.with_suffix(extension_conversions[rel_path.suffix])
        sync_path = sync_dir / rel_path
        stat = google_path.stat()
        os.utime(sync_path, times=(stat.st_atime, stat.st_mtime))
        mtime = datetime.fromtimestamp(stat.st_mtime)
        print(f"syncing '{str(rel_path)}' to mtime {str(mtime)}")


if __name__ == "__main__":
    typer.run(main)
