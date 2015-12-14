
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


#Functions that I think will be necessary

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
    print numpy.array(A)
    l = numpy.array(numpy.linalg.lstsq(A, b)[0])
    return l
    
q0 = numpy.array([[ 0,0,0],[1,1,0],[2,2,0]])
q1 = numpy.array([[ 0,0,0],[1,2,0],[2,3,0]])
q2 = numpy.array([[-1,0,0],[0,1,0],[3,2,0]])
q = numpy.array([q0,q1,q2])
s = numpy.array([[-1,0,0],[0,2,0],[3,3,0]])

#A = numpy.concatenate([q1, q2], axis=1)
#print A

print leastSquares(s, q)

    