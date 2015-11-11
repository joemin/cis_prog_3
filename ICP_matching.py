import numpy
import math
import sys
from prog_3_functions import *

# if (len(sys.argv) != 4):
# 	print("The command format should be: ")
# 	sys.exit(0)

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
sample_readings = open(sys.argv[3])
sample_readings_first_line = sample_readings.readline().split(",")
n_s = int(sample_readings_first_line[0].strip())
# n_a = n_s/4
# n_b = n_s/4
n_a = n_a_markers
n_b = n_b_markers
n_d = n_s - n_a - n_b
n_samples = int(sample_readings_first_line[1].strip())
readings = []
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
	F_A.append(get_frame(numpy.array(a_led_markers).T, numpy.array(a_current_markers).T))
	F_B.append(get_frame(numpy.array(b_led_markers).T, numpy.array(b_current_markers).T))
	d.append(Frame.vec_dot(Frame.frame_dot(F_B[i].inv_frame(), F_A[i]), a_tip).tolist())
	# readings.append([a_current_markers, b_current_markers])
sample_readings.close()

# print(Frame.frame_dot(F_A[0], F_B[0]).get_rot())
# print(d[0])

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
print(s)
full_set = []
for point in s:
	closest_point = None
	closest_distance = None
	for t in triangles:
		# print(point, t)
		triangle = [vertices[t[0]], vertices[t[1]], vertices[t[2]]]
		closest_point_on_t = closest_point_on_triangle(point, triangle)
		distance = find_distance(point, closest_point_on_t)
		if (closest_point is None or distance < closest_distance):
			closest_point = closest_point_on_t
			closest_distance = distance
	full_set.append(closest_point.tolist())

# print(len(full_set), full_set)
