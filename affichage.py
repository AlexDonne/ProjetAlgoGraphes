#!/usr/bin/env python3
"""
display given segment files
"""
import sys
import time
from geo.segment import load_segments
from geo.tycat import tycat
from geo.graph import Graph
sys.setrecursionlimit(9000000)


def display(filename):
    """
    load segment file, get back connexity, get even degrees, display eulerian path.
    """
    # seg = []
    segments = load_segments(filename)
    # for index, segment in enumerate(segments):
    #     if (index % 8)==0:
    #         seg.append(segment)
    g = Graph(segments)
    tycat(g)
    print("{}: nous avons {} segments".format(filename, len(segments)))
    t1 = time.time()
    g.reconnect(True)
    t2 = time.time()
    tps = t2 - t1
    print("Temps reconnect hash:" + str(tps))

    t1 = time.time()
    g.even_degrees(True)
    t2 = time.time()
    tps = t2 - t1
    print("Temps degré pair hash:" + str(tps))

    g = Graph(segments)
    t1 = time.time()
    g.reconnect(False)
    t2 = time.time()
    tps = t2 - t1
    print("Temps reconnect quad:" + str(tps))

    t1 = time.time()
    g.even_degrees(False)
    t2 = time.time()
    tps = t2 - t1
    print("Temps degré pair quad:" + str(tps))
    t1 = time.time()
    g.eulerian_cycle()
    t2 = time.time()
    tps = t2 - t1
    print("Temps cycle eulérien:" + str(tps))

def main():
    """
    launch test on each file.
    """
    for filename in sys.argv[1:]:
        display(filename)

main()


# for top in self.vertices.keys():
#     for segment in self.vertices[top]:
#         I += 1
#         connected_components.union(top, segment.endpoint_not(top))
# print(str(I))
# return connected_components
