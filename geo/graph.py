"""
graph structure
"""
import copy
from itertools import chain, combinations
from geo.hash import ordered_segments
from geo.quadrant import Quadrant
from geo.segment import Segment
from geo.union import UnionFind
from geo.point import Point
from geo.tycat import tycat

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

    def quadratic_iterator(self, tops):
        """
        Iterator on a quadratic number of segments
        """
        segments = []
        length = len(tops)
        for i in range(length):
            for j in range(i + 1, length):
                segments.append(Segment([tops[i], tops[j]]))
        for segment in sorted(segments, key=lambda segment: segment.length()):
            yield segment

    def get_first_precision(self):
        """
        Returns the length of the longer possible segment, to start the paving
        """
        quadrant = self.bounding_quadrant()
        point_min = Point(quadrant.min_coordinates)
        point_max = Point(quadrant.max_coordinates)
        segmax = Segment([point_min, point_max])
        maxlength = segmax.length()
        return 2*maxlength

    def reconnect(self, hash_points):
        """
        greedily add edges until graph is fully connected.
        if hash_points is true then use hashed segments iterator
        else use quadratic segments iterator.
        """
        if hash_points:
            iterator = ordered_segments(self.vertices.keys(), self.get_first_precision())
        else:
            iterator = self.quadratic_iterator(list(self.vertices.keys()))
        connected_components = self.connected_components()
        # Ligne du dessous à décommenter pour utiliser notre algo optimisé
        # return
        #Algo DEMANDE
        if len(connected_components) == 1:
            return
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
        tops_separed = []
        connected_components = UnionFind(self.vertices.keys())
        tops_dict = dict()
        for key in self.vertices.keys():
            tops_dict[key] = False
        top = self.top_not_marked(tops_dict)
        tops_separed.append(top)
        while top is not None:
            self.parcours(top, tops_dict, connected_components)
            top = self.top_not_marked(tops_dict)
            tops_separed.append(top)
        top_first = tops_separed[0]
        # A décommenter pour utiliser notre algo optimisé
        # for i in range(1, len(tops_separed)-1):
        #     self.vertices[top_first].append(Segment([top_first,tops_separed[i]]))
        #     self.vertices[tops_separed[i]].append(Segment([top_first,tops_separed[i]]))
        return connected_components

    def parcours(self, top, tops_dict, connected_components):
        """
        Parcours le graphe à partir d'un sommet et marque les sommets traversés
        Unit les sommets qui sont dans la même composante dans l'unionfind
        """
        tops_dict[top] = True
        for segment in self.vertices[top]:
            endpointnot = segment.endpoint_not(top)
            if tops_dict[endpointnot] != True:
                connected_components.union(top, endpointnot)
                self.parcours(endpointnot, tops_dict, connected_components)

    def even_degrees(self, hash_points):
        """
        greedily add edges until all degrees are even.
        if hash_points is true then use hashed segments iterator
        else use quadratic segments iterator.
        """
        sommets_impairs = []
        impairs = 0
        for top in self.vertices.keys():
            if len(self.vertices[top]) % 2 == 1:
                impairs += 1
                sommets_impairs.append(top)
        if hash_points:
            #décommenter en dessous et commenter celle d'après pour optimisation
            # iterator = ordered_segments(sommets_impairs, self.get_first_precision())
            iterator = ordered_segments(self.vertices.keys(), self.get_first_precision())
        else:
            # décommenter en dessous et commenter celle d'après pour optimisation
            # iterator = self.quadratic_iterator(sommets_impairs)
            iterator = self.quadratic_iterator(list(self.vertices.keys()))
        while impairs != 0:
            segment = next(iterator)
            if len(self.vertices[segment.endpoints[0]]) %2 == 1 and \
                len(self.vertices[segment.endpoints[1]]) %2 == 1:
                self.vertices[segment.endpoints[0]].append(segment)
                self.vertices[segment.endpoints[1]].append(segment)
                impairs -= 2

    def remove_segment(self, top1, top2, vertices):
        """
        Remove a segment in vertices of a graph
        """
        vertices[top1].remove(Segment([top1, top2]))
        vertices[top2].remove(Segment([top1, top2]))


    def eulerian_cyle_from_top(self, begin, cycle, vertices):
        """
        Returns an eulerian cycle from a top
        """
        if len(vertices[begin]) == 0:
            return
        cycle.append(begin)
        current = vertices[begin][0].endpoint_not(begin)
        self.remove_segment(begin, current, vertices)
        while current != begin:
            cycle.append(current)
            previous = current
            if len(vertices[current]) == 0:
                return
            current = vertices[current][0].endpoint_not(current)
            self.remove_segment(previous, current, vertices)

    def eulerian_cycle(self):
        """
        return eulerian cycle. precondition: all degrees are even.
        """
        vertices = copy.deepcopy(self.vertices)
        begin = list(self.vertices.keys())[0]
        cycle = []
        self.eulerian_cyle_from_top(begin, cycle, vertices)
        if len(cycle) != len(self.vertices):
            for top in cycle:
                self.eulerian_cyle_from_top(top, cycle, vertices)
        return cycle
