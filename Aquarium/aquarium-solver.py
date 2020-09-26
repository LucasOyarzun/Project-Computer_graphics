import numpy as np
import json
import sys

from scipy.sparse import csc_matrix
from scipy.sparse import csr_matrix
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

import matplotlib.pyplot as mpl
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from matplotlib import cm

# We define a function to convert the indices from i,j to k and viceversa
# i,j indexes the discrete domain in 2D.
# k parametrize those i,j, this way we can tidy the unknowns
# in a column vector and use the standard algebra
#archivo_json = 'problem-setup.json'
grafico = False
archivo_json = sys.argv[1]
if len(sys.argv) == 3:
    grafico = sys.argv[2]
print('Espere un poco, esto toma su tiempo')

with open(archivo_json) as file:
    data = json.load(file)
    H= data["height"]
    W= data["width"]
    L= data["lenght"]
    F= data["window_loss"]
    Heather_a= data["heater_a"]
    Heather_b= data["heater_b"]
    T= data["ambient_temperature"]
    filename = data["filename"]


def aquiariumSolver(H=H, W=W,L=L, h=0.1,T= T, Ta = Heather_a , Tb = Heather_b, F=-F, filename = filename,grafico = grafico): # TOP=100, BOTTOM=-10, LEFT=0, RIGHT=10
    # Number of unknowns
    # left, bottom and top sides are known (Dirichlet condition)
    # right side is unknown (Neumann condition)
    nh = int(W / h) - 1
    nv = int(L / h) - 1
    na = int(H / h) - 1
    
    # In this case, the domain is just a rectangle
    N = nh * nv* na

    # We define a function to convert the indices from i,j to k and viceversa
    # i,j indexes the discrete domain in 2D.
    # k parametrize those i,j, this way we can tidy the unknowns
    # in a column vector and use the standard algebra

    def newgetK(i, j, z):
        return z * nh*nv + j * nh + i 

    def newgetIJZ(k):
        i = k % (nh*nv) % nh
        j = k % (nh*nv) // nh
        z = k // (nh*nv)
        return (i, j, z)

    # In this matrix we will write all the coefficients of the unknowns
    #A = np.zeros((N, N))
    A = lil_matrix((N, N))  # We use a sparse matrix in order to spare memory, since it has many 0's      #Creamos matriz sparse

    # In this vector we will write all the right side of the equations
    b = np.zeros((N,))                                                                                    #Creamos el vector b

    # Note: To write an equation is equivalent to write a row in the matrix system

    # We iterate over each point inside the domain
    # Each point has an equation associated
    # The equation is different depending on the point location inside the domain
    for i in range(0, nh):                                                                                 #Asignamos valores a la matriz
        for j in range(0, nv):
            for z in range(0, na):
                
                # We will write the equation associated with row k
                k = newgetK(i , j, z)

                # We obtain indices of the other coefficients
                k_front = newgetK(i, j+1, z)
                k_back = newgetK(i, j-1, z)
                k_left = newgetK(i-1, j, z)
                k_right = newgetK(i+1, j, z)
                k_down = newgetK(i, j, z-1)
                k_up = newgetK(i, j, z+1)

                # Depending on the location of the point, the equation is different
                # Interior
                if 1 <= i and i <= nh - 2 and 1 <= j and j <= nv - 2 and 1 <= z and z <= na - 2:
                    A[k, k_up] = 1
                    A[k, k_down] = 1
                    A[k, k_left] = 1
                    A[k, k_right] = 1
                    A[k, k_back] = 1
                    A[k, k_front] = 1
                    A[k, k] = -6
                    b[k] = 0

                #REGULADORES
                #Regulador a

                elif z == 0 and nh//3 <= i and i <= 2*nh//3 and 3*nv//5 <= j and j <= 4*nv//5:
                
                    A[k, k_up] = 1
                    A[k, k_left] = 1
                    A[k, k_right] = 1
                    A[k, k_back] = 1
                    A[k, k_front] = 1
                    A[k, k] = -6
                    b[k] = -Ta

                #Regulador b

                elif z == 0 and nh//3 <= i and i <= 2*nh//3 and nv//5 <= j and j <= 2*nv//5: 
                    
                    A[k, k_up] = 1
                    A[k, k_left] = 1
                    A[k, k_right] = 1
                    A[k, k_back] = 1
                    A[k, k_front] = 1
                    A[k, k] = -6
                    b[k] = -Tb

                #CARAS (6)
                # left face
                elif i == 0 and 1 <= j and j <= nv - 2 and 1 <= z and z <= na - 2:
                    A[k, k_up] = 1
                    A[k, k_down] = 1
                    A[k, k_right] = 2
                    A[k, k_back] = 1
                    A[k, k_front] = 1
                    A[k, k] = -6
                    b[k] = 2*h*F

                # back face
                elif 1 <= i and i <= nh - 2 and j == 0 and 1 <= z and z <= na - 2:
                    A[k, k_up] = 1
                    A[k, k_left] = 1
                    A[k, k_right] = 1
                    A[k, k_down] = 1
                    A[k, k_front] = 2
                    A[k, k] = -6
                    b[k] = 2*h*F
                
                # right face
                elif i == nh - 1 and 1 <= j and j <= nv - 2 and 1 <= z and z <= na - 2:
                    A[k, k_up] = 1
                    A[k, k_down] = 1
                    A[k, k_left] = 2
                    A[k, k_back] = 1
                    A[k, k_front] = 1
                    A[k, k] = -6
                    b[k] = 2*h*F

                # front face
                elif 1 <= i and i <= nh - 2 and j == nv - 1 and 1 <= z and z <= na - 2:
                    A[k, k_down] = 1
                    A[k, k_left] = 1
                    A[k, k_right] = 1
                    A[k, k_back] = 2
                    A[k, k_up] = 1
                    A[k, k] = -6
                    b[k] = 2*h*F
                
                # up face
                elif 1 <= i and i <= nh - 2 and 1 <= j and j <= nv - 2 and z == na - 1:
                    A[k, k_down] = 1
                    A[k, k_left] = 1
                    A[k, k_right] = 1
                    A[k, k_back] = 1
                    A[k, k_front] = 1
                    A[k, k] = -6
                    b[k] = -T
                # down face
                elif 1 <= i and i <= nh - 2 and 1 <= j and j <= nv - 2 and z == 0:
                    A[k, k_up] = 2
                    A[k, k_left] = 1
                    A[k, k_right] = 1
                    A[k, k_back] = 1
                    A[k, k_front] = 1
                    A[k, k] = -6
                    b[k] = 0

                #ESQUINAS (8)

                #Esquinas de back

                # corner down left back
                elif (i, j, z) == (0, 0, 0):
                    A[k, k_up] = 2
                    A[k, k_right] = 2
                    A[k, k_front] = 2
                    A[k, k] = -6
                    b[k] = 4*h*F

                # corner down right back
                elif (i, j, z) == (nh - 1, 0, 0):
                    A[k, k_up] = 2
                    A[k, k_left] = 2
                    A[k, k_front] = 2
                    A[k, k] = -6
                    b[k] = 4*h*F 

                # corner up left back
                elif (i, j, z) == (0, 0, na - 1):
                    A[k, k_down] = 1
                    A[k, k_right] = 2
                    A[k, k_front] = 2
                    A[k, k] = -6
                    b[k] = 4*h*F -T

                # corner up right back
                elif (i, j, z) == (nh - 1, 0, na - 1 ):
                    A[k, k_down] = 1
                    A[k, k_left] = 2
                    A[k, k_front] = 2
                    A[k, k] = -6
                    b[k] = 4*h*F -T

                #Esquinas de front

                # corner down left front
                elif (i, j, z) == (0, nv - 1, 0):
                    A[k, k_up] = 2
                    A[k, k_right] = 2
                    A[k, k_back] = 2
                    A[k, k] = -6
                    b[k] = 4*h*F

                # corner down right front
                elif (i, j, z) == (nh - 1, nv - 1, 0):
                    A[k, k_up] = 2
                    A[k, k_left] = 2
                    A[k, k_back] = 2
                    A[k, k] = -6
                    b[k] = 4*h*F

                # corner up left front
                elif (i, j, z) == (0, nv - 1, na - 1):
                    A[k, k_down] = 1
                    A[k, k_left] = 2
                    A[k, k_back] = 2
                    A[k, k] = -6
                    b[k] = 4*h*F -T

                # corner up right front
                elif (i, j, z) == (nh - 1, nv - 1, na - 1 ):
                    A[k, k_down] = 1
                    A[k, k_left] = 2
                    A[k, k_back] = 2
                    A[k, k] = -6
                    b[k] = 4*h*F -T
                
                #Aristas (12)

                #Aristas de abajo

                # left down corner
                elif i == 0 and z == 0 and 1 <= j and j <= nv - 2:
                    A[k, k_up] = 2
                    A[k, k_front] = 1
                    A[k, k_right] = 2
                    A[k, k_back] = 1
                    A[k, k] = -6
                    b[k] = 2*h*F
                
                # right down corner
                elif i == nh - 1 and z == 0 and 1 <= j and j <= nv - 2:
                    A[k, k_up] = 2
                    A[k, k_back] = 1
                    A[k, k_left] = 2
                    A[k, k_front] = 1
                    A[k, k] = -6
                    b[k] = 2*h*F
                
                # back down corner
                elif 1 <= i  and i <= nh - 2 and j == 0 and z == 0:
                    A[k, k_up] = 2
                    A[k, k_left] = 1
                    A[k, k_right] = 1
                    A[k, k_front] = 2
                    A[k, k] = -6
                    b[k] = 2*h*F
                
                # front down corner
                elif 1 <= i  and i <= nh - 2 and j == nv - 1 and z == 0:
                    A[k, k_up] = 2
                    A[k, k_left] = 1
                    A[k, k_right] = 1
                    A[k, k_back] = 2
                    A[k, k] = -6
                    b[k] = 2*h*F
                
                #Aristas del medio

                # front right middle corner
                elif i == nh - 1 and j == nv - 1 and 1 <= z and z <= na - 2:
                    A[k, k_up] = 1
                    A[k, k_down] = 1
                    A[k, k_left] = 2
                    A[k, k_back] = 2
                    A[k, k] = -6
                    b[k] = 4*h*F
                
                # front left middle corner
                elif i == 0 and j == nv - 1 and 1 <= z and z <= na - 2:
                    A[k, k_up] = 1
                    A[k, k_back] = 2
                    A[k, k_right] = 2
                    A[k, k_down] = 1
                    A[k, k] = -6
                    b[k] = 4*h*F 
                
                # back right middle corner
                elif i == nh - 1 and j == 0 and 1 <= z and z <= na - 2:
                    A[k, k_up] = 1
                    A[k, k_left] = 2
                    A[k, k_down] = 1
                    A[k, k_front] = 2
                    A[k, k] = -6
                    b[k] = 4*h*F
                
                # back left middle corner
                elif i == 0 and j == 0 and 1 <= z and z <= na - 2:
                    A[k, k_up] = 1
                    A[k, k_down] = 1
                    A[k, k_right] = 2
                    A[k, k_front] = 2
                    A[k, k] = -6
                    b[k] = 4*h*F

                #Aristas de arriba

                # left up corner
                elif i == 0  and 1 <= j and j <= nv - 2 and z == na - 1:
                    A[k, k_down] = 1
                    A[k, k_front] = 1
                    A[k, k_right] = 2
                    A[k, k_back] = 1
                    A[k, k] = -6
                    b[k] = 2*h*F -T
                
                # right up corner
                elif i == nh - 1  and 1 <= j and j <= nv - 2 and z == na - 1 :
                    A[k, k_down] = 1
                    A[k, k_back] = 1
                    A[k, k_left] = 2
                    A[k, k_front] = 1
                    A[k, k] = -6
                    b[k] = 2*h*F - T
                
                # back up corner
                elif 1 <= i  and i <= nh - 2 and j == 0 and z == na - 1 :
                    A[k, k_down] = 1
                    A[k, k_left] = 1
                    A[k, k_right] = 1
                    A[k, k_front] = 2
                    A[k, k] = -6
                    b[k] = 2*h*F - T
                
                # front up corner
                elif 1 <= i  and i <= nh - 2 and j == nv - 1 and z == na -1:
                    A[k, k_down] = 1
                    A[k, k_left] = 1
                    A[k, k_right] = 1
                    A[k, k_back] = 2
                    A[k, k] = -6
                    b[k] = 2*h*F - T
                else:
                    print("Point (" + str(i) + ", " + str(j) + str(z) + ") missed!")
                    print("Associated point index is " + str(k))
                    raise Exception()

    # A quick view of a sparse matrix
    #mpl.spy(A)
    print('Matriz creada, resolviendo EDP')
    # Solving our system
    #x = np.linalg.solve(A, b)
    x = spsolve(A, b)                                                                                      #Resolvemos el sistemas de ecuaciones
    print('EDP lista, ahora se está graficando')
    # Now we return our solution to the 2d discrete domain
    # In this matrix we will store the solution in the 2d domain
    u = np.zeros((nh, nv, na))

    for k in range(0, N):                                     
        i, j, z = newgetIJZ(k)
        u[i, j, z] = x[k]

    # Adding the borders, as they have known values
    ub = np.zeros((nh + 2, nv + 2, na + 2))
    ub[1:nh + 1, 1:nv + 1, 1:na + 1] = u[:, :, :]
    
    # Dirichlet boundary condition
    # top
    ub[0:nh + 2,0:nv + 2, na + 1] = T
    
    #heathers
    ub[nh//3:2*nh//3,3*nv//5:4*nv//5, 0] = Ta
    ub[nh//3:2*nh//3,nv//5:2*nv//5, 0] = Tb

    np.save(filename, ub)                              #Guardamos la matriz ub con las temperaturas en (x,y,z)
    
    datos_pecera=[h,H,W,L,F,T,Heather_a,Heather_b]     #Guardamos un arreglo con los datos ingresados para la pecera
    np.save("datos_pecera.npy",datos_pecera)
    
    #if grafico==True:                                  #Si se indica, se crea el Gráfico en 3D
        # Graph in 3D
        # 3D
        # Make data.
    X = np.arange(0, ub.shape[0]-2, 1, dtype=int)
    Y = np.arange(0, ub.shape[1]-2, 1, dtype=int)
    Z = np.arange(0, ub.shape[2]-2, 1, dtype=int)
    X, Y, Z = np.meshgrid(Y, X, Z)

    fig = mpl.figure()

    ax = fig.add_subplot(111, projection='3d')
    scat= ax.scatter(Z, X, Y, c=x, marker='*')

    fig.colorbar(scat)

    ax.set_title('Acuario EDP')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    mpl.show()
    return ub

aquiariumSolver()
