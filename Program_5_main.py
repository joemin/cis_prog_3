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

# Make KD tree
# Compute closest points on current mesh (use s to get c)
# Calculate q, then lambdas, then new mesh.
# Repeat
for i in range(5):
	root_box = construct_tree(boxes)
	s, c, closest_triangles = converge_closest_points_on_mesh(s, root_box)
	print closest_triangles[:10]
	q = get_all_q(c, atlas, lambdas, triangle_indices)
	lambdas = leastSquares(c, q)
	vertices = computeMesh(lambdas, atlas)



print_output(filename, n_samples, s, c)