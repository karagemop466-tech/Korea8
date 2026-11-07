#!/usr/bin/env python3
"""Compatibility entrypoint: canonical verification now lives in verify_overflow_site.py."""
from verify_overflow_site import main
import sys
if __name__=='__main__': sys.exit(main())
