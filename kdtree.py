import numpy

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

#Finds the median for a list of boxes x,y,or z coordinate
#At the moment it finds the median of the upper coordinates
def findMedian(boxes, coord):   #coord must be either 0,1, or 2. 0 = x, 1 = y, 2 = z
    coords = []
    for box in boxes:
        coords.append(box.upper[coord])
    return numpy.median(coords)

#Splits on the upper coordinate at the moment
def splitBox(boxes, median, coord):
    l1 = []
    l2 = []
    for box in boxes:
        if box[coord] < median:
            l1.append(box)
        else:
            l2.append(box)
    return l1, l2


def makeBox(boxes): #Takes a list of bounding boxes and gives a tight bounding box for them
    maxes = []
    mins = []
    for coord in boxes[0].upper:    #Initialize the maxes and mins
        maxes.append(coord)
        mins.append(coord)
    for box in boxes:
        for i in range(3):
            if (maxes[i] < box.upper[i]):
                maxes[i] = box.upper[i]
            if (mins[i] > box.lower[i]):
                mins[i] = box.lower[i]
    return BoundingBox(mins, maxes)

def pointToTriangle(t, p):  #This actually just gives distance from point to point atm
    d = (p.x - t.x)**2 + (p.y - t.y)**2 + (p.z-t.z)**2
    return d

def findClosestTriangle(point, rootBox):        #Note this only finds closest box at the moment
    closestTriangle = None
    dist = None
    stack= []
    stack.append(rootBox)
    while not len(stack) == 0:
        print("iterating")
        box = stack.pop()
        if (not closestTriangle is None) and ((point.x + dist < box.lower[0]) or (point.x - dist > box.upper[0]) or (point.y + dist < box.lower[1]) or (point.y - dist > box.upper[1]) or (point.z + dist < box.lower[2]) or (point.z - dist > box.upper[2])):
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

def constructTree(boxes):
    boxQueue = Queue()
    listQueue = Queue()
    b = makeBox(boxes)
    b.coordSplit = 0
    boxQueue.put(b)
    listQueue.put(boxes)
    while not boxQueue.empty():
        curBox = boxQueue.get()
        if curBox.leaf: #Potentially might need to pop from listqueue
            continue
        else:
            curList = listQueue.get()
            m = findMedian(curList, curBox.coordSplit)
            l1,l2 = splitBox(curList, m, curBox.coordSplit)
            box1 = makeBox(l1)
            box2 = makeBox(l2)
            c = (curBox.coordSplit + 1) % 3
            box1.coordSplit = c
            box2.coordSplit = c
            curBox.subBoxes.append(box1)
            curBox.subBoxes.append(box2)
            listQueue.put(l1)
            listQueue.put(l2)
            boxQueue.put(box1)
            boxQueue.put(box2)
            
        


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
