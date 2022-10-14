# SPDX-FileCopyrightText: (c) 2022 Artsiom iG <github.com/rtmigo>
# SPDX-License-Identifier: MIT

from pathlib import Path

from ._errors import UnexpectedOutput  # , GradleRunFailed
# from ._obsolete_app_with_git_dep import AppWithGitDependency
# from ._obsolete_gradle import RunResult
from ._temp_project import TempProject, CompletedRun

# assert (Path(__file__).parent / "data").exists()
# assert (Path(__file__).parent / "data" / "dependency_from_github").exists()
# assert (Path(__file__).parent / "data" / "dependency_from_github"
#         / "src" / "main" / "kotlin" / "Main.kt").exists()
