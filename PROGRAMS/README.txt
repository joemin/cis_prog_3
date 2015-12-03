Overall, our program should be run as follows:
python ICP_matching_kdtree.py /path-to-data/Problem4-BodyA.txt /path-to-data/Problem4-BodyB.txt /path-to-data/PA4-X-ddddddd-SampleReadingsTest.txt /path-to-data/Problem4MeshFile.sur
Where X is the dataset letter, and ddddddd should be replaced by either "Debug" or "Unknown".


ICP_matching_kdtree.py
This is our main script that handles the reading of input files and then calls functions from the other files to construct and search through a KD tree to find closest points. It does this for a number of iterations then outputs to a folder called OUTPUT.

prog_3_functions.py
This has all of our functions from programming assignment 3, including but not limited to a frame transformation class, finding the closest point on a triangle to a given point, and finding the Euclidean distance between points.

kdtree.py
This has all of our new classes and functions including but not limited to the construction of a KD tree, the creation of a bounding box for a triangle, and a search algorithm for the KD tree.
