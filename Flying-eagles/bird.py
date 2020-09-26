
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders

import numpy as np
import sys  # para hacer handling de eventos, como entradas del sistema, o cerrar el programa.
import transformations as tr  # importa transformaciones
import easy_shaders as es  # importa shaders
import basic_shapes as bs # importa shapes
import lighting_shaders as ls # importa shaders
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

def cursor_pos_callback(window, x, y): # da la posición del mouse en pantalla con coordenadas
    global controller
    controller.mousePos =(x, y)


def createBird():

    gpuBlackCube = es.toGPUShape(bs.createColorNormalsCube(0.1,0.1,0.1))
    gpuWhiteCube = es.toGPUShape(bs.createColorNormalsCube(1,1,1))
    gpuGrayCube = es.toGPUShape(bs.createColorNormalsCube(0.8, 0.8, 0.8))
    gpuYellowCube = es.toGPUShape(bs.createColorNormalsCube(1 , 1, 0))

    torso = sg.SceneGraphNode("torso")
    torso.transform = tr.scale(1.7, 0.6, 0.5)
    torso.childs += [gpuBlackCube]

    torsoTranslation = sg.SceneGraphNode("torsoTranslation")
    torsoTranslation.childs += [torso]

    alaext = sg.SceneGraphNode("alaext")
    alaext.transform = tr.scale(0.8, 0.8, 0.1)
    alaext.childs += [gpuBlackCube]

    alaextRotation = sg.SceneGraphNode("alaextRotation")
    alaextRotation.childs += [alaext]

    alaextTranslation = sg.SceneGraphNode("alaextTranslation")
    alaextTranslation.childs += [alaextRotation]

    alaint = sg.SceneGraphNode("alaint")
    alaint.transform = tr.scale(0.8, 0.8, 0.1)
    alaint.childs += [gpuBlackCube]

    alaintRotation = sg.SceneGraphNode("alaintRotation")
    alaintRotation.childs += [alaint]
    
    alaintTranslation = sg.SceneGraphNode("alaintTranslation")
    alaintTranslation.childs += [alaintRotation]

    ala = sg.SceneGraphNode("ala")
    ala.childs += [alaintTranslation]
    ala.childs += [alaextTranslation]

    alaizq = sg.SceneGraphNode("alaizq")
    alaizq.transform = tr.translate(0, 0.5, 0)
    alaizq.childs += [ala]

    alader = sg.SceneGraphNode("alader")
    alader.transform = tr.matmul([tr.rotationZ(np.pi), tr.translate(0, 0.5, 0)])
    alader.childs += [ala]

    alas = sg.SceneGraphNode("alas")
    alas.childs += [alaizq]
    alas.childs += [alader]

    alasRotation = sg.SceneGraphNode("alasRotation")
    alasRotation.childs += [alas]

    cuello = sg.SceneGraphNode("cuello")
    cuello.transform =tr.matmul([tr.translate(1, 0, 0.1), tr.scale(0.5, 0.2, 0.2)])
    cuello.childs += [gpuGrayCube]

    cuelloRotation = sg.SceneGraphNode("cuelloRotation")
    cuelloRotation.childs += [cuello]
    
    cuelloTranslation = sg.SceneGraphNode("cuelloTranslation")
    cuelloTranslation.childs += [cuelloRotation]

    cabeza = sg.SceneGraphNode("cabeza")
    cabeza.transform =tr.matmul([tr.translate(1.3, 0, 0.3), tr.scale(0.5, 0.4, 0.4)])
    cabeza.childs += [gpuWhiteCube]

    pico = sg.SceneGraphNode("pico")
    pico.transform =tr.matmul([tr.translate(1.6, 0, 0.2), tr.scale(0.3, 0.17, 0.2)])
    pico.childs += [gpuYellowCube]

    ojoder = sg.SceneGraphNode("ojoder")
    ojoder.transform =tr.matmul([tr.translate(1.55, 0.1, 0.4), tr.scale(0.05, 0.05, 0.05)])
    ojoder.childs += [gpuBlackCube]

    ojoizq = sg.SceneGraphNode("ojoizq")
    ojoizq.transform =tr.matmul([tr.translate(1.55, -0.1, 0.4), tr.scale(0.05, 0.05, 0.05)])
    ojoizq.childs += [gpuBlackCube]

    cabezaTranslation = sg.SceneGraphNode("cabezaTranslation")
    cabezaTranslation.childs += [cabeza]
    cabezaTranslation.childs += [pico]
    cabezaTranslation.childs += [ojoizq]
    cabezaTranslation.childs += [ojoder]

    cola = sg.SceneGraphNode("cola")
    cola.transform =tr.scale(0.7, 0.5, 0.1)
    cola.childs += [gpuGrayCube]

    colaRotation = sg.SceneGraphNode("colaRotation")
    colaRotation.childs += [cola]

    colaTranslation = sg.SceneGraphNode("colaTranslation")
    colaTranslation.transform = tr.translate(-1, 0, 0)
    colaTranslation.childs +=[colaRotation]

    pataDown = sg.SceneGraphNode("pataDown")
    pataDown.transform = tr.matmul([tr.translate(0, 0, -0.2), tr.scale(0.1, 0.1, 0.2)])
    pataDown.childs += [gpuYellowCube]

    pataUp= sg.SceneGraphNode("pataUp")
    pataUp.transform = tr.matmul([tr.translate(0, 0, 0), tr.scale(0.2, 0.2, 0.2)])
    pataUp.childs += [gpuGrayCube]

    pata= sg.SceneGraphNode("pata")
    pata.childs += [pataDown]
    pata.childs += [pataUp]

    pataDer= sg.SceneGraphNode("pataDer")
    pataDer.transform = tr.translate(0, 0.14, -0.3)
    pataDer.childs += [pata]

    pataIzq= sg.SceneGraphNode("pataIzq")
    pataIzq.transform = tr.translate(0, -0.14, -0.3)
    pataIzq.childs += [pata]

    patas= sg.SceneGraphNode("patas")
    patas.transform = tr.matmul([tr.rotationY(np.pi/4), tr.scale(1.2, 1.2, 1.2)])
    patas.childs += [pataIzq]
    patas.childs += [pataDer]

    cuerpo = sg.SceneGraphNode("cuerpo")
    cuerpo.childs += [torsoTranslation]
    cuerpo.childs += [alasRotation]
    cuerpo.childs += [cuelloTranslation]
    cuerpo.childs += [cabezaTranslation]
    cuerpo.childs += [colaTranslation]
    cuerpo.childs += [patas]
    return cuerpo



if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 700

    window = glfw.create_window(width, height, "Lighting demo", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)
    glfw.set_cursor_pos_callback(window, cursor_pos_callback)

    # Different shader programs for different lighting strategies

    phongPipeline = ls.SimplePhongShaderProgram()

    # This shader program does not consider lighting
    mvpPipeline = es.SimpleModelViewProjectionShaderProgram()
    lightingPipeline = ls.SimplePhongShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    gpuAxis = es.toGPUShape(bs.createAxis(4))
    gpuBird = createBird()
    t0 = glfw.get_time()
    camera_theta = np.pi/4
    camera_thetaz = np.pi/4
    theta_alas = 0
#######################VARIABLES A MOVER
    alaintRotation = sg.findNode(gpuBird,"alaintRotation")
    alaextRotation = sg.findNode(gpuBird,"alaextRotation")
    alaintTranslation = sg.findNode(gpuBird,"alaintTranslation")
    alaextTranslation = sg.findNode(gpuBird,"alaextTranslation")
    colaRotation = sg.findNode(gpuBird,"colaRotation")
    colaTranslation = sg.findNode(gpuBird,"colaTranslation")

    cabezaTranslation = sg.findNode(gpuBird,"cabezaTranslation")
    cuelloRotation = sg.findNode(gpuBird,"cuelloRotation")
    cuelloTranslation = sg.findNode(gpuBird,"cuelloTranslation")
#####################WHILE
    while not glfw.window_should_close(window):

    # Using GLFW to check for input events
        glfw.poll_events()

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1    
    
############################CAMARA
        if (glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS):
            camera_theta -= 2 * dt

        if (glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS):
            camera_theta += 2* dt
        if (glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS):
            if camera_thetaz<1.5:
                camera_thetaz += 2* dt
        if (glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS):
            if camera_thetaz >-1.5:
                camera_thetaz -= 2* dt
        projection = tr.perspective(45, float(width)/float(height), 0.1, 100)

        camX = 6 * np.sin(camera_theta)
        camY = 6 * np.cos(camera_theta)
        camZ = 6 * np.sin(camera_thetaz)

        viewPos = np.array([camX,camY,camZ+2])

        view = tr.lookAt(
            viewPos,
            np.array([0,0,0]),
            np.array([0,0,1])
        )
#################################

#############MOVIMIENTO CON EL MOUSE
        if controller.mousePos == 0:
            mouseX= 0
            mouseY= 0
        else:
            mouseX,  mouseY = controller.mousePos
        mouseX= mouseX/width
        mouseY= mouseY/height
        theta_alas = np.pi-mouseY*2*np.pi
        if theta_alas>=1.4:
            theta_alas=1.4
        if theta_alas<=-1.4:
            theta_alas=-1.4
        alaintRotation.transform = tr.rotationX(theta_alas/4)
        alaextRotation.transform = tr.rotationX(theta_alas/2)

        alaintTranslation.transform = tr.translate(0,0.15,0.15*np.sin(theta_alas))
        alaextTranslation.transform = tr.translate(0,0.8+np.cos(theta_alas)*0.1,0.55*np.sin(theta_alas))

        colaRotation.transform = tr.rotationY(theta_alas/4)
        colaTranslation.transform = tr.translate(-1,0,0.1*np.sin(theta_alas))
        movcabeza = mouseY/1.2-0.6
        if movcabeza >=0:
            movcabeza =0

        if movcabeza <=-0.4:
            movcabeza =-0.4
        cabezaTranslation.transform = tr.translate(0,0,movcabeza)

        cuelloRotation.transform = tr.rotationY(theta_alas/4)
        cuelloTranslation.transform = tr.translate(0.1,0,0.2*np.sin(theta_alas))

##############################

###########DIBUJAR LOS AXIS

        axis = np.array([1,-1,1])
        axis = axis / np.linalg.norm(axis)
        model = tr.identity()
        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # The axis is drawn without lighting effects
        if controller.showAxis:
            glUseProgram(mvpPipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
            mvpPipeline.drawShape(gpuAxis, GL_LINES)

#################################

###############DIBUJAR EL AGUILA
        glUseProgram(lightingPipeline.shaderProgram)

        # White light in all components: ambient, diffuse and specular.
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ls"), 1.0, 1.0, 0)

        # Object is barely visible at only ambient.
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ka"), 0.8, 0.8, 0.8)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Kd"), 0.5, 0.5, 0)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

        # TO DO: Explore different parameter combinations to understand their effect!

        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "lightPosition"), -5, -5, 5)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "viewPosition"), viewPos[0], viewPos[1], viewPos[2])
        glUniform1ui(glGetUniformLocation(lightingPipeline.shaderProgram, "shininess"), 100)
        
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "constantAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "linearAttenuation"), 0.03)
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "quadraticAttenuation"), 0.01)

        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "model"), 1, GL_TRUE, model)

        # Drawing
        sg.drawSceneGraphNode(gpuBird, lightingPipeline, "model")
        
        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()
