#!/usr/bin/env python3
"""Compatibility entry point: export only the current user-only educational beta.

Never embeds historical community snapshots. No network or deployment.
"""
import argparse
from pathlib import Path
try:
    from scripts.export_beta import export
except ModuleNotFoundError:
    from export_beta import export
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('.private/hytale-craft-preview.html'))
    args=parser.parse_args();print('User-only educational beta export:',export(args.output))
