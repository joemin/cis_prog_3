import math
import numpy

_EPS = numpy.finfo(float).eps * 4.0

# Performs a cloud to cloud registration
def get_frame(cloud1, cloud2):
    cloud1 = numpy.array(cloud1)
    cloud1_original = cloud1
    cloud2 = numpy.array(cloud2)
    cloud2_original = cloud2
    cloud1x, cloud1y, cloud1z = numpy.sum(cloud1, axis=1)
    centroid_1 = numpy.array([[cloud1x], [cloud1y], [cloud1z]])/len(cloud1[0])
    cloud1 = cloud1 - centroid_1 #center around origin
    cloud2x, cloud2y, cloud2z = numpy.sum(cloud2, axis=1)
    centroid_2 = numpy.array([[cloud2x], [cloud2y], [cloud2z]])/len(cloud2[0])
    cloud2 = cloud2 - centroid_2 #center around origin
    xx, yy, zz = numpy.sum(cloud1 * cloud2, axis=1)
    xy, yz, zx = numpy.sum(cloud1 * numpy.roll(cloud2, -1, axis=0), axis=1)
    xz, yx, zy = numpy.sum(cloud1 * numpy.roll(cloud2, -2, axis=0), axis=1)
    N = [[xx+yy+zz, yz-zy,      zx-xz,      xy-yx],
            [yz-zy,    xx-yy-zz, xy+yx,      zx+xz],
            [zx-xz,    xy+yx,    yy-xx-zz, yz+zy],
            [xy-yx,    zx+xz,    yz+zy,    zz-xx-yy]]
    w1, v1 = numpy.linalg.eig(N)
    max_index = numpy.argmax(w1)
    q = v1[:,max_index]
    n = numpy.dot(q, q)
    if n < _EPS:
        R = numpy.identity(3)
    else:
        rot_matrix = [[math.pow(q[0], 2) + math.pow(q[1], 2) - math.pow(q[2], 2) - math.pow(q[3], 2), 2*(q[1]*q[2] - q[0]*q[3]), 2*(q[1]*q[3] + q[0]*q[2])],
        [2*(q[1]*q[2] + q[0]*q[3]), math.pow(q[0], 2) - math.pow(q[1], 2) + math.pow(q[2], 2) - math.pow(q[3], 2), 2*(q[2]*q[3] - q[0]*q[1])],
        [2*(q[1]*q[3] - q[0]*q[2]), 2*(q[2]*q[3] + q[0]*q[1]), math.pow(q[0], 2) - math.pow(q[1], 2) - math.pow(q[2], 2) + math.pow(q[3], 2)]]
        R = numpy.array(rot_matrix)
    t = numpy.dot(R.T, centroid_2) - centroid_1
    return Frame(R.T, -t)

# A frame class that holds rotation and translation matrices
# It also has functions to perform registrations on vectors, other frames, and lists of points.
class Frame:
    def __init__(self, rotation = None, translation = None):
        if rotation is None:
            self.rotation = [numpy.identity(3)] #the identity matrix should be default
        else:
            self.rotation = numpy.array(rotation)
        if translation is None:
            self.translation = numpy.array([0, 0, 0]) #default translation should be zero
        else:
            self.translation = numpy.array(translation)
    def get_rot(self):
        return self.rotation
    def get_trans(self):
        return self.translation
    def get_inv_rot(self):
        return numpy.linalg.inv(numpy.array(self.rotation))
    def get_inv_trans(self):
        return numpy.dot(-1*numpy.array(self.get_inv_rot()), numpy.array(self.translation))
    def inv_frame(self):
        return Frame(self.get_inv_rot(), self.get_inv_trans())
    def frame_dot(frame_1, frame_2):
        new_rot = numpy.dot(numpy.array(frame_1.get_rot()), numpy.array(frame_2.get_rot()))
        new_trans = numpy.dot(numpy.array(frame_1.get_rot()), numpy.array(frame_2.get_trans())) + numpy.array(frame_1.get_trans())
        return Frame(new_rot, new_trans)
    def vec_dot(frame, vector):
        return numpy.dot(numpy.array(frame.get_rot()), numpy.array(vector)) + numpy.array(frame.get_trans()).T
    def cloud_dot(frame, cloud):
        new_cloud = []
        for point in cloud:
            new_point = Frame.vec_dot(frame, numpy.array(point).T)
            new_cloud.append(new_point[0].tolist())
        return new_cloud

# Given a triangle, this returns the associated plane given by a point and the normal to that plane
def get_plane(triangle):
    apex = numpy.array(triangle[0])
    vec_1 = numpy.array(triangle[1]) - numpy.array(triangle[0])
    vec_2 = numpy.array(triangle[2]) - numpy.array(triangle[0])
    vec_norm = get_unit_vec(numpy.cross(vec_1, vec_2))
    return [apex, vec_norm]

# Returns the unit vector of a given vector
def get_unit_vec(vector):
    magnitude = math.sqrt(numpy.dot(numpy.array(vector), numpy.array(vector).T))
    return numpy.array(vector)/magnitude

# Gets the orthogonal projection of a vector onto a plane
def get_ortho_proj(vector, plane):
    return numpy.array(vector) - numpy.dot(numpy.array(vector) - numpy.array(plane[0]), numpy.array(plane[1])) * numpy.array(plane[1])

# Gets the projection of a point in a plane, but outside of a triangle, onto the triangle
def get_proj_on_line(point, vert_1, vert_2):
    c, p, q = numpy.array(point), numpy.array(vert_1), numpy.array(vert_2)
    lam_top = numpy.dot(c-p, q-p)
    lam_bot = numpy.dot(q-p, q-p)
    lam = float(lam_top)/float(lam_bot)
    lam_star = max(0.0, min(lam, 1.0))
    # print(lam_star)
    return p + lam_star*(q - p)

# Given a point and a triangle, this returns the closest point on that triangle
def closest_point_on_triangle(point, triangle):
    p, q, r = numpy.array(triangle[0]), numpy.array(triangle[1]), numpy.array(triangle[2])
    c = numpy.array(get_ortho_proj(point, get_plane(triangle)))
    # # # # # # # # # # # # # # # # #
    # Solve: lam(q-p) + mu(r-p) = c-p
    # # # # # # # # # # # # # # # # #
    lam, mu = numpy.linalg.solve(numpy.array([[q[0]-p[0], r[0]-p[0]], [q[1]-p[1], r[1]-p[1]]]), numpy.array([c[0]-p[0], c[1]-p[1]]))
    if (lam >= 0 and mu >=0 and lam + mu < 1):
        return p + lam*(q-p) + mu*(r-p)
        # return c
    elif (lam < 0 and mu < 0 and lam + mu <= 0):
        return p
    elif (lam < 0 and mu < 1):
        return get_proj_on_line(c, r, p)
    elif (mu < 0 and lam < 1):
        return get_proj_on_line(c, q, p)
    elif (lam < 0 and mu >= 1):
        return r
    elif (mu < 0 and lam >= 1):
        return q
    else:
        return get_proj_on_line(c, r, q)

# Returns the Euclidean distance between two points
def find_distance(point_1, point_2):
    p_1, p_2 = numpy.array(point_1), numpy.array(point_2)
    return numpy.linalg.norm(p_2 - p_1)