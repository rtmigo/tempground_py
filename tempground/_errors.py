# SPDX-FileCopyrightText: (c) 2022 Artsiom iG <github.com/rtmigo>
# SPDX-License-Identifier: MIT
import warnings


class GradleRunFailed (Exception):
    def __init__(self, msg):
        warnings.warn("Obsolete 2022-09", DeprecationWarning)
        super().__init__(msg)


class UnexpectedOutput (Exception):
    def __init__(self, msg):
        super().__init__(msg)