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
            for j in range(i + 1, length):
                segments.append(Segment([points[i], points[j]]))
        return sorted(segments, key=lambda segment: segment.length())

    def reconnect(self, hash_points):
        """
        greedily add edges until graph is fully connected.
        if hash_points is true then use hashed segments iterator
        else use quadratic segments iterator.
        """
        if hash_points:
            iterator = hashed_iterator(self.vertices.keys())
        else:
            iterator = self.quadratic_iterator()
        connected_components = self.connected_components()
        for segment in iterator:
            compp1 = connected_components.find(segment.endpoints[0])
            compp2 = connected_components.find(segment.endpoints[1])
            if compp1 != compp2:
                self.vertices[segment.endpoints[0]].append(segment)
                self.vertices[segment.endpoints[1]].append(segment)
                connected_components.union(compp1, compp2)
            if len(connected_components) == 1:
                return

    def top_not_marked(self, tops_dict):
        """
        Retourne le premier sommet non marqué
        """
        for top, marked in tops_dict.items():
            if marked is False:
                return top
        return None

    def connected_components(self):
        """
        Retoure l'union find comportant les composantes connexes
        """
        connected_components = UnionFind()
        tops_dict = dict()
        for key in self.vertices.keys():
            tops_dict[key] = False
        top = self.top_not_marked(tops_dict)
        while top is not None:
            connected_components.add(top)
            self.parcours(top, tops_dict, connected_components)
            top = self.top_not_marked(tops_dict)
        return connected_components

    def parcours(self, top, tops_dict, connected_components):
        """
        Parcours le graphe à partir d'un sommet et marque les sommets traversés
        Ajoute chaque sommet à l'unionfind et unit tout ceux qui sont dans la même
        composante connexe
        """
        tops_dict[top] = True
        for segment in self.vertices[top]:
            endpointnot = segment.endpoint_not(top)
            if tops_dict[endpointnot] != True:
                connected_components.add(endpointnot)
                connected_components.union(top, endpointnot)
                self.parcours(endpointnot, tops_dict, connected_components)

    def even_degrees(self, hash_points):
        """
        greedily add edges until all degrees are even.
        if hash_points is true then use hashed segments iterator
        else use quadratic segments iterator.
        """
        if hash_points:
            iterator = hashed_iterator(self.vertices.keys())
        else:
            iterator = self.quadratic_iterator()
        impairs = sum(1 for e in self.vertices.values() if len(e) % 2 == 1)
        while impairs != 0:
            for segment in iterator:
                if len(self.vertices[segment.endpoints[0]]) %2 == 1 and \
                 len(self.vertices[segment.endpoints[1]]) %2 == 1:
                    self.vertices[segment.endpoints[0]].append(segment)
                    self.vertices[segment.endpoints[1]].append(segment)
                    impairs -= 2




    def eulerian_cycle(self):
        """
        return eulerian cycle. precondition: all degrees are even.
        """
        pass
