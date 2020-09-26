import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders

import numpy as np
import sys  # para hacer handling de eventos, como entradas del sistema, o cerrar el programa.
import transformations as tr  # importa transformaciones
import easy_shaders as es  # importa shaders
import basic_shapes as bs # importa shapes
import scene_graph as sg

# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True        
        self.showAxis = False
        self.mousePos = 0

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

    elif key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

def createNemo(i,j,k,theta):
    
    gpuWhiteCube = es.toGPUShape(bs.createColorCube(1,1,1))
    gpuOrangeCube = es.toGPUShape(bs.createColorCube(1,0.2,0))
    gpuOrangeTriangle = es.toGPUShape(bs.createColor3dTriangle(1, 0.2, 0))
    gpuBlackCube = es.toGPUShape(bs.createColorCube(0 , 0, 0))

    cara = sg.SceneGraphNode("cara")
    cara.transform = tr.matmul([tr.translate(1.5,0,0),tr.rotationY(np.pi/2),tr.scale(1,1,0.5)])
    cara.childs += [gpuOrangeTriangle]

    ojoder = sg.SceneGraphNode("ojoder")
    ojoder.transform = tr.matmul([tr.translate(1.5,0.3,0.3),tr.uniformScale(0.1)])
    ojoder.childs +=[gpuBlackCube]

    ojoizq = sg.SceneGraphNode("ojoizq")
    ojoizq.transform = tr.matmul([tr.translate(1.5,-0.3,0.3),tr.uniformScale(0.1)])
    ojoizq.childs +=[gpuBlackCube]

    ojos = sg.SceneGraphNode("ojos")
    ojos.childs += [ojoizq]
    ojos.childs += [ojoder]

    cabeza = sg.SceneGraphNode("cabeza")
    cabeza.childs += [cara]
    cabeza.childs += [ojos]

    cuerpo1 = sg.SceneGraphNode("cuerpo1")
    cuerpo1.transform = tr.matmul([tr.translate(1,0,0),tr.scale(0.5,1,1)])
    cuerpo1.childs +=[gpuWhiteCube]

    cuerpo2 = sg.SceneGraphNode("cuerpo2")
    cuerpo2.transform = tr.matmul([tr.translate(0.25,0,0),tr.scale(1,1,1)])
    cuerpo2.childs +=[gpuOrangeCube]

    cuerpo3 = sg.SceneGraphNode("cuerpo3")
    cuerpo3.transform = tr.matmul([tr.translate(-0.5,0,0),tr.scale(0.5,1,1)])
    cuerpo3.childs +=[gpuWhiteCube]

    aletaizq = sg.SceneGraphNode("aletaizq")
    aletaizq.transform = tr.matmul([tr.translate(0.8,-0.7,0),tr.rotationZ(-np.pi/4),tr.scale(0.2,0.6,0.5)])
    aletaizq.childs +=[gpuOrangeCube]

    aletader = sg.SceneGraphNode("aletader")
    aletader.transform = tr.matmul([tr.translate(0.8,0.7,0),tr.rotationZ(np.pi/4),tr.scale(0.2,0.6,0.5)])
    aletader.childs +=[gpuOrangeCube]

    aletaarr = sg.SceneGraphNode("aletaarr")
    aletaarr.transform = tr.matmul([tr.translate(0.5,0,0.6),tr.scale(1,0.2,0.5)])
    aletaarr.childs +=[gpuOrangeCube] 

    cuerpo = sg.SceneGraphNode("cuerpo")
    cuerpo.childs += [cuerpo1]
    cuerpo.childs += [cuerpo2]
    cuerpo.childs += [cuerpo3]
    cuerpo.childs += [aletaizq]
    cuerpo.childs += [aletader]
    cuerpo.childs += [aletaarr]



    cuerpo4 = sg.SceneGraphNode("cuerpo4")
    cuerpo4.transform = tr.matmul([tr.translate(-1,0,0),tr.rotationY(-np.pi/2),tr.scale(1,1,0.5)])
    cuerpo4.childs +=[gpuOrangeTriangle]

    cuerpo4Rotation = sg.SceneGraphNode("cuerpo4Rotation")
    cuerpo4Rotation.childs += [cuerpo4]


    cola1 = sg.SceneGraphNode("cola1")
    cola1.transform = tr.matmul([tr.translate(-1.2,0,0),tr.scale(0.5,0.3,0.5)])
    cola1.childs +=[gpuWhiteCube]

    cola1Rotation = sg.SceneGraphNode("cola1Rotation")
    cola1Rotation.childs += [cola1]

    cola2 = sg.SceneGraphNode("cola2")
    cola2.transform = tr.matmul([tr.translate(-1.7,0,0),tr.rotationY(np.pi/2),tr.scale(0.5,0.3,0.5)])
    cola2.childs +=[gpuOrangeTriangle]

    cola2Rotation = sg.SceneGraphNode("cola2Rotation")
    cola2Rotation.childs +=[cola2]

    cola = sg.SceneGraphNode("cola")
    cola.childs += [cuerpo4Rotation]
    cola.childs += [cola1Rotation]
    cola.childs += [cola2Rotation]

    pez = sg.SceneGraphNode("pez")
    pez.transform = tr.matmul([tr.translate(i,j,k),tr.uniformScale(0.8),tr.rotationZ(theta)])
    pez.childs += [cabeza]
    pez.childs += [cuerpo]
    pez.childs += [cola]

    return pez

def createSwordfish(i,j,k,theta):

    gpuWhiteCube = es.toGPUShape(bs.createColorCube(1,1,1))
    gpuBlueCube = es.toGPUShape(bs.createColorCube(0,0,1))
    gpuBlueTriangle = es.toGPUShape(bs.createColor3dTriangle(0, 0, 1))
    gpuBlackCube = es.toGPUShape(bs.createColorCube(0 , 0, 0))
    gpuBluePyramid = es.toGPUShape(bs.createColorPyramid(0,0,1))

    nariz = sg.SceneGraphNode("nariz")
    nariz.transform = tr.matmul([tr.translate(2,0,0),tr.rotationY(np.pi/2),tr.scale(0.2,0.5,4)])
    nariz.childs += [gpuBluePyramid]

    cara = sg.SceneGraphNode("cara")
    cara.transform = tr.matmul([tr.translate(1.5,0,0),tr.rotationY(np.pi/2),tr.scale(1,0.5,0.5)])
    cara.childs += [gpuBluePyramid]

    ojoder = sg.SceneGraphNode("ojoder")
    ojoder.transform = tr.matmul([tr.translate(1.45,0.15,0.3),tr.uniformScale(0.1)])
    ojoder.childs +=[gpuBlackCube]

    ojoizq = sg.SceneGraphNode("ojoizq")
    ojoizq.transform = tr.matmul([tr.translate(1.45,-0.15,0.3),tr.uniformScale(0.1)])
    ojoizq.childs +=[gpuBlackCube]

    ojos = sg.SceneGraphNode("ojos")
    ojos.childs += [ojoizq]
    ojos.childs += [ojoder]

    cabeza = sg.SceneGraphNode("cabeza")
    cabeza.childs += [cara]
    cabeza.childs += [ojos]
    cabeza.childs += [nariz]

    cuerpo1 = sg.SceneGraphNode("cuerpo1")
    cuerpo1.transform = tr.matmul([tr.translate(0.25,0,0.25),tr.scale(2,0.5,0.5)])
    cuerpo1.childs +=[gpuBlueCube]

    cuerpo2 = sg.SceneGraphNode("cuerpo2")
    cuerpo2.transform = tr.matmul([tr.translate(0.25,0,-0.25),tr.scale(2,0.5,0.5)])
    cuerpo2.childs +=[gpuWhiteCube]


    aletaizq = sg.SceneGraphNode("aletaizq")
    aletaizq.transform = tr.matmul([tr.translate(0.8,-0.5,-0.2),tr.rotationX(-np.pi/2),tr.rotationY(-   3*np.pi/4),tr.scale(0.1,0.3,1.1)])
    aletaizq.childs +=[gpuBlueTriangle]

    aletader = sg.SceneGraphNode("aletader")
    aletader.transform = tr.matmul([tr.translate(0.8,0.5,-0.2),tr.rotationX(-np.pi/2),tr.rotationY(-np.pi/4),tr.scale(0.1,0.3,1.1)])
    aletader.childs +=[gpuBlueTriangle]

    aletaarr = sg.SceneGraphNode("aletaarr")
    aletaarr.transform = tr.matmul([tr.translate(0.7,0,0.6),tr.scale(0.7,0.2,0.9)])
    aletaarr.childs +=[gpuBlueTriangle] 

    cuerpo = sg.SceneGraphNode("cuerpo")
    cuerpo.childs += [cuerpo1]
    cuerpo.childs += [cuerpo2]
    cuerpo.childs += [aletaizq]
    cuerpo.childs += [aletader]
    cuerpo.childs += [aletaarr]

    cuerpo3 = sg.SceneGraphNode("cuerpo3")
    cuerpo3.transform = tr.matmul([tr.translate(-1.1,0,0),tr.rotationY(-np.pi/2),tr.scale(1,0.5,0.7)])
    cuerpo3.childs +=[gpuBluePyramid]

    cuerpo3Rotation = sg.SceneGraphNode("cuerpo3Rotation")
    cuerpo3Rotation.childs += [cuerpo3]

    cola = sg.SceneGraphNode("cola")
    cola.transform = tr.matmul([tr.translate(-1.6,0,0),tr.rotationY(np.pi/2),tr.scale(1.5,0.1,0.5)])
    cola.childs +=[gpuBluePyramid]

    colaRotation = sg.SceneGraphNode("colaRotation")
    colaRotation.childs +=[cola]

    cola = sg.SceneGraphNode("cola")
    cola.childs += [cuerpo3Rotation]
    cola.childs += [colaRotation]

    pez = sg.SceneGraphNode("pez")
    pez.transform = tr.matmul([tr.translate(i,j,k),tr.uniformScale(0.8),tr.rotationZ(theta)])
    pez.childs += [cabeza]
    pez.childs += [cuerpo]
    pez.childs += [cola]

    return pez

def createDori(i,j,k,theta):

    gpuBlackTriangle = es.toGPUShape(bs.createColor3dTriangle(0 , 0, 0))
    gpuBlackCube = es.toGPUShape(bs.createColorCube(0 , 0, 0))
    gpuBlueCube = es.toGPUShape(bs.createColorCube(0 , 0, 1))
    gpuBluePyramid = es.toGPUShape(bs.createColorPyramid(0,0,1))
    gpuYellowPyramid = es.toGPUShape(bs.createColorPyramid(1,1,0))

    cara = sg.SceneGraphNode("cara")
    cara.transform = tr.matmul([tr.translate(0.5,0,0),tr.rotationY(np.pi/2),tr.scale(1,0.3,0.5)])
    cara.childs += [gpuBluePyramid]

    ojoder = sg.SceneGraphNode("ojoder")
    ojoder.transform = tr.matmul([tr.translate(0.4,0.15,0.3),tr.uniformScale(0.1)])
    ojoder.childs +=[gpuBlackCube]

    ojoizq = sg.SceneGraphNode("ojoizq")
    ojoizq.transform = tr.matmul([tr.translate(0.4,-0.15,0.3),tr.uniformScale(0.1)])
    ojoizq.childs +=[gpuBlackCube]

    ojos = sg.SceneGraphNode("ojos")
    ojos.childs += [ojoizq]
    ojos.childs += [ojoder]

    cabeza = sg.SceneGraphNode("cabeza")
    cabeza.childs += [cara]
    cabeza.childs += [ojos]

    cuerpo1 = sg.SceneGraphNode("cuerpo1")
    cuerpo1.transform = tr.matmul([tr.translate(0.1,0,0),tr.scale(0.3,0.3,1)])
    cuerpo1.childs +=[gpuBlueCube]


    aletaizq = sg.SceneGraphNode("aletaizq")
    aletaizq.transform = tr.matmul([tr.translate(-0.3,-0.3,0.2),tr.rotationX(np.pi/4),tr.rotationY(-0.5),tr.rotationZ(np.pi/2),tr.scale(0.1,0.3,0.8)])
    aletaizq.childs +=[gpuYellowPyramid]

    aletader = sg.SceneGraphNode("aletader")
    aletader.transform = tr.matmul([tr.translate(-0.3,0.3,0.2),tr.rotationX(-np.pi/4),tr.rotationY(-0.5),tr.rotationZ(np.pi/2),tr.scale(0.1,0.3,0.8)])
    aletader.childs +=[gpuYellowPyramid]

    aletaarr = sg.SceneGraphNode("aletaarr")
    aletaarr.transform = tr.matmul([tr.translate(-0.2,0,0.4),tr.rotationY(-np.pi/8),tr.scale(1,0.125,0.3)])
    aletaarr.childs +=[gpuBlackTriangle] 

    cuerpo = sg.SceneGraphNode("cuerpo")
    cuerpo.childs += [cuerpo1]
    cuerpo.childs += [aletaizq]
    cuerpo.childs += [aletader]
    cuerpo.childs += [aletaarr]

    cuerpo2 = sg.SceneGraphNode("cuerpo2")
    cuerpo2.transform = tr.matmul([tr.translate(-0.55,0,0),tr.rotationY(-np.pi/2),tr.scale(1,0.3,1)])
    cuerpo2.childs +=[gpuBluePyramid]

    cuerpo2Rotation = sg.SceneGraphNode("cuerpo2Rotation")
    cuerpo2Rotation.childs += [cuerpo2]

    cola = sg.SceneGraphNode("cola")
    cola.transform = tr.matmul([tr.rotationY(np.pi/2),tr.scale(0.4,0.1,0.5)])
    cola.childs +=[gpuYellowPyramid]

    colaRotation = sg.SceneGraphNode("colaRotation")
    colaRotation.childs +=[cola]

    colaTranslation = sg.SceneGraphNode("colaTranslation")
    colaTranslation.transform = tr.translate(-1.1,0,0)
    colaTranslation.childs +=[colaRotation]

    cola = sg.SceneGraphNode("cola")
    cola.childs += [cuerpo2Rotation]
    cola.childs += [colaTranslation]

    pez = sg.SceneGraphNode("pez")
    pez.transform = tr.matmul([tr.translate(i,j,k),tr.uniformScale(0.8),tr.rotationZ(theta)])
    pez.childs += [cabeza]
    pez.childs += [cuerpo]
    pez.childs += [cola]

    return pez

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Pececitos", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # This shader program does not consider lighting
    mvpPipeline = es.SimpleModelViewProjectionShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    gpuAxis = es.toGPUShape(bs.createAxis(4))
    gpuNemo = createNemo(0,0,-1.5,0)
    gpuSwordfish = createSwordfish(0,0,1.5,0)
    gpuDori = createDori(0,0,0,0)
    gpuCube= es.toGPUShape(bs.createColorCube(1,0,0))

    t0 = glfw.get_time()
    camera_theta = np.pi/4
    theta_cola=0
    #######################VARIABLES A MOVER
    nemoCuerpoRotation = sg.findNode(gpuNemo,"cuerpo4Rotation")
    nemoCola1Rotation = sg.findNode(gpuNemo,"cola1Rotation")
    nemoCola2Rotation = sg.findNode(gpuNemo,"cola2Rotation")
    doriColaRotation = sg.findNode(gpuDori,"colaRotation")
    doriColaTranslation = sg.findNode(gpuDori,"colaTranslation")
    espadaCuerpoRotation = sg.findNode(gpuSwordfish,"cuerpo3Rotation")
    espadaColaRotation = sg.findNode(gpuSwordfish,"colaRotation")

    while not glfw.window_should_close(window):

        # Using GLFW to check for input events
        glfw.poll_events()

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        if (glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS):
            camera_theta -= 2 * dt

        if (glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS):
            camera_theta += 2* dt

        projection = tr.ortho(-1, 1, -1, 1, 0.1, 100)
        projection = tr.perspective(45, float(width)/float(height), 0.1, 100)

        camX = 6 * np.sin(camera_theta)
        camY = 6 * np.cos(camera_theta)

        viewPos = np.array([camX,camY,3])

        view = tr.lookAt(
            viewPos,
            np.array([0,0,0]),
            np.array([0,0,1])
        )

        rotation_theta = glfw.get_time()

        model = tr.identity()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)



        if -2*np.sin(theta_cola) <3 and -2*np.sin(theta_cola)>-11 :
            nemoCuerpoRotation.transform = tr.rotationZ(-0.5*np.sin(theta_cola))
            nemoCola1Rotation.transform = tr.rotationZ(-0.5*np.sin(theta_cola))
            nemoCola2Rotation.transform = tr.rotationZ(-0.6*np.sin(theta_cola))

            doriColaRotation.transform = tr.rotationZ(-np.sin(theta_cola))
            doriColaTranslation.transform = tr.translate(-1.1,0.2*np.sin(theta_cola),0)

            espadaCuerpoRotation.transform = tr.rotationZ(-0.5*np.sin(theta_cola))
            espadaColaRotation.transform = tr.rotationZ(-0.5*np.sin(theta_cola))
        theta_cola +=dt*5    


        # The axis is drawn without lighting effects
        glUseProgram(mvpPipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
        if controller.showAxis:
            mvpPipeline.drawShape(gpuAxis, GL_LINES)
        sg.drawSceneGraphNode(gpuDori, mvpPipeline, "model")
        sg.drawSceneGraphNode(gpuNemo, mvpPipeline, "model")
        sg.drawSceneGraphNode(gpuSwordfish, mvpPipeline, "model")
        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()