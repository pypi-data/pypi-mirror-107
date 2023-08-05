#!/usr/bin/env python

from .arguments import Arguments
from yt_dlp import main as ytmain


def main():
    args = Arguments()
    args.check()
    ytmain(["-x", args.arguments.url])
