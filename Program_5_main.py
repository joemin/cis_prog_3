import numpy
import math
import sys
import copy
from prog_3_functions import *
from kdtree import *
from modulated_code import *
from deform_reg import *
from Queue import Queue


if (len(sys.argv) != 6):
	print("The command format should be: python ICP_matching.py Problem5-BodyA.txt Problem5-BodyB.txt PA5-X-ddddd-SampleReadingsTest.txt Problem5Mesh.sur Problem5Modes.txt")
	sys.exit(0)

n_samples, d, vertices, triangle_indices, boxes, filename, atlas, lambdas = get_input(sys.argv)
s = d

# print(vertices[:10])

# Make KD tree
# Compute closest points on current mesh (use s to get c)
# Calculate q, then lambdas, then new mesh.
# Repeat
for i in range(10):
	print i
	root_box = construct_tree(boxes)
	s, c, closest_indices = converge_closest_points_on_mesh(s, root_box)
	q = get_all_q(c, vertices, closest_indices, len(atlas))
	lambdas = leastSquares(numpy.array(s), numpy.array(q))
	print (lambdas)
	vertices = computeMesh(numpy.array(lambdas), numpy.array(atlas))
	boxes = new_boxes(vertices, triangle_indices)



print_output(filename, n_samples, s, c)