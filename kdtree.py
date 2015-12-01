import numpy
from Queue import Queue
from prog_3_functions import *

class BoundingBox:
    def __init__(self, lower, upper):
        self.upper = upper
        self.lower = lower
        self.triangle = None
        self.leaf = False
        self.subBoxes = []        
    def createBoundingBox(triangle):
        return None
    def __str__(self):
        return str(self.lower) + " " + str(self.upper)

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
    def __str__(self):
        return str(self.x) + "," + str(self.y) + "," + str(self.z)

#Finds the median for a list of boxes x,y,or z coordinate
#At the moment it finds the median of the upper coordinates
def findMedian(boxes, coord, upper):   #coord must be either 0,1, or 2. 0 = x, 1 = y, 2 = z
    coords = []
    if upper:
        for box in boxes:
            coords.append(box.upper[coord])
    else:
        for box in boxes:
            coords.append(box.lower[coord])
    return numpy.median(coords)

#Splits on the upper coordinate at the moment
def splitBox(boxes, median, coord, upper):
    l1 = []
    l2 = []
    if upper:
        for box in boxes:
            if box.upper[coord] < median:
                l1.append(box)
            else:
                l2.append(box)
    else:
        for box in boxes:
            if box.lower[coord] < median:
                l1.append(box)
            else:
                l2.append(box)
    return l1, l2
    
def findMinMax(triangle, coord):
    mi = triangle[0][coord]
    ma = triangle[0][coord]
    for p in triangle:
        if p[coord] > ma:
            ma = p[coord]
        if p[coord] < mi:
            mi = p[coord]
    return ma, mi

#Param triangle is a list of three points 
def makeBoundingBox(triangle):
    maxX, minX = findMinMax(triangle, 0)
    maxY, minY = findMinMax(triangle, 1)
    maxZ, minZ = findMinMax(triangle, 2)
    b = BoundingBox([minX, minY, minZ], [maxX, maxY, maxZ])
    b.triangle = triangle
    b.leaf = True
    return b
    


def makeBox(boxes): #Takes a list of bounding boxes and gives a tight bounding box for them
    if len(boxes) is 1:
        return boxes[0]
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
    p2 = closest_point_on_triangle(p, t)
    return find_distance(p, p2)

def boxesIntersect(box1, box2):
    if (box1.upper[0] < box2.lower[0]):
        return False
    if (box1.upper[1] < box2.lower[1]):
        return False
    if (box1.upper[2] < box2.lower[2]):
        return False
    if (box1.lower[0] > box2.upper[0]):
        return False
    if (box1.lower[1] > box2.upper[1]):
        return False
    if (box1.lower[2] > box2.upper[2]):
        return False
    return True

def boxesIntersect2(box1, box2):
    if (box1.upper[0] < box2.lower[0]):
        print "a"
        return False
    if (box1.upper[1] < box2.lower[1]):
        return False
        print "b"
    if (box1.upper[2] < box2.lower[2]):
        return False
        print "c"
    if (box1.lower[0] > box2.upper[0]):
        return False
        print "d"
    if (box1.lower[1] > box2.upper[1]):
        return False
        print "e"
    if (box1.lower[2] > box2.upper[2]):
        return False
        print "f"
    return True

def findClosestTriangle(point, rootBox):        #Note this only finds closest box at the moment
    closestTriangle = None
    dist = None
    stack= []
    stack.append(rootBox)
    # print(pointIn)
    # point = Point(pointIn[0][0], pointIn[0][1], pointIn[0][2])
    while not len(stack) == 0:
        box = stack.pop()
        if not dist is None:
            newBox = BoundingBox([point[0] - dist, point[1] - dist, point[2] - dist], [point[0] + dist, point[1] + dist, point[2] + dist])
        if (not closestTriangle is None) and not boxesIntersect(box, newBox):
              if (box.leaf and dist < 1):
                d = pointToTriangle(box.triangle, point)
                # if (d<.1):
                    # print box
                    # printTriangle(closestTriangle)
                    # print newBox
                    # printTriangle(box.triangle)
                    # print d
              continue
        if (box.leaf):
             d = pointToTriangle(box.triangle, point)
             if ((d < dist) or (dist is None)):
                 closestTriangle = box.triangle
                 dist = d
        else:
            for child in box.subBoxes:
                stack.append(child)
    return closestTriangle

def printTriangle(triangle):
    if triangle is None:
        return
    print str(triangle[0]) + "," + str(triangle[1]) + "," + str(triangle[2])

# Param boxes is a list
def constructTree(boxes):
    boxQueue = Queue()
    listQueue = Queue()
    b = makeBox(boxes)
    b.coordSplit = 0
    boxQueue.put(b)
    listQueue.put(boxes)
    while not boxQueue.empty():
        # print "\n"
        # print boxQueue.qsize()
        curBox = boxQueue.get()
        curList = listQueue.get()
        if curBox.leaf or len(curList) is 1: #Potentially might need to pop from listqueue
            curBox.leaf = True
            continue
        else:
            m = findMedian(curList, curBox.coordSplit, True)
            l1,l2 = splitBox(curList, m, curBox.coordSplit, True)
            if (len(l1) is 0) or (len(l2) is 0):
                # print "Using Lower instead"
                m = findMedian(curList, curBox.coordSplit, False)
                l1,l2 = splitBox(curList, m, curBox.coordSplit, False)
            if ((len(l1) is 0) or (len(l2) is 0)) and ((len(l2) is 2) or (len(l2) is 3) or (len(l1) is 2) or (len(l1) is 3)):   #Potentially is making the wrong bounds for the parent box
                for box in l1:
                    box.leaf = True
                    curBox.subBoxes.append(box)
                for box in l2:
                    box.leaf = True
                    curBox.subBoxes.append(box)
                continue
            # print m, curBox.coordSplit
            # for box in l2:
             # print box
            #     # printTriangle(box.triangle)
            # print "\n"
            c = (curBox.coordSplit + 1) % 3
            if (len(l1) > 0):#Can be zero if all the boxes lie in the same plane (i.e. everything is 0 in the z coordinate)
                box1 = makeBox(l1)
                box1.coordSplit = c
                curBox.subBoxes.append(box1)
                listQueue.put(l1)
                boxQueue.put(box1)
            if (len(l2) > 0):
                box2 = makeBox(l2)
                box2.coordSplit = c
                curBox.subBoxes.append(box2)
                listQueue.put(l2)
                boxQueue.put(box2)
        # print boxQueue.qsize()
    return b
            

# b1 = BoundingBox([-12.513461, -27.024874, -14.898345], [-16.716616, -29.941799, -19.676682])
# b1.leaf = True
# b2 = BoundingBox([-10.566681, -27.024874, -14.898345], [-12.763243, -29.941799, -19.676682])
# b2.leaf = True
# b3 = BoundingBox([-12.513461, -26.910938, -12.595299], [-16.716616, -29.685785, -16.313026])
# b3.leaf = True

# constructTree([b1, b2, b3])

# print makeBoundingBox([[2.190276, -7.224511, 58.876591],[1.744815, -7.125705, 55.080135],[4.860498, -7.415166, 54.500889]])



"""box1 = BoundingBox([1,10,0], [3,12,0])
box1.leaf = True
box1.triangle = Point(2, 11, 0)
box2 = BoundingBox([3,4,0], [8,8,0])
box2.leaf = True
box2.triangle = Point(5, 6, 0)
box3 = BoundingBox([10,20,0], [13,22,0])
box3.leaf = True
box3.triangle = Point(12, 21, 0)
box4 = BoundingBox([20,12,0], [25,17,0])
box4.leaf = True
box4.triangle = Point(22, 15, 0)
box5 = BoundingBox([6,9,0], [11,15,0])
box5.leaf = True
box5.triangle = Point(8,12,0)
box = BoundingBox([0,0,0],[30,30,0])
box.subBoxes = [box1, box2, box3, box4, box5]

test = [box4, box3]

#a,b = splitBox(test, findMedian(box.subBoxes, 0), 0)

#c = makeBox(a)

d = constructTree(box.subBoxes)

point = Point(15,21, 0)

print findClosestTriangle(point, d)"""

"""dist = 1
if ((point.x + dist < box.lower.x) or (point.x - dist > box.upper.x) or (point.y + dist < box.lower.y) or (point.y - dist > box.upper.y) or (point.z + dist < box.lower.z) or (point.z - dist > box.upper.z)):
    print "No intersection"
else:
    print "Intersection" """













