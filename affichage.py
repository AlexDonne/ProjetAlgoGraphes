#!/usr/bin/env python3
"""
display given segment files
"""
import sys
from geo.segment import load_segments
from geo.tycat import tycat
from geo.graph import Graph
from geo.hash import hashed_iterator

def display(filename):
    """
    load segment file, get back connexity, get even degrees, display eulerian path.
    """
    segments = load_segments(filename)
    g = Graph(segments)
    tycat(g)
    #print("{}: nous avons {} segments".format(filename, len(segments)))
    g.reconnect(True)
    tycat(g)

def main():
    """
    launch test on each file.
    """
    for filename in sys.argv[1:]:
        display(filename)

main()
