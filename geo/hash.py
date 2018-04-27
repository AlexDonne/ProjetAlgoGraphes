"""
Hash module for the iterator on the hashed segments.
"""
from geo.segment import Segment
def hashed_segments(points, precision):
    """
    Return hashed tables for a given precision
    """
    tables = [dict(), dict(), dict(), dict()]
    collision = False
    for point in points:
        for i in range(4):
            carre = point.hasher(precision, i)
            tables[i].setdefault(carre, []).append(point)
            if len(tables[i][carre]) > 1:
                collision = True
    return tables, collision

def ordered_segments(points, precision):
    """
    Returns iterator on the hashed segments
    """
    tables = []
    tables_hash, collision = hashed_segments(points, precision)
    tables.append(tables_hash)
    while collision:
        precision = precision/2
        tables_hash, collision = hashed_segments(points, precision)
        tables.append(tables_hash)
    for table in reversed(tables):
        for table_hash in table:
            for carre in table_hash.keys():
                length = len(table_hash[carre])
                for i in range(length):
                    for j in range(i+1, length):
                        yield Segment([table_hash[carre][i], table_hash[carre][j]])
