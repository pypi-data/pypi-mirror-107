#!/usr/bin/env python

from .arguments import Arguments
from yt_dlp import main as ytmain


def main(argv=None):
    args = Arguments(argv)
    args.check()
    try:
        ytmain(["-x", "-o", r"%(title)s.%(ext)s", args.arguments.url])
    except SystemExit as e:
        if e.code != 0:
            raise e
