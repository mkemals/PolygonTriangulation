import sys

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Polygon:
    def __init__(self, points):
        self.points = points
    @property
    def edges(self):
        edge_list = []
        for i,p in enumerate(self.points):
            p1 = p
            p2 = self.points[(i+1) % len(self.points)]
            edge_list.append((p1,p2))
        return edge_list

    def contains(self, point):
        _eps = 0.00001
        inside = False
        for edge in self.edges:
            A, B = edge[0], edge[1]
            if A.y > B.y:
                A, B = B, A
            if point.y == A.y or point.y == B.y:
                point.y += _eps
            if point.y > B.y or point.y < A.y or point.x > max(A.x, B.x):
                continue
            if point.x < min(A.x, B.x):
                inside = not inside
                continue
        return inside


q = Polygon([Point(20, 10),
             Point(50, 125),
             Point(125, 90),
             Point(150, 10)])

# Test 1: Point inside of polygon
p1 = Point(75, 50)
print("P1 inside polygon: " + str(q.contains(p1)))

# Test 2: Point outside of polygon
p2 = Point(200, 50)
print("P2 inside polygon: " + str(q.contains(p2)))

# Test 3: Point at same height as vertex
p3 = Point(35, 90)
print("P3 inside polygon: " + str(q.contains(p3)))

# Test 4: Point on bottom line of polygon
p4 = Point(50, 10)
print("P4 inside polygon: " + str(q.contains(p4)))

