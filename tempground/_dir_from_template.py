# SPDX-FileCopyrightText: (c) 2022 Artsiom iG <github.com/rtmigo>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import shutil
from pathlib import Path


def _replace_in_string(text: str, replacements: dict[str, str]) -> str:
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return text


def _header(txt: str, c: str) -> str:
    return f"{c}{c} {txt} ".ljust(80, c)


def _replace_in_dir(parent: Path,
                    string_replacements: dict[str, str],
                    basename_replacements: dict[str, str],
                    ):
    for p in parent.rglob('*'):
        if p.is_file():
            old_text = p.read_text()

            new_text = basename_replacements.get(p.name)
            if new_text is None:
                new_text = old_text

            new_text = _replace_in_string(new_text, string_replacements)
            if new_text != old_text:
                p.write_text(new_text)

            tag_name = str(Path("project") / p.relative_to(parent))
            print(_header(tag_name + " begin", '>'))
            print(p.read_text())
            print(_header(tag_name + " end", '<'))
            print()


def create_temp_project(template_path: Path,
                        target_dir: Path,
                        string_replacements: dict[str, str],
                        basename_replacements: dict[str, str]):
    src_dir = template_path
    if not src_dir.exists():
        raise FileNotFoundError(src_dir)
    if target_dir.exists():
        raise FileExistsError(target_dir)
    shutil.copytree(src_dir, target_dir)
    _replace_in_dir(target_dir, string_replacements=string_replacements,
                    basename_replacements=basename_replacements)
