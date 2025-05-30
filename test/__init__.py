import os
import sys

# Asegura que Python encuentre los módulos src
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))