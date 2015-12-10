
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
    5. Run ICP again on the new mesh
    6. Go back to step 2 using the newly generated transformed sample points
"""

#Functions that I think will be necessary

#Computes a new mesh given the lambdas
#Input: New Set of Lambdas, Atlas
#Output: A new set of vertices (by combining the atlases)
def computeMesh(lambdas, atlas):
    return None
    
#Computes the set of q values for a given point given its triangle index and barycentric coordinates
#Input: triangle index (integer), barycentric coordinates (set of 3 floats), atlas
#Output: set of points (q values for every mode in atlas)
def computeQValues(index, coordinates, atlas):
    return None
    
#Solve Least Squares
#Input: Sample Points (set of points), Q values (set of sets of points)
#Output: Lambda Values (set of floats)
def leastSquares(samplePoints, qPoints):
    return None
    