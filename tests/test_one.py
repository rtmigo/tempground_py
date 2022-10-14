# SPDX-FileCopyrightText: (c) 2022 Artsiom iG <rtmigo.github.io>
# SPDX-License-Identifier: MIT

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tempground._dir_from_template import create_temp_project


class TestCreateProject(unittest.TestCase):
    def test_create_temp_project(self):
        with TemporaryDirectory() as tds:
            project_root = Path(tds) / "project"

            create_temp_project(
                template_path=(Path(__file__).parent / "data" /
                               "projects" / "dependency_from_github"),
                target_dir=project_root,
                basename_replacements={},
                string_replacements={
                    "__PACKAGE__": "org.sample.package",
                    "__REPO_URL__": "https://github.com/user/repo",
                    "__MAIN_KT__": "fun main()"})
            self.assertIn(
                "https://github.com/user/repo",
                (project_root / "settings.gradle.kts").read_text())
