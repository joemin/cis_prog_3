import numpy
import math
import sys
import copy
from prog_3_functions import *
from kdtree import *
from Queue import Queue


if (len(sys.argv) != 5):
	print("The command format should be: python ICP_matching.py Problem3-BodyA.txt Problem3-BodyB.txt PA3-X-ddddd-SampleReadingsTest.txt Problem3Mesh.sur")
	sys.exit(0)

# First we get a cloud of data for rigid body A in optical coordinates
rigid_a_data = open(sys.argv[1])
a_first_line = rigid_a_data.readline().split()
n_a_markers = int(a_first_line[0].strip())
a_led_markers = []
for i in range(n_a_markers):
	current_marker = rigid_a_data.readline().split()
	x, y, z = float(current_marker[0].strip()), float(current_marker[1].strip()), float(current_marker[2].strip())
	a_led_markers.append([x, y, z])
a_tip_line = rigid_a_data.readline().split()
a_tip = [float(a_tip_line[0].strip()), float(a_tip_line[1].strip()), float(a_tip_line[2].strip())]
rigid_a_data.close()


# Then we get a cloud of data for rigid body B in optical coordinates
rigid_b_data = open(sys.argv[2])
b_first_line = rigid_b_data.readline().split()
n_b_markers = int(b_first_line[0].strip())
b_led_markers = []
for i in range(n_b_markers):
	current_marker = rigid_b_data.readline().split()
	x, y, z = float(current_marker[0].strip()), float(current_marker[1].strip()), float(current_marker[2].strip())
	b_led_markers.append([x, y, z])
b_tip_line = rigid_b_data.readline().split()
b_tip = [float(b_tip_line[0].strip()), float(b_tip_line[1].strip()), float(b_tip_line[2].strip())]
rigid_b_data.close()


# This lets us set up what the name of the output file will be
index1 = 0
try:
	index1 = int(sys.argv[3].index("PA3-"))
except:
	index1 = int(sys.argv[3].index("PA4-"))
index2 = 0
try:
	index2 = int(sys.argv[3].index("-Unknown"))
except:
	index2 = int(sys.argv[3].index("-Sample"))
filename = sys.argv[3][index1:index2]

# Use this to find Fa and Fb
sample_readings = open(sys.argv[3])
sample_readings_first_line = sample_readings.readline().split(",")
n_s = int(sample_readings_first_line[0].strip())
n_a = n_a_markers
n_b = n_b_markers
n_d = n_s - n_a - n_b
n_samples = int(sample_readings_first_line[1].strip())
F_A = []
F_B = []
d = []
for i in range(n_samples):
	a_current_markers = []
	b_current_markers = []
	for j in range(n_a):
		current_marker = sample_readings.readline().split(",")
		x, y, z = float(current_marker[0].strip()), float(current_marker[1].strip()), float(current_marker[2].strip())
		a_current_markers.append([x, y, z])
	for j in range(n_b):
		current_marker = sample_readings.readline().split(",")
		x, y, z = float(current_marker[0].strip()), float(current_marker[1].strip()), float(current_marker[2].strip())
		b_current_markers.append([x, y, z])
	for j in range(n_d):
		sample_readings.readline()
	F_A.append(get_frame(numpy.array(a_current_markers).T, numpy.array(a_led_markers).T))
	F_B.append(get_frame(numpy.array(b_current_markers).T, numpy.array(b_led_markers).T))
	d.append(Frame.vec_dot(Frame.frame_dot(F_B[i].inv_frame(), F_A[i]), a_tip).tolist()[0])
sample_readings.close()


# Read in the mesh data
mesh_data = open(sys.argv[4])
n_vertices = int(mesh_data.readline().strip())
vertices = []
triangles = []
boxes = []
for i in range(n_vertices):
	current_vertices = mesh_data.readline().split()
	x, y, z = float(current_vertices[0].strip()), float(current_vertices[1].strip()), float(current_vertices[2].strip())
	vertices.append([x, y, z])
n_indices = int(mesh_data.readline().strip())
for i in range(n_indices):
	current_indices = mesh_data.readline().split()
	i_1, i_2, i_3 = int(current_indices[0].strip()), int(current_indices[1].strip()), int(current_indices[2].strip())
	triangles.append([i_1, i_2, i_3])
	triangle = [vertices[triangles[i][0]], vertices[triangles[i][1]], vertices[triangles[i][2]]]
	boxes.append(makeBoundingBox(triangle))
mesh_data.close()


# Construct the KD tree
root_box = constructTree(boxes)
count = 0
q = Queue()
q.put(root_box)
while not q.empty():
	node = q.get()
	if (node.leaf):
		count=count+1
	else:
		for box in node.subBoxes:
			q.put(box)


# Make initial guess: s = d
s = d
mean_distances = []
done = False
i = 0
change_mean_diff = 999
# Continue to register s points until they are as close as possible to points on the mesh
while not done:
	print i
	c = []
	for point in s:
		closest_triangle = findClosestTriangle(point, root_box) #kdtree method
		closest_point = closest_point_on_triangle(point, closest_triangle)
		c.append(closest_point.tolist())

	diffs = []
	for j in range(len(s)):
		diffs.append(find_distance(s[j], c[j]))
	mean_distance = numpy.mean(diffs)
	mean_distances.append(mean_distance)
	std = numpy.std(diffs)
	# Exclude data points by building weighted matrices
	weighted_s = []
	weighted_c = []
	for j in range(len(diffs)):
		if (float(diffs[j]) > (float(mean_distance) + 4*float(std))):
			weighted_s.append([0, 0, 0])
			weighted_c.append([0, 0, 0])
		else:
			weighted_s.append(s[j])
			weighted_c.append(c[j])
	if i > 0:
		change_mean_diff = mean_distances[i-1] - mean_distances[i]

	# Check to see if we can be done
	if change_mean_diff < .000001 or i > 100 or mean_distance < .001:
		done = True

	# Calculate the new f_reg using the weighted matrices
	f_reg = get_frame(numpy.array(weighted_c).T, numpy.array(weighted_s).T)
	new_s = numpy.array(Frame.cloud_dot(f_reg, s))
	s = new_s
	i = i+1

################################################
### Final output
################################################
output = open("OUTPUT/" + filename + "-Output.txt", 'w')
output.write(str(len(c)) + " " + filename + "-Output.txt\n")
# Print to standard out and also write to file
for i in range(n_samples):
	output.write("%.2f" % s[i][0] + " " + "%.2f" % s[i][1] + " " + "%.2f" % s[i][2] + "\t%.2f" % c[i][0] + " " + "%.2f" % c[i][1] + " " + "%.2f" % c[i][2] + "\t%.3f" % find_distance(s[i], c[i]) + "\n")
output.close()