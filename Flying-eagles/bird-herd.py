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
import bird
import gpu_creations as cr
import csv

#archivo=input('Introduce nombre del csv: ')
#archivo='path2.csv'
archivo= sys.argv[1]

#####PONER EN EL INFORME QUE EL ULTIMO Y PRIMER PUNTO NO SE USAN
######HAY PEQUEÑOS FRAMES QUE SE VAN PORQUE LOS DZ;DX;DY SON MUY PEQUEÑOS

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

###################BIRDS
def birds(): #Crea la bandada de pajaros usando bird.py
    bird1 = sg.SceneGraphNode("bird1")
    bird1.transform = tr.uniformScale(0.04)
    bird1.childs += [bird.createBird()]
    bird2 = sg.SceneGraphNode("bird2")
    bird2.transform = tr.uniformScale(0.04)
    bird2.childs += [bird.createBird()]
    bird3 = sg.SceneGraphNode("bird3")
    bird3.transform = tr.uniformScale(0.04)
    bird3.childs += [bird.createBird()]
    bird4 = sg.SceneGraphNode("bird4")
    bird4.transform = tr.uniformScale(0.04)
    bird4.childs += [bird.createBird()]
    bird5 = sg.SceneGraphNode("bird5")
    bird5.transform = tr.uniformScale(0.04)
    bird5.childs += [bird.createBird()]

    bird1Rotation = sg.SceneGraphNode("bird1Rotation")
    bird1Rotation.childs += [bird1]
    bird2Rotation = sg.SceneGraphNode("bird2Rotation")
    bird2Rotation.childs += [bird2]
    bird3Rotation = sg.SceneGraphNode("bird3Rotation")
    bird3Rotation.childs += [bird3]
    bird4Rotation = sg.SceneGraphNode("bird4Rotation")
    bird4Rotation.childs += [bird4]
    bird5Rotation = sg.SceneGraphNode("bird5Rotation")
    bird5Rotation.childs += [bird5]

    bird1Translation = sg.SceneGraphNode("bird1Translation")
    bird1Translation.childs += [bird1Rotation]
    bird2Translation = sg.SceneGraphNode("bird2Translation")
    bird2Translation.childs += [bird2Rotation]
    bird3Translation = sg.SceneGraphNode("bird3Translation")
    bird3Translation.childs += [bird3Rotation]
    bird4Translation = sg.SceneGraphNode("bird4Translation")
    bird4Translation.childs += [bird4Rotation]
    bird5Translation = sg.SceneGraphNode("bird5Translation")
    bird5Translation.childs += [bird5Rotation]

    
    bird2Translation.transform = tr.translate(-0.2, 0.2, 0)
    bird3Translation.transform = tr.translate(-0.4, 0.4, 0)
    bird4Translation.transform = tr.translate(-0.2, -0.2, 0)
    bird5Translation.transform = tr.translate(-0.4, -0.4, 0)


    birds = sg.SceneGraphNode("birds")
    birds.childs += [bird1Translation]
    birds.childs += [bird2Translation]
    birds.childs += [bird3Translation]
    birds.childs += [bird4Translation]
    birds.childs += [bird5Translation]
    
    birdsRotation = sg.SceneGraphNode("birdsRotation")
    birdsRotation.childs += [birds]

    birdsTranslation = sg.SceneGraphNode("birdsTranslation")
    birdsTranslation.childs += [birdsRotation]

    

    return birdsTranslation

####################CURVA
def generateT(t): #Genera el vector con los t
    return np.array([[1, t, t**2, t**3]]).T

def catmullRomMatrix(P0,P1,P2,P3): #Crea una matriz de Catmull Rom tomando 4 puntos
    G = np.concatenate((np.array([P0]).T,np.array([P1]).T,np.array([P2]).T,np.array([P3]).T), axis=1)
    Mcr = np.array([[0, -1/2, 2/2, -1/2], [2/2, 0, -5/2, 3/2], [0, 1/2, 4/2, -3/2], [0, 0, -1/2, 1/2]])

    return np.matmul(G, Mcr)

def evalCurve(M, N):     #Crea la curva de Catmull Rom usando la matriz recien creada y N puntos
    # The parameter t should move between 0 and 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(N, 3), dtype=float)
    
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(M, T).T
        
    return curve

def catmullRomChain(puntos, N): #Crea una cadena de Catmull Rom con N puntos, tomando puntos dados
    sz = len(puntos)

    C = []
    for i in range(sz-3):
        matrix = catmullRomMatrix(puntos[i],puntos[i+1],puntos[i+2],puntos[i+3]) #usamos los 4 puntos que utiliza Catmull Rom
        c = evalCurve(matrix,N)
        C.extend(c)

    return C #Retorna la cadena de puntos en una lista

def csvReader(archivo):  #Lee archivo csv con puntos en 3 dimensiones y los guarda en un arreglo
    with open(archivo) as File:
        
        numeros=[]
        reader = csv.reader(File, delimiter=',', quotechar=',',
                            quoting=csv.QUOTE_MINIMAL)
        contador= 0
        contador2= 0
        for row in reader:
            numeros += [[0,0,0]]
            for j in row:
                numeros[contador][contador2] = float(j)
                contador2+=1
            contador+=1
            contador2=0
        
        return numeros

puntos = csvReader(archivo) #Leemos el csv y guardamos puntos
Cadena = catmullRomChain(puntos,len(puntos)*100) #Creamos la cadena de Catmull Rom con N puntos intermedios

############################### MAIN
if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 1024
    height = 720

    window = glfw.create_window(width, height, "Animación Águilas", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)
    glfw.set_cursor_pos_callback(window, cursor_pos_callback)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED) #Escondemos el mouse

    # Different shader programs for different lighting strategies
    phongPipeline = ls.SimplePhongShaderProgram()
    mvpPipeline = es.SimpleTextureModelViewProjectionShaderProgram()
    lightingPipeline = ls.SimplePhongShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)
    # Creating shapes on GPU memory

    gpuAxis = es.toGPUShape(bs.createAxis(4))
    gpuBirds = birds()
    gpuBird1 = sg.findNode(gpuBirds,"bird1Translation")
    gpuBird2 = sg.findNode(gpuBirds,"bird2Translation")
    gpuBird3 = sg.findNode(gpuBirds,"bird3Translation")
    gpuBird4 = sg.findNode(gpuBirds,"bird4Translation")
    gpuBird5 = sg.findNode(gpuBirds,"bird5Translation")
    
    skybox_image = cr.ImageObject("skyboxTarea2.png")
    skyNode = sg.SceneGraphNode("Sky")
    skyNode.childs += [cr.createSkybox(skybox_image, 512, 10)]

    #iniciamos las variables a usar
    camera_theta = np.pi/4
    camera_thetaz = np.pi/4
    t0 = glfw.get_time()
    theta_alas1 =0
    theta_alas2 =0.5
    theta_alas3 =2
    theta_alas4 =-0.9
    theta_alas5 =-3
    contador_cadenaCurva=0

    phi_mov = 0
    theta_mov = 0

    pos_0 = puntos[0]
    pos_1 = [0, 0, 0]
#############VARIABLES A MOVER
    alaintRotation1 = sg.findNode(gpuBird1,"alaintRotation")
    alaextRotation1 = sg.findNode(gpuBird1,"alaextRotation")
    alaextTranslation1 = sg.findNode(gpuBird1,"alaextTranslation")
    colaRotation1 = sg.findNode(gpuBird1,"colaRotation")
    cabezaTranslation1 = sg.findNode(gpuBird1,"cabezaTranslation")
    cuelloRotation1 = sg.findNode(gpuBird1,"cuelloRotation")

    alaintRotation2 = sg.findNode(gpuBird2,"alaintRotation")
    alaextRotation2 = sg.findNode(gpuBird2,"alaextRotation")
    alaextTranslation2 = sg.findNode(gpuBird2,"alaextTranslation")
    colaRotation2 = sg.findNode(gpuBird2,"colaRotation")
    cabezaTranslation2 = sg.findNode(gpuBird2,"cabezaTranslation")
    cuelloRotation2 = sg.findNode(gpuBird2,"cuelloRotation")

    alaintRotation3 = sg.findNode(gpuBird3,"alaintRotation")
    alaextRotation3 = sg.findNode(gpuBird3,"alaextRotation")
    alaextTranslation3 = sg.findNode(gpuBird3,"alaextTranslation")
    colaRotation3 = sg.findNode(gpuBird3,"colaRotation")
    cabezaTranslation3 = sg.findNode(gpuBird3,"cabezaTranslation")
    cuelloRotation3 = sg.findNode(gpuBird3,"cuelloRotation")

    alaintRotation4 = sg.findNode(gpuBird4,"alaintRotation")
    alaextRotation4 = sg.findNode(gpuBird4,"alaextRotation")
    alaextTranslation4 = sg.findNode(gpuBird4,"alaextTranslation")
    colaRotation4 = sg.findNode(gpuBird4,"colaRotation")
    cabezaTranslation4 = sg.findNode(gpuBird4,"cabezaTranslation")
    cuelloRotation4 = sg.findNode(gpuBird4,"cuelloRotation")

    alaintRotation5 = sg.findNode(gpuBird5,"alaintRotation")
    alaextRotation5 = sg.findNode(gpuBird5,"alaextRotation")
    alaextTranslation5 = sg.findNode(gpuBird5,"alaextTranslation")
    colaRotation5 = sg.findNode(gpuBird5,"colaRotation")
    cabezaTranslation5 = sg.findNode(gpuBird5,"cabezaTranslation")
    cuelloRotation5 = sg.findNode(gpuBird5,"cuelloRotation")

    birdsTranslation = sg.findNode(gpuBirds, "birdsTranslation")
    birdsRotation = sg.findNode(gpuBirds, "birdsRotation")

#WHILE
    while not glfw.window_should_close(window):

    # Using GLFW to check for input events
        glfw.poll_events()

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1
            
#############MOVIMIENTO DEL MOUSE
        #MouseX y MouseY dan la posicion del mouse, de 0 a 1
        if controller.mousePos == 0:
            mouseX= np.pi/4
            mouseY= np.pi/2.5
        else:
            mouseX,  mouseY = controller.mousePos   #Escalamos la posición del mouse ne la pantalla a un dominio[0,1]
            mouseX= mouseX/width
            mouseY= mouseY/height
        if mouseY <=0.1:
            mouseY=0.1
        if mouseY >=0.9:
            mouseY=0.9
#############CAMARA
        #La cámara estará en viewPos, fija, y rotará con la posición del mouse transformada
        #a ángulos, que posteriormente se transformarán en coord. esfericas

        projection = tr.perspective(45, float(width)/float(height), 0.1, 100)
        viewPos = np.array([0,0,0])     #La posición de la cámara puede ser cualquiera, luego el LookAt mueve su centro según la posición de la cámara

        theta=mouseY*np.pi       #definimos un theta y un phi que permitiran mover la cámara con el mouse, los obtenemos transformando el dominio[0,1] del mouse en [0,pi] o [0,2pi] segun el ángulo
        phi=mouseX*np.pi*2+np.pi
        
        view = tr.lookAt(
            viewPos, 
            np.array([-5*np.sin(theta)*np.cos(phi)+viewPos[0],5*np.sin(theta)*np.sin(phi)+viewPos[1],5*np.cos(theta)+viewPos[2]]), #Usamos esféricas para mover el LookAt
            np.array([0,0,1]))

#############MOVIMIENTO ALAS  
        #Movemos todas las aguilas, y es necesario entrar a cada nodo de bird en gpuBirds() para moverlas todas     

        dt1 = dt*8
        dt2 = dt*5
        dt3 = dt*4
        dt4 = dt*7
        dt5 = dt*3

        if -2*np.sin(theta_alas1) <1.2 and -2*np.sin(theta_alas1)>-1.2 :
            alaintRotation1.transform = tr.rotationX(-np.sin(theta_alas1))
            alaextRotation1.transform = tr.rotationX(-1.5*np.sin(theta_alas1))
            colaRotation1.transform = tr.rotationY(0.5*np.sin(theta_alas1))
            cabezaTranslation1.transform = tr.translate(0,0,-np.sin(theta_alas1)/3)
            cuelloRotation1.transform = tr.rotationY(0.2*np.sin(theta_alas1))
            alaextTranslation1.transform = tr.translate(0,0.6,-0.9*np.sin(theta_alas1))
        
        else:
            dt1+=0.2

        if -2*np.sin(theta_alas2) <1.2 and -2*np.sin(theta_alas2)>-1.2 :
            alaintRotation2.transform = tr.rotationX(-np.sin(theta_alas2))
            alaextRotation2.transform = tr.rotationX(-1.5*np.sin(theta_alas2))
            colaRotation2.transform = tr.rotationY(0.5*np.sin(theta_alas2))
            cabezaTranslation2.transform = tr.translate(0,0,-np.sin(theta_alas2)/3)
            cuelloRotation2.transform = tr.rotationY(0.2*np.sin(theta_alas2))
            alaextTranslation2.transform = tr.translate(0,0.6,-0.9*np.sin(theta_alas2))

        else:
            dt2+=0.2

        if -2*np.sin(theta_alas3) <1.2 and -2*np.sin(theta_alas3)>-1.2 :
            alaintRotation3.transform = tr.rotationX(-np.sin(theta_alas3))
            alaextRotation3.transform = tr.rotationX(-1.5*np.sin(theta_alas3))
            colaRotation3.transform = tr.rotationY(0.5*np.sin(theta_alas3))
            cabezaTranslation3.transform = tr.translate(0,0,-np.sin(theta_alas3)/3)
            cuelloRotation3.transform = tr.rotationY(0.2*np.sin(theta_alas3))
            alaextTranslation3.transform = tr.translate(0,0.6,-0.9*np.sin(theta_alas3))

        else:
            dt3+=0.2

        if -2*np.sin(theta_alas4) <1.2 and -2*np.sin(theta_alas4)>-1.2 :
            alaintRotation4.transform = tr.rotationX(-np.sin(theta_alas4))
            alaextRotation4.transform = tr.rotationX(-1.5*np.sin(theta_alas4))
            colaRotation4.transform = tr.rotationY(0.5*np.sin(theta_alas4))
            cabezaTranslation4.transform = tr.translate(0,0,-np.sin(theta_alas4)/3)
            cuelloRotation4.transform = tr.rotationY(0.2*np.sin(theta_alas4))
            alaextTranslation4.transform = tr.translate(0,0.6,-0.9*np.sin(theta_alas4))

        else:
            dt4+=0.2

        if -2*np.sin(theta_alas5) <1.2 and -2*np.sin(theta_alas5)>-1.2 :
            alaintRotation5.transform = tr.rotationX(-np.sin(theta_alas5))
            alaextRotation5.transform = tr.rotationX(-1.5*np.sin(theta_alas5))
            colaRotation5.transform = tr.rotationY(0.5*np.sin(theta_alas5))
            cabezaTranslation5.transform = tr.translate(0,0,-np.sin(theta_alas5)/3)
            cuelloRotation5.transform = tr.rotationY(0.2*np.sin(theta_alas5))
            alaextTranslation5.transform = tr.translate(0,0.6,-0.9*np.sin(theta_alas5))

        else:
            dt5+=0.2
        
        
        theta_alas1 +=dt1
        theta_alas2 +=dt2
        theta_alas3 +=dt3
        theta_alas4 +=dt4
        theta_alas5 +=dt5

#############MOVIMIENTO AGUILAS
        #Movemos las aguilas a través de la cadena de Catmull Rom
        if contador_cadenaCurva<len(Cadena): #Mientras no se recorra toda la cadena
            birdsTranslation.transform = tr.translate(Cadena[contador_cadenaCurva][0],Cadena[contador_cadenaCurva][1],Cadena[contador_cadenaCurva][2])
            pos_1 = sg.findPosition(gpuBirds, "birdsRotation") #Guardamos la posición en pos_1

            #Guardamos las diferencias de posicion entre un instante y otro
            dx = pos_1[0] - pos_0[0]
            dy = pos_1[1] - pos_0[1]
            dz = pos_1[2] - pos_0[2]

            #Pasamos las diferencias de posicion a coordenadas esfericas
            if dz>0:
                theta_mov = 3*np.pi/2 + np.arctan(np.sqrt(dx**2+dy**2)/dz)
            elif dz<0:
                theta_mov =  3*np.pi/2 +np.pi + np.arctan(np.sqrt(dx**2+dy**2)/dz)
            
            if dx>=0 and dy>0:
                phi_mov = np.arctan(dy/dx)
            if dx>0 and dy<0:
                phi_mov = 2*np.pi + np.arctan(dy/dx)
            if dx ==0:
                phi_mov = np.pi/2 * np.sign(dy)
            if dx<0:
                phi_mov = np.pi + np.arctan(dy/dx)

            #Rotamos las aguilas con los angulos obtenidos por coordenadas esfericas
            birdsRotation.transform = tr.matmul([tr.rotationZ(phi_mov),tr.rotationY(theta_mov)])

            pos_0 = pos_1 #Actualizarmos la posicion "anterior" y el contador de dónde vamos en la cadena
            contador_cadenaCurva+=1

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

###############DIBUJAR AGUILAS
        #Se dibujan con efectos de luz
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

        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "lightPosition"), 5, 5, 5)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "viewPosition"), viewPos[0], viewPos[1], viewPos[2])
        glUniform1ui(glGetUniformLocation(lightingPipeline.shaderProgram, "shininess"), 100)
        
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "constantAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "linearAttenuation"), 0.03)
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "quadraticAttenuation"), 0.01)

        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "model"), 1, GL_TRUE, model)

        sg.drawSceneGraphNode(gpuBirds, lightingPipeline, "model")

        glUseProgram(mvpPipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        sg.drawSceneGraphNode(skyNode, mvpPipeline, "model")

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()