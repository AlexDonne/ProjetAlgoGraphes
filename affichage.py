#!/usr/bin/env python3
"""
display given segment files
"""
import sys
from geo.segment import load_segments
from geo.tycat import tycat
from geo.graph import Graph
import time
sys.setrecursionlimit(9000000)


def display(filename):
    """
    load segment file, get back connexity, get even degrees, display eulerian path.
    """
    #seg = []
    segments = load_segments(filename)
    # for index, segment in enumerate(segments):
    #     if (index % 8)==0:
    #         seg.append(segment)
    g = Graph(segments)
    tycat(g)
    #print("{}: nous avons {} segments".format(filename, len(segments)))
    # t1 = time.clock()
    # g.reconnect(True)
    # t2 = time.clock()
    # tycat(g)
    # tps = t2 - t1
    # print("Temps hash:" + str(tps))
    # g = Graph(segments)
    # t1 = time.clock()
    # g.reconnect(False)
    # t2 = time.clock()
    # tycat(g)
    # tps = t2 - t1
    # print("Temps hash:" + str(tps))
    g.even_degrees(True)
    tycat(g,g.eulerian_cycle())

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
