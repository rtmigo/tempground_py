from __future__ import annotations

import os
import shutil
from pathlib import Path


def _rmtree_skipping_permission_errors(path: Path):
    # TODO test
    if path.is_dir():
        try:
            shutil.rmtree(path)
        except PermissionError:
            # Happens on Windows, when deleting .git subdir.
            # We cannot delete the whole `path`, but we can try to delete
            # something inside of it.
            for sub in path.glob("*"):
                _rmtree_skipping_permission_errors(sub)
    else:
        try:
            os.remove(path)
        except PermissionError:
            pass
