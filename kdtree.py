class BoundingBox:
    def __init__(self, triangle):
        self.upper, self.lower = self.createBoundingBox(triangle)
        self.triangle = triangle
        self.leaf = True
        self.subBoxes = []
    def __init__(self, lower, upper):
        self.upper = upper
        self.lower = lower
        self.triangle = None
        self.leaf = False
        self.subBoxes = []
        
    def createBoundingBox(triangle):
        return None

    """def findClosestTriangle(point, curBest, curBestTriangle):
        if self.leaf:
            return self.Triangle
        if (not curBestPoint is None) and
           (curBest.x + curBestPoint.x > self.upper.x) or (curBest.x - curBestPoint.x < self.lower.x) or
           (curBest.y + curBestPoint.y > self.upper.y) or (curBest.y - curBestPoint.y < self.upper.y) or
           (curBest.z + curBestPoint.z > self.upper.z) or (curBest.z - curBestPoint.z < self.upper.z):
               return None, None
        else:
            thisClosestDist = None
            thisClosestTriangle 
            for box in subBoxes:
                return subBoxes.findClosestTriangle"""

class Point:
    def __init__(self, x,y,z):
        self.x = x
        self.y = y
        self.z = z

def pointToTriangle(t, p):
    d = (p.x - t.x)**2 + (p.y - t.y)**2 + (p.z-t.z)**2
    return d

def findClosestTriangle(point, rootBox):
    closestTriangle = None
    dist = None
    stack= []
    stack.append(rootBox)
    while not len(stack) == 0:
        print("iterating")
        box = stack.pop()
        if (not closestTriangle is None) and ((point.x + dist < box.lower.x) or (point.x - dist > box.upper.x) or (point.y + dist < box.lower.y) or (point.y - dist > box.upper.y) or (point.z + dist < box.lower.z) or (point.z - dist > box.upper.z)):
               continue
        print ("past intersect check")
        if (box.leaf):
             d = pointToTriangle(box.triangle, point)
             if ((d < dist) or (dist is None)):
                 closestTriangle = box.triangle
                 dist = d
        else:
            for child in box.subBoxes:
                stack.append(child)
    return closestTriangle


box = BoundingBox(Point(0,0,0), Point(5,5,0))
box2 = BoundingBox(Point(0,0,0), Point(3,5,0))
box2.leaf = True
box3 = BoundingBox(Point(3,0,0), Point(5,5,0))
box3.leaf = True
box.subBoxes.append(box2)
box.subBoxes.append(box3)
box2.triangle = Point(1,3,0)
box3.triangle = Point(3,2,0)
point = Point(1,1,1)

print findClosestTriangle(point, box).z

"""dist = 1
if ((point.x + dist < box.lower.x) or (point.x - dist > box.upper.x) or (point.y + dist < box.lower.y) or (point.y - dist > box.upper.y) or (point.z + dist < box.lower.z) or (point.z - dist > box.upper.z)):
    print "No intersection"
else:
    print "Intersection" """
