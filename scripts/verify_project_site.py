#!/usr/bin/env python3
"""Compatibility entrypoint: the superseded project/*.json verifier is archived at
archive/superseded-2026-11-07/verify_project_site.py. Canonical verification runs
via scripts/verify_overflow_site.py against overflow-integration/data/.
"""
import sys
from verify_overflow_site import main

if __name__ == '__main__':
    sys.exit(main())
