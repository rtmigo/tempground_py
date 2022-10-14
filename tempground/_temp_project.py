from __future__ import annotations

import inspect
import shutil
import subprocess
import tempfile
import warnings
from collections.abc import Iterable
from pathlib import Path
from typing import List

from ._files import _rmtree_skipping_permission_errors


class Glob:
    def __init__(self,
                 src_ref: Path,
                 src_glob: str,
                 dst_ref: Path):
        self.src_glob = src_glob
        self.dst = dst_ref
        self.src_ref = src_ref

    def copy(self):
        # TODO unit test
        if self.src_ref is None:
            self.src_ref = Path(".").absolute()
        for p in self.src_ref.rglob(self.src_glob):
            abs_target = self.dst / p.relative_to(self.src_ref)
            print(f"Copying {p} to {abs_target}")
            if p.is_dir():
                shutil.copytree(p, abs_target)
            else:
                shutil.copy(p, abs_target)


class TempGround:
    def __init__(self,
                 files: dict[str, str],
                 copy: Iterable[Glob] | None = None):
        self.files = files
        self.copy = copy

    def _create(self, dst_dir: Path):
        for fn, contents in self.files.items():
            full_fn = dst_dir / fn
            full_fn.parent.mkdir(parents=True, exist_ok=True)
            full_fn.write_text(contents)
        if self.copy is not None:
            # TODO unit test
            for c in self.copy:
                match c:
                    case Glob():
                        c.copy()
                    case _:
                        raise TypeError(c)

    @property
    def project_dir(self) -> Path:
        if self._temp_dir is None:
            raise Exception("Unavailable")
        return self._temp_dir / "project"

    def __enter__(self) -> TempGround:
        self._temp_dir = Path(tempfile.mkdtemp())
        self._create(self.project_dir)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO test files really removed
        _rmtree_skipping_permission_errors(self._temp_dir)

    def print_files(self, unindent: bool = True):
        warnings.warn("Use print( tempground.files_content() )",
                      DeprecationWarning)
        print(self.files_content(unindent=unindent))

    def files_content(self, unindent: bool = True) -> str:
        lines: list[str] = list()

        def add_line(s: str):
            lines.append(s)

        for file in sorted(self.project_dir.rglob("*")):
            if file.is_file():
                add_line(
                    _header(f'file "{file.relative_to(self.project_dir)}"'))
                add_line("")
                text = file.read_text()
                if unindent:
                    text = inspect.cleandoc(text)
                add_line(text)
                add_line("")
        add_line(_header("end of files"))
        return "\n".join(lines)

    def run(self, args: List[str]) -> CompletedRun:
        result = subprocess.run(args,
                                cwd=self.project_dir,
                                universal_newlines=True,
                                # triggering text mode
                                capture_output=True)
        return CompletedRun(result)


def _header(text: str, width: int = 80) -> str:
    return ("## " + text + " ").ljust(width, "#")


class CompletedRun:
    def __init__(self, cp: subprocess.CompletedProcess):
        self.completed_process = cp

    @property
    def args(self):
        return self.completed_process.args

    @property
    def returncode(self):
        return self.completed_process.returncode

    @property
    def stdout(self):
        return self.completed_process.stdout

    @property
    def stderr(self):
        return self.completed_process.stderr

    def __str__(self):
        class_name = self.__class__.__name__
        prefix = f"{self.__class__.__name__}."
        lines = [
            _header(class_name),
            f"{class_name}.args = {self.args}",
            f"{class_name}.returncode = {self.returncode}"
        ]

        stdout_empty = self.stdout == ""
        stderr_empty = self.stderr == ""

        if stdout_empty:
            lines.append(f"{class_name}.stdout is empty")
        if stderr_empty:
            lines.append(f"{class_name}.stderr is empty")

        if not stdout_empty:
            lines += [
                _header(f"{class_name}.stdout"),
                self.stdout,
            ]

        if not stderr_empty:
            lines += [
                _header(f"{class_name}.stderr"),
                self.stderr,
            ]

        lines += [_header(f"end of {class_name}")]

        return "\n\n".join(lines)
