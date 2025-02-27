"""
This file is used to add the parent directory to the sys.path so that the tests can be run from the root directory.
Not intended to be used as a standalone script.
"""

import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
