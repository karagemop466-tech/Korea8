#!/usr/bin/env python3
"""Compatibility entrypoint. The canonical build is scripts/build_overflow_site.py.
The previous session-5d4c76bb generator is archived under archive/superseded-2026-11-07/.
"""
import runpy, pathlib, sys
runpy.run_path(str(pathlib.Path(__file__).with_name('build_overflow_site.py')), run_name='__main__')
