import numpy
import math
import sys
from prog_3_functions import *

if (len(sys.argv) != 5):
	print("The command format should be: python ICP_matching.py Problem3-BodyA.txt Problem3-BodyB.txt PA3-X-ddddd-SampleReadingsTest.txt Problem3Mesh.sur")
	sys.exit(0)

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


# Use this to find Fa and Fb
index1 = int(sys.argv[3].index("PA3-"))
index2 = 0
try:
	index2 = int(sys.argv[3].index("-Unknown"))
except:
	index2 = int(sys.argv[3].index("-Sample"))
filename = sys.argv[3][index1:index2]

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
	d.append(Frame.vec_dot(Frame.frame_dot(F_B[i].inv_frame(), F_A[i]), a_tip).tolist())
sample_readings.close()

mesh_data = open(sys.argv[4])
n_vertices = int(mesh_data.readline().strip())
vertices = []
triangles = []
for i in range(n_vertices):
	current_vertices = mesh_data.readline().split()
	x, y, z = float(current_vertices[0].strip()), float(current_vertices[1].strip()), float(current_vertices[2].strip())
	vertices.append([x, y, z])
n_indices = int(mesh_data.readline().strip())
for i in range(n_indices):
	current_indices = mesh_data.readline().split()
	i_1, i_2, i_3 = int(current_indices[0].strip()), int(current_indices[1].strip()), int(current_indices[2].strip())
	triangles.append([i_1, i_2, i_3])
mesh_data.close()

# FOR PROG 3: s = d
s = d
c = []
for point in s:
	closest_point = None
	closest_distance = None
	for t in triangles:
		triangle = [vertices[t[0]], vertices[t[1]], vertices[t[2]]]
		closest_point_on_t = closest_point_on_triangle(point[0], triangle)
		distance = find_distance(point, closest_point_on_t)
		if (closest_point is None or distance < closest_distance):
			closest_point = closest_point_on_t
			closest_distance = distance
	c.append(closest_point.tolist())

################################################
### Final output
################################################
output = open("OUTPUT/" + filename + "-Output.txt", 'w')
output.write(str(len(c)) + " " + filename + "-Output.txt\n")
# Print to standard out and also write to file
for i in range(n_samples):
	output.write("%.2f" % d[i][0][0] + " " + "%.2f" % d[i][0][1] + " " + "%.2f" % d[i][0][2] + "\t%.2f" % c[i][0] + " " + "%.2f" % c[i][1] + " " + "%.2f" % c[i][2] + "\t%.3f" % find_distance(d[i][0], c[i]) + "\n")
output.close()