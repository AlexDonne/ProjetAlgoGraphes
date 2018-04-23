def hasher(points, t):
    hash1 = dict()
    hash2 = dict()
    hash3 = dict()
    hash4 = dict()
    for point in points:
        x1 = round(point.coordinates[0]/t)
        y1= round(point.coordinates[1]/t)
        hash1[(x1, y1)].append(point)

        x2 = round((point.coordinates[0] + t/2) / t)
        y2 = round(point.coordinates[1] / t)
        hash2[(x2, y2)].append(point)

        x3 = round(point.coordinates[0] / t)
        y3 = round((point.coordinates[1] + t/2) / t)
        hash3[(x3, y3)].append(point)

        x4 = round((point.coordinates[0] + t/2) / t)
        y4 = round((point.coordinates[1] + t/2) / t)
        hash4[(x4, y4)].append(point)

    return hash1, hash2, hash3, hash4

def deuxpointsenCollision(hash):
    pass

def ordered_segments(points):
    t = 1
    tables = list()
    tables.append(hasher(points, t))
    test = deuxpointsenCollision(tables[len(tables)-1])
    while test:
        t = t/2
        tables.append(hasher(points,t))
        test = deuxpointsenCollision(tables[len(tables) - 1])