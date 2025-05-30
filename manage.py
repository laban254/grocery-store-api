#!/usr/bin/env python
"""
Wrapper script to run Django's manage.py from the root directory.
This allows you to run Django commands from the project root.
"""
import os
import sys

if __name__ == "__main__":
    # Add the src directory to Python path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))
    
    # Execute the manage.py script in the src directory
    os.chdir(os.path.join(os.path.dirname(__file__), "src"))
    os.system(f"python manage.py {' '.join(sys.argv[1:])}")
