# encode = utf-8

"""
This module is used to filter and reload PATH.
This file is genrated by Splunk add-on builder
"""

import os
import sys
import re


ta_name = 'TA_cortex'
ta_lib_name = 'ta_cortex'
pattern = re.compile(r"[\\/]etc[\\/]apps[\\/][^\\/]+[\\/]bin[\\/]?$")
new_paths = [path for path in sys.path if not pattern.search(path) or ta_name in path]
new_paths.insert(0, os.path.sep.join([os.path.dirname(__file__), "lib"]))
if sys.version_info >= (3,0):
    new_paths.insert(0, os.path.sep.join([os.path.dirname(__file__), "lib3"]))
else:
    new_paths.insert(0, os.path.sep.join([os.path.dirname(__file__), "lib2"]))
sys.path = new_paths

