#!/usr/bin/env python
"""
Module which does a couple of things:
* It puts the project's package on sys.path.
* It sets the DJANGO_SETTINGS_MODULE environment variable so that it points to
the project's docker.py file.
"""

import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cdapi.docker')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
