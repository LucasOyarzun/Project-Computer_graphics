import sys
import numpy as np
import json
from scipy.stats import truncnorm

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders

import transformations as tr  # importa transformaciones
import easy_shaders as es  # importa shaders
import basic_shapes as bs # importa shapes
import scene_graph as sg

#Funciones propias
from funciones_marching_cubes import fast_marching_cube_aqua
from funciones_marching_cubes import fast_marching_cube
from funciones_marching_cubes import createColorCube
from funciones_marching_cubes import merge
from peces import createDori
from peces import createNemo
from peces import createSwordfish

###########################

################## ARCHIVO JSON, DATOS PECERA

#archivo_json = 'view-setup.json'
archivo_json = sys.argv[1]

with open(archivo_json) as file:
    data = json.load(file)
    filename = data["filename"]
    t_a = data["t_a"]
    t_b = data["t_b"]
    t_c = data["t_c"]
    n_a = data["n_a"]
    n_b = data["n_b"]
    n_c = data["n_c"]

ub = np.load(filename)                     #matriz ub de aquarium_solver.py

datos_pecera = np.load("datos_pecera.npy") #datos_pecera = [h,H,W,L,F,T,Heather_a,Heather_b]
H = datos_pecera[1]
W = datos_pecera[2]
L = datos_pecera[3]

#################################################

#################################CONTROLLER

# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True        
        self.showAxis = False
        self.mousePos = 0
        self.visual = '1' #Para el tipo de transparencia
        self.agua = True #Para que se vea el agua o no
        self.temperatura_a = True
        self.temperatura_b = True
        self.temperatura_c = True

# We will use the global controller as communication with the callback function
controller = Controller()

def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller
    if key == glfw.KEY_LEFT_CONTROL:
        controller.showAxis = not controller.showAxis

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

    if key == glfw.KEY_A:
        controller.temperatura_a = not controller.temperatura_a
    if key == glfw.KEY_B:
        controller.temperatura_b = not controller.temperatura_b
    if key == glfw.KEY_C:
        controller.temperatura_c = not controller.temperatura_c

    if key == glfw.KEY_1:
        controller.visual = '1'

    if key == glfw.KEY_2:
        controller.visual = '2'

    if key == glfw.KEY_3:
        controller.agua = not controller.agua

def cursor_pos_callback(window, x, y): # da la posición del mouse en pantalla con coordenadas
    global controller
    controller.mousePos =(x, y)

##########################################

###################################ACUARIO

def createAquarium(W=W,L=L,H=H):
    gpuBlackCube = es.toGPUShape(bs.createColorCube(0.6,0.6,0.6))

    ancho = sg.SceneGraphNode("ancho")
    ancho.transform = tr.scale(W*10, 1, 1)
    ancho.childs += [gpuBlackCube]

    largo = sg.SceneGraphNode("largo")
    largo.transform = tr.scale(1, L*10, 1)
    largo.childs += [gpuBlackCube] 

    alto = sg.SceneGraphNode("alto")
    alto.transform = tr.scale(1, 1, H*10)
    alto.childs += [gpuBlackCube]

    ancho1 = sg.SceneGraphNode("ancho1")
    ancho1.transform = tr.translate(0, -L/2*10, -H/2*10)
    ancho1.childs += [ancho]

    ancho2 = sg.SceneGraphNode("ancho2")
    ancho2.transform = tr.translate(0, L/2*10, -H/2*10)
    ancho2.childs += [ancho]  

    ancho3 = sg.SceneGraphNode("ancho3")
    ancho3.transform = tr.translate(0, -L/2*10, H/2*10)
    ancho3.childs += [ancho]  

    ancho4 = sg.SceneGraphNode("ancho4")
    ancho4.transform = tr.translate(0, L/2*10, H/2*10)
    ancho4.childs += [ancho]    

    largo1 = sg.SceneGraphNode("largo1")
    largo1.transform = tr.translate(-W/2*10, 0, -H/2*10)
    largo1.childs += [largo]

    largo2 = sg.SceneGraphNode("largo2")
    largo2.transform = tr.translate(W/2*10, 0, -H/2*10)
    largo2.childs += [largo]

    largo3 = sg.SceneGraphNode("largo3")
    largo3.transform = tr.translate(-W/2*10, 0, H/2*10)
    largo3.childs += [largo]

    largo4 = sg.SceneGraphNode("largo4")
    largo4.transform = tr.translate(W/2*10, 0, H/2*10)
    largo4.childs += [largo]

    alto1 = sg.SceneGraphNode("alto1")
    alto1.transform = tr.translate(-W/2*10, -L/2*10, 0)
    alto1.childs += [alto]

    alto2 = sg.SceneGraphNode("alto2")
    alto2.transform = tr.translate(W/2*10, -L/2*10, 0)
    alto2.childs += [alto]

    alto3 = sg.SceneGraphNode("alto3")
    alto3.transform = tr.translate(-W/2*10, L/2*10, 0)
    alto3.childs += [alto]

    alto4 = sg.SceneGraphNode("alto4")
    alto4.transform = tr.translate(W/2*10, L/2*10, 0)
    alto4.childs += [alto]

    acuario = sg.SceneGraphNode("acuario")
    acuario.transform = tr.rotationZ(np.pi/2)
    acuario.childs += [alto1]
    acuario.childs += [alto2]
    acuario.childs += [alto3]
    acuario.childs += [alto4]
    acuario.childs += [ancho1]
    acuario.childs += [ancho2]
    acuario.childs += [ancho3]
    acuario.childs += [ancho4]
    acuario.childs += [largo1]
    acuario.childs += [largo2]
    acuario.childs += [largo3]
    acuario.childs += [largo4]
    return acuario
##################################################
#############################################VOXELES

X = np.arange(-ub.shape[0]//2, ub.shape[0]//2, 1, dtype=int) #Aranges centrados en 0
Y = np.arange(-ub.shape[1]//2, ub.shape[1]//2, 1, dtype=int)
Z = np.arange(-ub.shape[2]//2, ub.shape[2]//2, 1, dtype=int)
X, Y, Z = np.meshgrid(Y,X, Z)
redVoxels = fast_marching_cube(X, Y, Z, ub, t_a)
yellowVoxels = fast_marching_cube(X, Y, Z, ub, t_b)
blueVoxels = fast_marching_cube(X, Y, Z, ub, t_c)
aquaVoxels = fast_marching_cube_aqua(X, Y, Z, ub, t_c)

#################################################

#############################################MAIN

if __name__ == "__main__":
    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 1000
    height = 800

    window = glfw.create_window(width, height, "Acuario", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)
    glfw.set_cursor_pos_callback(window, cursor_pos_callback)

    # Different shader programs for different lighting strategies

    # This shader program does not consider lighting
    mvpPipeline = es.SimpleModelViewProjectionShaderProgram()                #3 pipelines
    transPipeline1 =es.SimpleModelViewProjectionTransparente1ShaderProgram()
    transPipeline2 =es.SimpleModelViewProjectionTransparente2ShaderProgram()
    # Setting up the clear screen color
    glClearColor(0.9, 0.9, 0.9, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
########################################################

##########################################SHAPES Y VARIABLES

    # Creating shapes on GPU memory
    gpuAquarium =  createAquarium(W,L,H)
    gpuAxis = es.toGPUShape(bs.createAxis(4))

    t0 = glfw.get_time()
    camera_theta = np.pi/4
    camera_thetaz = np.pi/4
    camera_dist = 100
    theta_cola =0         #Angulo de movimiento de colas

    lugares_a =[]         #Lugares donde iran los peces
    lugares_b =[]  
    lugares_c =[]
    listaNemos = []       #Lista de peces
    listaDoris = []
    listaEspadas = []

#####################################################

###########################DIBUJAR VOXELES
    isosurfaceRed = bs.Shape([], [])
    isosurfaceYellow = bs.Shape([], [])
    isosurfaceBlue = bs.Shape([], [])
    isosurfaceAqua = bs.Shape([], [])
    
    # Now let's draw voxels!
    for i in range(X.shape[0]-1):
        for j in range(X.shape[1]-1):
            for k in range(X.shape[2]-1):
                if aquaVoxels[i,j,k]:                                                           #Voxels de agua
                    temp_shape = createColorCube(i,j,k, X,Y, Z, 0, 0.7, 0.9)
                    merge(destinationShape=isosurfaceAqua, strideSize=6, sourceShape=temp_shape)
                    
                if redVoxels[i,j,k]:                                                            #Voxels rojos
                    temp_shape = createColorCube(i,j,k, X,Y, Z, 1, 0, 0)
                    merge(destinationShape=isosurfaceRed, strideSize=6, sourceShape=temp_shape)
                    lugares_a.append((j-L*5,i-W*5,k-H*5))                                       #Lugares de Nemo

                if yellowVoxels[i,j,k]:                                                          #Voxels amarillos
                    temp_shape = createColorCube(i,j,k, X,Y, Z, 1, 1, 0)
                    merge(destinationShape=isosurfaceYellow, strideSize=6, sourceShape=temp_shape)
                    lugares_b.append((j-L*5,i-W*5,k-H*5))                                       #Lugares de Dori

                if blueVoxels[i,j,k]:                                                            #Voxels azules
                    temp_shape = createColorCube(i,j,k, X,Y, Z, 0, 0, 1)
                    merge(destinationShape=isosurfaceBlue, strideSize=6, sourceShape=temp_shape)
                    lugares_c.append((j-L*5,i-W*5,k-H*5))                                       #Lugares de Espada
    
    gpu_surfaceAqua = es.toGPUShape(isosurfaceAqua)       #Superficies a GPU
    gpu_surfaceRed = es.toGPUShape(isosurfaceRed)
    gpu_surfaceYellow = es.toGPUShape(isosurfaceYellow)
    gpu_surfaceBlue = es.toGPUShape(isosurfaceBlue)

    ##################################################################

    #########################LISTAS CON LOS LUGARES PARA PONER LOS PECES
    for i in range(n_a):
        random_a = np.random.randint(len(lugares_a))                                      #Sacamos un indice random
        indice_a = lugares_a.pop(random_a)                                                #ESTO ES NECESARIO PARA NO REPETIR POSICIONES(SUPERPONER)
        nemo = createNemo(indice_a[0],indice_a[1],indice_a[2],np.random.uniform(2*np.pi))   #Creamos un Nemo
        listaNemos.append(nemo)                                                           #Agregamos el Nemo a la lista

    for i in range(n_b):
        random_b = np.random.randint(len(lugares_b))                                      #Sacamos un indice random
        indice_b = lugares_b.pop(random_b)                                                #ESTO ES NECESARIO PARA NO REPETIR POSICIONES(SUPERPONER)
        dori = createDori(indice_b[0],indice_b[1],indice_b[2],np.random.uniform(2*np.pi))   #Creamos una Dori
        listaDoris.append(dori)                                                           #Agregamos a Dori a la lista

    for i in range(n_c):
        random_c = np.random.randint(len(lugares_c))                                      #Sacamos un indice random
        indice_c = lugares_c.pop(random_c)                                                #ESTO ES NECESARIO PARA NO REPETIR POSICIONES(SUPERPONER)
        espada = createSwordfish(indice_c[0],indice_c[1],indice_c[2],np.random.uniform(2*np.pi))#Creamos una Dori
        listaEspadas.append(espada)                                                       #Agregamos el Espada a la lista

########################################################

#################################################WHILE
    while not glfw.window_should_close(window):
        
    # Using GLFW to check for input events
        glfw.poll_events()

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1    
############################################################

#######################################################CAMARA
        if (glfw.get_key(window, glfw.KEY_W) == glfw.PRESS):
            if camera_dist >=0.2:
                camera_dist -= 40 * dt
        if (glfw.get_key(window, glfw.KEY_S) == glfw.PRESS):
            camera_dist += 40 * dt

        if (glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS):
            camera_theta += 2 * dt

        if (glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS):
            camera_theta -= 2* dt
        if (glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS):
            if camera_thetaz<np.pi/2:
                camera_thetaz += 2* dt
        if (glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS):
            if camera_thetaz >-np.pi/2:
                camera_thetaz -= 2* dt
        projection = tr.perspective(45, float(width)/float(height), 0.1, 1000)

        camX = camera_dist * np.sin(camera_theta)
        camY = camera_dist * np.cos(camera_theta)
        camZ = camera_dist * np.sin(camera_thetaz)

        viewPos = np.array([camX,camY,camZ+2])

        view = tr.lookAt(
            viewPos,
            np.array([0,0,0]),
            np.array([0,0,1])
        )
#############################################################

################################################MOVIMIENTO COLAS
        for i in range(n_a):
            nemoCuerpoRotation = sg.findNode(listaNemos[i],"cuerpo4Rotation")
            nemoCola1Rotation = sg.findNode(listaNemos[i],"cola1Rotation")
            nemoCola2Rotation = sg.findNode(listaNemos[i],"cola2Rotation")
            if -2*np.sin(theta_cola) <3 and -2*np.sin(theta_cola)>-11 :
                nemoCuerpoRotation.transform = tr.rotationZ(-0.5*np.sin(theta_cola))
                nemoCola1Rotation.transform = tr.rotationZ(-0.5*np.sin(theta_cola))
                nemoCola2Rotation.transform = tr.rotationZ(-0.6*np.sin(theta_cola))

        for i in range(n_b):
            doriColaRotation = sg.findNode(listaDoris[i],"colaRotation")
            doriColaTranslation = sg.findNode(listaDoris[i],"colaTranslation")
            if -2*np.sin(theta_cola) <3 and -2*np.sin(theta_cola)>-11 :
                doriColaRotation.transform = tr.rotationZ(-np.sin(theta_cola))
                doriColaTranslation.transform = tr.translate(-1.1,0.2*np.sin(theta_cola),0)

        for i in range(n_c):
            espadaCuerpoRotation = sg.findNode(listaEspadas[i],"cuerpo3Rotation")
            espadaColaRotation = sg.findNode(listaEspadas[i],"colaRotation")
            if -2*np.sin(theta_cola) <3 and -2*np.sin(theta_cola)>-11 :
                espadaCuerpoRotation.transform = tr.rotationZ(-0.5*np.sin(theta_cola))
                espadaColaRotation.transform = tr.rotationZ(-0.5*np.sin(theta_cola))
        theta_cola +=dt*5    
####################################################################

#####################################################DIBUJAMOS LAS COSAS

        axis = np.array([1,-1,1])
        axis = axis / np.linalg.norm(axis)
        model = tr.identity()
        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # The axis is drawn without lighting effects

        glUseProgram(mvpPipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())

        if controller.showAxis:      
            mvpPipeline.drawShape(gpuAxis, GL_LINES)
        
        sg.drawSceneGraphNode(gpuAquarium, mvpPipeline, 'model')   #Dibujamos las barras del acuario
        
        for nemo in listaNemos:                                    #Dibujamos los peces
            sg.drawSceneGraphNode(nemo, mvpPipeline, 'model')
        for dori in listaDoris:
            sg.drawSceneGraphNode(dori, mvpPipeline, 'model')
        for espada in listaEspadas:
            sg.drawSceneGraphNode(espada, mvpPipeline, 'model')

        ###################################################USO DE TRANSPARENCIA(O NO)
        if controller.visual == '1':
            glUseProgram(transPipeline1.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(transPipeline1.shaderProgram, "projection"), 1, GL_TRUE, projection)
            glUniformMatrix4fv(glGetUniformLocation(transPipeline1.shaderProgram, "view"), 1, GL_TRUE, view)
            glUniformMatrix4fv(glGetUniformLocation(transPipeline1.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
            
            if controller.temperatura_a == True:                     #Dibujamos rojos
                transPipeline2.drawShape(gpu_surfaceRed)
            if controller.temperatura_b == True:                     #Dibujamos amarillos
                transPipeline2.drawShape(gpu_surfaceYellow)
            if controller.temperatura_c == True:                     #Dibujamos azules      
                transPipeline2.drawShape(gpu_surfaceBlue) 
            if controller.agua == True:                           #Dibujamos agua
                transPipeline2.drawShape(gpu_surfaceAqua)

        if controller.visual == '2':
            glUseProgram(transPipeline2.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(transPipeline2.shaderProgram, "projection"), 1, GL_TRUE, projection)
            glUniformMatrix4fv(glGetUniformLocation(transPipeline2.shaderProgram, "view"), 1, GL_TRUE, view)
            glUniformMatrix4fv(glGetUniformLocation(transPipeline2.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
            
            if controller.temperatura_a == True:                     #Dibujamos rojos
                transPipeline2.drawShape(gpu_surfaceRed)
            if controller.temperatura_b == True:                     #Dibujamos amarillos
                transPipeline2.drawShape(gpu_surfaceYellow)
            if controller.temperatura_c == True:                     #Dibujamos azules      
                transPipeline2.drawShape(gpu_surfaceBlue) 
            if controller.agua == True:                           #Dibujamos agua
                transPipeline2.drawShape(gpu_surfaceAqua)
        
        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()