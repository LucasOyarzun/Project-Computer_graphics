import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys

import transformations as tr
import basic_shapes as bs
import easy_shaders as es
import scene_graph as sg
import random as rand

#NOTA POR SI VUELVO A TOCAR ESTE CÓDIGO: SE PUEDE MEJORAR, HACIENDO QUE EL FONDO AL LLEGAR ABAJO, LAS ESTRELLAS SE DEVUELVAN ARRIBA(COMO EL ENEMIGO)
#PARA NO HACER COMO 800 ESTRELLAS, SINO QUE UNAS 20 QUE BAJEN Y AL LLEGAR A CIERTO PUNTO, SUBAN A LA POSICION INICIAL, CON LOS PLANETAS LO MISMO
#TAMBIEN SE PUEDE HACER UNA LISTA DE UNAS 10 BALAS, QUE AL LLEGAR A CIERTO PUNTO, VUELVAN DONDE EL ENEMIGO Y SE LANCEN DENUEVO
#PARA EVITAR EL LAG

N= sys.argv[1]
#N=input('Introduce cantidad de enemigos: ') # (PARA EJECUTAR EL CODIGO SIN EL PROMPT)
N= int(N)
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.x = 0.0
        self.y = 0.0
        self.shoot = False #Para cambiarlo al apretar espacio

controller = Controller()

#Definimos lo que hará cada tecla
def on_key(window, key, scancode, action, mods):

    global controller

    
    if action == glfw.REPEAT or action == glfw.PRESS:

        if key == glfw.KEY_A:
            controller.x -= 0.1

        if key == glfw.KEY_D:
            controller.x += 0.1

        if key == glfw.KEY_W:
            controller.y += 0.1

        if key == glfw.KEY_S:
            controller.y -= 0.1

    if action == glfw.PRESS:
        if key == glfw.KEY_SPACE:
                controller.shoot = True
    

    if key == glfw.KEY_ESCAPE:
        sys.exit()

def createUserBullets(): #Crea balas del usuario

    gpuYellowQuad = es.toGPUShape(bs.createColorQuad(1, 1, 0))

    bullet =sg.SceneGraphNode("bullet")
    bullet.transform = tr.matmul([tr.translate(-0.0005,0,0),tr.uniformScale(0.01),tr.scale(1,5,0)])
    bullet.childs +=[gpuYellowQuad]

    translatedBullet = sg.SceneGraphNode("translatedBullet") #Para que vayan hacia adelante las balas, transform se modifica despues
    translatedBullet.transform = tr.identity() 
    translatedBullet.childs += [bullet]

    translatedBullet2 = sg.SceneGraphNode("translatedBullet2") #No me acuerdo por que es necesario tener translatedBullet2
    translatedBullet2.childs +=[translatedBullet]

    return translatedBullet2

def createEnemieBullets(): #Crea balas de los enemigos

    gpuRedQuad = es.toGPUShape(bs.createColorQuad(1, 0, 0))

    bullet =sg.SceneGraphNode("bullet")
    bullet.transform = tr.matmul([tr.translate(-0.0005,0,0),tr.uniformScale(0.01),tr.scale(1,5,0)])
    bullet.childs +=[gpuRedQuad]

    translatedBullet = sg.SceneGraphNode("translatedBullet") #Para que vayan hacia adelante las balas, transform se modifica despues
    translatedBullet.transform = tr.identity() 
    translatedBullet.childs += [bullet]

    translatedBullet2 = sg.SceneGraphNode("translatedBullet2") #Para que se posicionen en el enemigo
    translatedBullet2.childs +=[translatedBullet]

    return translatedBullet2

#Creamos la forma de los enemigos
def createEnemie():

    gpuGreyQuad = es.toGPUShape(bs.createColorQuad(0.8, 0.8, 0.8))
    gpuRedQuad = es.toGPUShape(bs.createColorQuad(1, 0, 0))
    gpuDarkGreyTriangle = es.toGPUShape(bs.createTriangle(0.2, 0.2, 0.2))
    

    # Cheating a single side
    side = sg.SceneGraphNode("side")
    side.transform = tr.scale( 0.2, 0.8, 0)
    side.childs += [gpuGreyQuad]

    sideTraslation = sg.SceneGraphNode("sideTraslation")
    sideTraslation.transform = tr.translate(0, -0.2, 0)
    sideTraslation.childs += [side]

    # Instanciating 2 armors, right and left
    rightSide = sg.SceneGraphNode("rightSide")
    rightSide.transform = tr.translate(0.3,-0.3,0)
    rightSide.childs += [sideTraslation]

    leftSide = sg.SceneGraphNode("leftSide")
    leftSide.transform = tr.translate(-0.3,-0.3,0)
    leftSide.childs += [sideTraslation]
    
    # Creating the chasis of the enemie
    chasis = sg.SceneGraphNode("chasis")
    chasis.transform = tr.matmul([tr.uniformScale(1.3),tr.scale(0.6,0.8,1)])
    chasis.childs += [gpuDarkGreyTriangle]

    #Creatinf the cannon of the enemie
    cannon = sg.SceneGraphNode("cannon")
    cannon.transform = tr.scale(0.1, 0.4, 0)
    cannon.childs += [gpuRedQuad]

    cannonTraslation = sg.SceneGraphNode("cannonTraslation")
    cannonTraslation.transform = tr.translate(0, 0.45, 0)
    cannonTraslation.childs += [cannon]


    enemie = sg.SceneGraphNode("enemie")
    enemie.transform = tr.matmul([tr.rotationZ(np.pi),tr.uniformScale(0.15)])
    
    enemie.childs += [cannonTraslation]
    enemie.childs += [chasis]
    enemie.childs += [rightSide]
    enemie.childs += [leftSide]
    
    translatedEnemie = sg.SceneGraphNode("translatedEnemie")
    translatedEnemie.transform = tr.translate(0,2.0,0)
    translatedEnemie.childs += [enemie]

    return translatedEnemie

#Creamos planetas
def createPlanets():

    gpuRainbowQuad = es.toGPUShape(bs.createColorQuad(0.5,0.8,0))

    planet =sg.SceneGraphNode("planet")
    planet.transform =tr.uniformScale(0.1)
    planet.childs +=[gpuRainbowQuad]

    translatedPlanet = sg.SceneGraphNode("translatedPlanet")
    translatedPlanet.transform = tr.identity()
    translatedPlanet.childs +=[planet]
    

    planets = sg.SceneGraphNode("planets")

    baseName = "Planet"
    for i in range(10):
        # A new node is only locating a scaledEnemie in the scene depending on index i
        newNode = sg.SceneGraphNode(baseName + str(i))
        
        newNode.transform = tr.translate(rand.random()*2-1, i/2, 0)
        newNode.childs += [translatedPlanet]
        
        # Now this enemie is added to the 'enemies' scene graph
        planets.childs += [newNode]
    return planets

#Creamos estrellas
def createStars(N):

    gpuWhiteQuad = es.toGPUShape(bs.createColorQuad(1, 1, 1))

    star =sg.SceneGraphNode("star")
    star.transform =tr.matmul([tr.translate(0, -0.5, 0),tr.uniformScale(0.015)])
    star.childs +=[gpuWhiteQuad]

    translatedStar = sg.SceneGraphNode("translatedStar")
    translatedStar.transform = tr.identity()
    translatedStar.childs +=[star]
    

    stars = sg.SceneGraphNode("stars")

    baseName = "Star"
    for i in range(N*15):
        # A new node is only locating a scaledEnemie in the scene depending on index i
        newNode = sg.SceneGraphNode(baseName + str(i))
        
        newNode.transform = tr.translate(rand.random()*2-1, i/6, 0)
        newNode.childs += [translatedStar]
        
        # Now this enemie is added to the 'enemies' scene graph
        stars.childs += [newNode]
    return stars

#Creamos usuario
def createUser():

    gpuGreyQuad = es.toGPUShape(bs.createColorQuad(0.8, 0.8, 0.8))
    gpuBlueQuad = es.toGPUShape(bs.createColorQuad(0, 0, 1))
    gpuDarkGreyTriangle = es.toGPUShape(bs.createTriangle(0.2, 0.2, 0.2))
    gpuYellowQuad = es.toGPUShape(bs.createColorQuad(1, 1, 0))

    # Cheating a single side
    side = sg.SceneGraphNode("side")
    side.transform = tr.scale( 0.2, 0.8, 0)
    side.childs += [gpuGreyQuad]

    sideTraslation = sg.SceneGraphNode("sideTraslation")
    sideTraslation.transform = tr.translate(0, -0.2, 0)
    sideTraslation.childs += [side]

    # Instanciating 2 armors, right and left
    rightSide = sg.SceneGraphNode("rightSide")
    rightSide.transform = tr.translate(0.3,-0.3,0)
    rightSide.childs += [sideTraslation]

    leftSide = sg.SceneGraphNode("leftSide")
    leftSide.transform = tr.translate(-0.3,-0.3,0)
    leftSide.childs += [sideTraslation]
    
    # Creating the chasis of the enemie
    chasis = sg.SceneGraphNode("chasis")
    chasis.transform = tr.matmul([tr.uniformScale(1.3),tr.scale(0.6,0.8,1)])
    chasis.childs += [gpuDarkGreyTriangle]

    #Creatinf the cannon of the enemie
    cannon = sg.SceneGraphNode("cannon")
    cannon.transform = tr.scale(0.1, 0.4, 0)
    cannon.childs += [gpuBlueQuad]

    cannonTraslation = sg.SceneGraphNode("cannonTraslation")
    cannonTraslation.transform = tr.translate(0, 0.45, 0)
    cannonTraslation.childs += [cannon]

    user = sg.SceneGraphNode("user")
    user.transform = tr.uniformScale(0.15)
    
    user.childs += [cannonTraslation]
    user.childs += [chasis]
    user.childs += [rightSide]
    user.childs += [leftSide]
    
    translatedUser2 = sg.SceneGraphNode("translatedUser2") #Posicion inicial
    translatedUser2.transform = tr.identity()
    translatedUser2.childs += [user]

    translatedUser = sg.SceneGraphNode("translatedUser") #Translated User que moveremos con las teclas
    translatedUser.transform = tr.identity()
    translatedUser.childs += [translatedUser2]

    return translatedUser

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Space-War", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program (pipeline) with both shaders

    pipeline = es.SimpleTransformShaderProgram() #Pipeline para el juego
    pipeline2 = es.SimpleTextureTransformShaderProgram() #pipeline para el GAME OVER
    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0, 0, 0, 1.0)

    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    # Creating shapes on GPU memory
    CONTADOR_ENEMIGOS=N #Contadores de enemigos y vida
    CONTADOR_VIDAS=3

    stars= createStars(N) #Dejamos los elementos en la GPU
    planets = createPlanets()
    enemie = createEnemie()
    user = createUser()

    balasUsuario= createUserBullets() #Conjunto de balas del usuario
    contadorBalasUsuario= 0 #Contador de balas del usuario

    balasEnemigos = createEnemieBullets() #Conjunto de balas del enemigo
    contadorBalasEnemigo=0 #Contador de balas del enemigo

    alfa=0#Para guardar valores temporales de theta
    beta=0

    while not glfw.window_should_close(window):

        if CONTADOR_VIDAS<=0: #Si las vidas baja a cero, se muestra el GAME OVER

            glUseProgram(pipeline2.shaderProgram)
            GAMEOVER =es.toGPUShape(bs.createTextureQuad("GAMEOVER.png", 261/1040, 516/1040, 2/369, 225/369), GL_REPEAT, GL_NEAREST) #Sprite de GAME OVER

            glUseProgram(pipeline2.shaderProgram)
            glfw.poll_events()
                
            glClear(GL_COLOR_BUFFER_BIT)
            theta2 = glfw.get_time()
            tx2 = np.cos(4*theta2)
            ty2 = np.sin(4*theta2)
                
            if tx2>=0 or ty2>=0: #Para darle tiempo (aparecer-desaparecer)
                glUniformMatrix4fv(glGetUniformLocation(pipeline2.shaderProgram, "transform"), 1, GL_TRUE,tr.uniformScale(2.2))
                pipeline2.drawShape(GAMEOVER) #Dibuja el GAME OVER

        else:#Si quedan vidas
            if CONTADOR_ENEMIGOS==0:
                sys.exit()
            # Using GLFW to check for input events
            glfw.poll_events()
            # Clearing the screen in both, color and depth
            glClear(GL_COLOR_BUFFER_BIT)

            #Obtenemos los parámetros para el movimiento
            theta = glfw.get_time()#Parámetro de tiempo
            tx = 0.9* np.sin(theta*1.3)#Parámetro sinusoidal del tiempo
            ty = 0.3 * np.sin(3 * theta)

            #Movemos y creamos las estrellas y planetas

            stars.transform = tr.translate(0, -theta/10, 0) #Mvimiento continuo

            planets.transform = tr.translate(0, -theta/10, 0) #Movimiento continuo
            
            sg.drawSceneGraphNode(stars, pipeline, "transform",tr.translate(0, -theta/10,0)) # Le da el movimiento hacia abajo al fondo

            sg.drawSceneGraphNode(planets, pipeline, "transform",tr.translate(0, -theta/10,0)) # Le da el movimiento hacia abajo al fondo

            #Movemos y creamos el enemigo

            enemie.transform = tr.translate(tx+beta, 2.0-theta+alfa+ty,0) #Transformacion del enemigo, con un alfa que se ocupa para elevarlo despues

            if sg.findPosition(enemie, "translatedEnemie")[1][0]<= 0.7+ty: #Si la posicion es 0.7 en y, lo deja a esa altura
                enemie.transform = tr.translate(tx+beta, 0.7+ty,0)

            #Movemos y creamos al usuario

            user.transform = tr.matmul([tr.translate(controller.x, controller.y,0),tr.translate(0,-0.8,0)])#Registra la posicion del jugador

            #Movemos y creamos las balas
            balasUsuario.transform = tr.translate(0, theta*2,0)#Movimiento continuo hacia arriba de las balas
            translatedBullet = sg.findNode(balasUsuario, "translatedBullet")
            translatedBullet.transform = tr.translate(0, 0,0)

            balasEnemigos.transform= tr.translate(0,-theta, 0)#movimiento de las balas
            translatedBulletEnemie = sg.findNode(balasEnemigos, "translatedBullet")
            translatedBulletEnemie.transform = tr.translate(0, 0 , 0)

            #Posiciones de las naves
            posicionEnemigo =sg.findPosition(enemie, "translatedEnemie")
            posicion_user=sg.findPosition(user, "translatedUser")

            #Creamos las balas del ususario
            if controller.shoot ==True:#Cuando apretamos Espacio
                posicionUsuario = [sg.findPosition(user, "translatedUser")[0]*2+0.005,sg.findPosition(user, "translatedUser")[1]*2+0.88] #ajuste feo de la posicion del usuario
            
                balanueva =sg.SceneGraphNode("balanueva" + str(contadorBalasUsuario)) #creamos una bala nueva
                balanueva.transform = tr.translate(controller.x,controller.y-theta*2-0.7, 0) #posicionamos la bala nueva en el usuario
                balanueva.childs +=[translatedBullet] #pasamos a las balas las caracteristicas de translatedBullet
                balasUsuario.childs +=[balanueva] #agregamos a las balas
                contadorBalasUsuario +=1#aumentamos el contador de balas
            controller.shoot =False

            #Creamos las balas del enemigo
            if posicionEnemigo[1][0]<=1.0 and theta%0.5<=0.1 :
                balanuevaEnemigo =sg.SceneGraphNode("balanuevaEnemigo" + str(contadorBalasEnemigo)) #creamos una bala nueva 
                balanuevaEnemigo.transform = tr.translate(posicionEnemigo[0],posicionEnemigo[1]+theta-0.08, 0) #posicionamos la bala nueva en el enemigo
                balanuevaEnemigo.childs +=[translatedBulletEnemie] #pasamos a las balas las caracteristicas de translatedBullet2
                balasEnemigos.childs +=[balanuevaEnemigo] #agregamos a las balas
                contadorBalasEnemigo+=1#aumentamos el contador de balas

            #Definimos el comportamiento en los choques
            for i in range(contadorBalasUsuario): #Para chocar un enemigo
                posicionBala = sg.findPosition(balasUsuario, "balanueva" + str(i))#posicion de las balas
                if abs(posicionBala[0][0]-posicionEnemigo[0][0])<=0.09 and abs(posicionBala[1][0]-posicionEnemigo[1][0])<=0.1 and posicionEnemigo[1][0]<=1.0:
                    alfa=theta #Guardamos el theta de vuando chocan
                    balita = sg.findNode(balasUsuario, "balanueva" + str(i))
                    balita.transform = tr.translate(2.0, 0, 0) #si chocan movemos la bala hacia afuera de la pantalla
                    enemie.transform = tr.translate(0, 2.0, 0) #si chocan movemos, al enemigo hacia arirba
                    CONTADOR_ENEMIGOS-=1
                    
                    if CONTADOR_ENEMIGOS <=0: #Si el contador de enemigos llega a 0, mandamos al enemigo afuera de la pantalla
                        enemie.transform = tr.translate(2.0,2*theta+ty,0)
                        beta=2.0

            for i in range(contadorBalasEnemigo): #Para chochar nuestra nave
                posicionBalasEnemigos= sg.findPosition(balasEnemigos, "balanuevaEnemigo" + str(i))#Posicion balas enemigos
                if abs(posicionBalasEnemigos[0]-posicion_user[0])<=0.09 and abs(posicionBalasEnemigos[1]-posicion_user[1])<=0.1: #"Si es que chocan"
                    CONTADOR_VIDAS-=1#Disminuimos el contador de vidas
                    balita = sg.findNode(balasEnemigos, "balanuevaEnemigo" + str(i))
                    balita.transform = tr.translate(2.0, 0, 0) #si chocan, mandamos la bala hacia afuera de la pantalla

            #Dibujamos todo
            sg.drawSceneGraphNode(balasEnemigos, pipeline, "transform")  #Dibujamos todas las balas que haya en el conjunto "balasEnemigo"
            sg.drawSceneGraphNode(balasUsuario, pipeline, "transform") #Dibujamos todas las balas que haya en el conjunto "balasUsuario"
            sg.drawSceneGraphNode(enemie, pipeline, "transform")#Dibuja al usuario
            sg.drawSceneGraphNode(user, pipeline, "transform")#Dibuja al usuario

        #Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)
    glfw.terminate()
        
        
        
        