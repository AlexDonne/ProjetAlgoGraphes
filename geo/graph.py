"""
graph structure
"""
from itertools import chain, combinations
from geo.hash import hashed_iterator
from geo.quadrant import Quadrant
from geo.segment import Segment
from geo.union import UnionFind

class Graph:
    """
    create a graph from given set of segments.
    each endpoint is a vertex, each segment an edge.
    """
    def __init__(self, segments):
        self.vertices = dict()
        for segment in segments:
            for point in segment.endpoints:
                if point not in self.vertices:
                    self.vertices[point] = []
                self.vertices[point].append(segment)

    def bounding_quadrant(self):
        """
        return min quadrant containing underlying objects.
        """
        quadrant = Quadrant.empty_quadrant(2)
        for point in self.vertices:
            quadrant.add_point(point)
        return quadrant

    def svg_content(self):
        """
        svg for tycat.
        """
        edges = (e for (p, edges) in self.vertices.items() for e in edges if e.endpoints[0] == p)
        return "\n".join(c.svg_content() for c in chain(self.vertices.keys(), edges))

    def quadratic_iterator(self):
        """
        Iterator on a quadratic number of segments
        """
        points = list(self.vertices.keys())
        segments = []
        length = len(self.vertices)
        for i in range(length):
            for j in range(i + 1,length):
                segments.append(Segment([points[i], points[j]]))
        return sorted(segments, key=lambda segment: segment.length())

    def reconnect(self, hash_points):
        """
        greedily add edges until graph is fully connected.
        if hash_points is true then use hashed segments iterator
        else use quadratic segments iterator.
        """
        if hash_points == True:
            iterator = hashed_iterator(self.vertices.keys())
        else:
            iterator = self.quadratic_iterator()
        C = UnionFind(self.vertices.keys())
        for segment in iterator:
            compp1 = C.find(segment.endpoints[0])
            compp2 = C.find(segment.endpoints[0])
            if compp1 != compp2:
                self.vertices[segment.endpoints[0]].append(segment)
                self.vertices[segment.endpoints[1]].append(segment)
                C.union(compp1, compp2)
            if len(C) == 1:
                return


    def even_degrees(self, hash_points):
        """
        greedily add edges until all degrees are even.
        if hash_points is true then use hashed segments iterator
        else use quadratic segments iterator.
        """
        if hash_points == True:
            iterator = hashed_iterator(self.vertices.keys())
        else:
            iterator = self.quadratic_iterator()
        sommets_impairs = list(e for e in self.vertices.values() if len(e) % 2 == 1)
        impairs = len(sommets_impairs)
        while impairs != 0:
            for segment in iterator:
                if segment.endpoints[0] in sommets_impairs and segment.endpoints[1] in sommets_impairs:
                    self.vertices[segment.endpoints[0]].append(segment)
                    self.vertices[segment.endpoints[1]].append(segment)
                    impairs -= 2




    def eulerian_cycle(self):
        """
        return eulerian cycle. precondition: all degrees are even.
        """
        pass
