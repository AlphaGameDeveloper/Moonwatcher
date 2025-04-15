# Copyright (c) 2025 Damien Boisvert (AlphaGameDeveloper)
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import unittest
import sys

suite = unittest.TestLoader().discover("moon/tests/", pattern="*.py")

if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(suite)
 
    if result.errors or result.failures:
        exit(1)