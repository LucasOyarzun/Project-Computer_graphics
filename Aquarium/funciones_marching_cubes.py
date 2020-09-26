import numpy as np
import basic_shapes as bs

# This is not a marching cube, it is a fast and simpler version.
def fast_marching_cube(X, Y, Z, scal_field, isosurface_value):
    dims = X.shape[0]-1, X.shape[1]-1, X.shape[2]-1
    voxels = np.zeros(shape=dims, dtype=bool)
    for i in range(1, X.shape[0]-1):
        for j in range(1, X.shape[1]-1):
            for k in range(1, X.shape[2]-1):
                # Tomamos desde i-1 hasta i+1, porque así analiza hasta el punto i
                # El slicing NO incluye el final.
                v_min = scal_field[i-1:i+1, j-1:j+1, k-1:k+1].min()
                v_max = scal_field[i-1:i+1, j-1:j+1, k-1:k+1].max()

                if v_min >= isosurface_value-2 and isosurface_value+2 >= v_max:
                    voxels[i,j,k] = True
                else:
                    voxels[i,j,k] = False

    return voxels

# This is not a marching cube, it is a fast and simpler version.
def fast_marching_cube_aqua(X, Y, Z, scal_field, isosurface_value):
    dims = X.shape[0]-1, X.shape[1]-1, X.shape[2]-1
    voxels = np.zeros(shape=dims, dtype=bool)
    for i in range(1, X.shape[0]-1):
        for j in range(1, X.shape[1]-1):
            for k in range(1, X.shape[2]-1):
                # Tomamos desde i-1 hasta i+1, porque así analiza hasta el punto i
                # El slicing NO incluye el final.
                v_min = scal_field[i-1:i+1, j-1:j+1, k-1:k+1].min()
                v_max = scal_field[i-1:i+1, j-1:j+1, k-1:k+1].max()

                voxels[i,j,k] = True

    return voxels


def createColorCube(i, j, k, X, Y, Z,r,g,b):
    l_x = X[i, j, k]
    r_x = l_x+1
    b_y = Y[i, j, k]
    f_y = b_y+1
    b_z = Z[i, j, k]
    t_z = b_z+1
    #   positions    colors
    vertices = [
    # Z+: number 1
        l_x, b_y,  t_z, r,g,b,
         r_x, b_y,  t_z, r,g,b,
         r_x,  f_y,  t_z, r,g,b,
        l_x,  f_y,  t_z, r,g,b,
    # Z-: number 6
        l_x, b_y, b_z, r,g,b,
         r_x, b_y, b_z, r,g,b,
         r_x,  f_y, b_z, r,g,b,
        l_x,  f_y, b_z, r,g,b,
    # X+: number 5
         r_x, b_y, b_z, r,g,b,
         r_x,  f_y, b_z, r,g,b,
         r_x,  f_y,  t_z, r,g,b,
         r_x, b_y,  t_z, r,g,b,
    # X-: number 2
        l_x, b_y, b_z, r,g,b,
        l_x,  f_y, b_z, r,g,b,
        l_x,  f_y,  t_z, r,g,b,
        l_x, b_y,  t_z, r,g,b,
    # Y+: number 4
        l_x,  f_y, b_z, r,g,b,
        r_x,  f_y, b_z, r,g,b,
        r_x,  f_y, t_z, r,g,b,
        l_x,  f_y, t_z, r,g,b,
    # Y-: number 3
        l_x, b_y, b_z, r,g,b,
        r_x, b_y, b_z, r,g,b,
        r_x, b_y, t_z, r,g,b,
        l_x, b_y, t_z, r,g,b
        ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,
        4, 5, 6, 6, 7, 4,
        4, 5, 1, 1, 0, 4,
        6, 7, 3, 3, 2, 6,
        5, 6, 2, 2, 1, 5,
        7, 4, 0, 0, 3, 7]

    return bs.Shape(vertices, indices)

def merge(destinationShape, strideSize, sourceShape):

    # current vertices are an offset for indices refering to vertices of the new shape
    offset = len(destinationShape.vertices)
    destinationShape.vertices += sourceShape.vertices
    destinationShape.indices += [(offset/strideSize) + index for index in sourceShape.indices]
