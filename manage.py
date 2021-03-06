#!/usr/bin/env python
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
import sys
from multiprocessing import Process
from detectDrowsiness import cnn

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    if sys.argv[1] == 'runserver':
        p1 = Process(target=main)
        p2 = Process(target=cnn)

        p1.start()
        p2.start()

        p2.join()

    else:
        main()
