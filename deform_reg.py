
"""
Rough Code Outline:
    1. First run Prog4 to generate the intial F_reg and s and c data sets
    2. Find the corresponding q set
        a. This is a set of sample points for every mesh in the atlas 
        b. You can compute these by getting the barycentric coordinates of the point in the triangle in the original mesh
        c. Then you simply use the same barycentric coordinates on the same triangle in the other meshes
    3. Once you have the q set solve the least squares problem s = q (0) + sum q(n) from 1 to N
        a. To do this you set up a system AX = B
        b. X is the lambdas
        c. A is the q values for the meshes that are not the current mesh!
        d. B is the sample point - q_0
    4. Use the new lambdas to create an updated "best guess" mesh
        a. Find set c (best guess points) on the update (Might not need to do this?)
    5. Run ICP again onthe new mesh
        a. Reconstruct KD Tree
    6. Go back to step 2 using the newly generated transformed sample points
"""

import numpy
import sys
from math import sqrt


#Computes a new mesh given the lambdas
#Input: New numpy array of Lambdas, Atlas (which should be an array of numpy arrays)
       #NOTE: The zeroth entry of the lambdas array is ignored since we correspond the index of lambda with the index of modes in the atlas
#Output: A new set of vertices (by combining the atlases)
def computeMesh(lambdas, atlas):
    newMesh = numpy.copy(atlas[0])
    for i in range(1,len(atlas)):
        newMesh = newMesh + lambdas[i] * atlas[i]
    return newMesh


#Computes the set of q values for a given point given its triangle index and barycentric coordinates
#Input: triangle index (integer), barycentric coordinates (set of 3 floats), atlas
#Output: set of points (q values for every mode in atlas)
def computeQValues(index, coordinates, atlas):
    q = []
    for mode in atlas:
        q.append(mode[index][0] * coordinates[0] + mode[index][1] * coordinates[1] + mode[index][2]*coordinates[2])
    return numpy.array(q)
        
    
#Solve Least Squares
#General idea is Sk - q0 = lambda1*q1 + lambda2*q2 ....
#Input: Sample Points (set of points), Q values (set of sets of points). qPoints should have which mode that set of q points is part of as its top index, then the point as the second index, then the axis (i.e. x, y, or z) as the third index
#Output: Lambda Values (set of floats)
def leastSquares(samplePoints, qPoints):
    b = numpy.reshape(samplePoints - qPoints[0], len(samplePoints) * 3)
    A = []
    for q in qPoints[1:]:
        A.append(numpy.reshape(q, len(q) * 3))
    A = numpy.array(A).T
    b = b.T
    # print numpy.array(A)
    l = numpy.array(numpy.linalg.lstsq(A, b)[0])
    return l

def get_all_q(c, mesh, lambdas, closest_indices):
    num_samples = len(c)
    num_modes = len(mesh)
    q = []

    for i in range(num_samples):
        q.append([])
        index_a = closest_indices[i][0]
        # print("HERE")
        # print(closest_indices[0])
        index_b = closest_indices[i][1]
        index_c = closest_indices[i][2]
        m_s = mesh[index_a]
        m_t = mesh[index_b]
        m_u = mesh[index_c]
        # # print "m_s", m_s
        # for j in range(num_modes):
        #     if not (j == 0):
        #         if i == 43 or i == 42:
        #             print j, atlas[j][index_b], lambdas[j]
        #             print "m_t", m_t, "m_s", m_s
        #             print (m_t + lambdas[j]*numpy.array(atlas[j][index_b])).tolist()
        #         m_s = (m_s + lambdas[j]*numpy.array(atlas[j][index_a])).tolist()
        #         m_t = (m_t + lambdas[j]*numpy.array(atlas[j][index_b])).tolist()
        #         m_u = (m_u + lambdas[j]*numpy.array(atlas[j][index_c])).tolist()
                # print atlas[j][index_a], lambdas[j]
            # else:
        triangle = [m_s, m_t, m_u]
        # print(triangle)
        bary_coords = numpy.array(barycentric_coordinates(c[i], triangle))
        for j in range(num_modes):
            if (j == 0):
                q.append(mesh[i])
            else:
                q_x = bary_coords[0]*mesh[index_a][0] + bary_coords[1]*mesh[index_b][0] + bary_coords[2]*mesh[index_c][0]
                q_y = bary_coords[0]*mesh[index_a][1] + bary_coords[1]*mesh[index_b][1] + bary_coords[2]*mesh[index_c][1]
                q_z = bary_coords[0]*mesh[index_a][2] + bary_coords[1]*mesh[index_b][2] + bary_coords[2]*mesh[index_c][2]
                # current_q = computeQValues()
                q[i].append([q_x, q_y, q_z])

# Calculate the barycentric coordinates of a given point in a given triangle
# Input: a triangle, and a point inside that triangle
# Output: The array of weights for each vertex
def barycentric_coordinates(point, triangle):
    # print(triangle)
    pab = [point, triangle[0], triangle[1]]
    pac = [point, triangle[0], triangle[2]]
    pbc = [point, triangle[1], triangle[2]]
    # print(pab)
    # print(pac)
    # print(pbc)
    area_abc = triangle_area(triangle)
    # print(area_abc)
    area_pab = triangle_area(pab)
    area_pac = triangle_area(pac)
    area_pbc = triangle_area(pbc)
    bary_coords = []
    alpha = area_pbc/area_abc
    beta = area_pac/area_abc
    gamma = area_pab/area_abc
    # print alpha, beta, gamma
    bary_coords.append(alpha)
    bary_coords.append(beta)
    bary_coords.append(gamma)
    return bary_coords

# Calculate the area of a given triangle
# Input: The triangle as an array of points
# Output: The area
def triangle_area(triangle):
    a = vector_length(triangle[0], triangle[1])
    b = vector_length(triangle[0], triangle[2])
    c = vector_length(triangle[1], triangle[2])
    s = (a + b + c)/2.0
    # print(s)
    if abs(s*(s-a)*(s-b)*(s-c)) < .00001:
        return 0
    return sqrt(s*(s-a)*(s-b)*(s-c))

# Calculate the euclidean distance between two points
# Input: Two points
# Output: The distance between them
def vector_length(point1, point2):
    p1 = numpy.array(point1)
    p2 = [0, 0, 0]
    try:
        p2 = numpy.array(point2)
    except:
        print(point2)
        sys.exit()
    return numpy.linalg.norm(p1-p2).tolist()


# barycentric_coordinates([0, 1.0/3.0, 0], [[-.5, 0, 0], [0, 1, 0], [.5, 0, 0]])
# q0 = numpy.array([[ 0,0,0],[1,1,0],[2,2,0]])
# q1 = numpy.array([[ 0,0,0],[1,2,0],[2,3,0]])
# q2 = numpy.array([[-1,0,0],[0,1,0],[3,2,0]])
# q = numpy.array([q0,q1,q2])
# s = numpy.array([[-1,0,0],[0,2,0],[3,3,0]])

# #A = numpy.concatenate([q1, q2], axis=1)
# #print A

# print leastSquares(s, q)

    