#final project

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image

import sys

windowWidth=1920
windowHeight=1080

mousePositionX = 0
mousePositionY = 0

mouseDrawPositionX = 0
mouseDrawPositionY = 0


points = []

isClicked = False


panelOptions=["Pencil","Eraser"] #Ekleme yapılacak
selectedPanel=str()

def InitImage():
    pencilImg = Image.open("./img/kalem.png")
    xSize = pencilImg.size[0]
    ySize = pencilImg.size[1]
    rawReference = pencilImg.tobytes("raw", "RGB")

    glClearColor(1, 1, 1, 0)

    # Create Texture
    id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, id)  # bind Texture, 2d texture (x and y size)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, xSize, ySize, 0, GL_RGB, GL_UNSIGNED_BYTE, rawReference)
    glEnable(GL_TEXTURE_2D)

def InitGL():
    glClearColor(0.0, 0.0, 0.0, 0.0) #darkmode
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    #gluOrtho2D(-6, 6, -6, 6)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def display():
    """Glut display function."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    InitImage()
    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)

    glTexCoord2f(0.2, 0.2)
    glVertex3f(-0.2, 0.2, 0)

    glTexCoord2f(0.2, 0.69)
    glVertex3f(-0.2, -0.2, 0)

    glTexCoord2f(0.69, 0.69)
    glVertex3f(0.2, -0.2, 0)

    glTexCoord2f(0.69, 0)
    glVertex3f(0.2, 0.2, 0)
    glEnd()

    glFlush()

def paintBackground(r,g,b):
    glColor3f(r,g,b)
    glBegin(GL_QUADS)
    glVertex2f(-1, 1)
    glVertex2f(-1, -1)
    glVertex2f(1, -1)
    glVertex2f(1, 1)
    glEnd()

def controlPanel():
    glViewport(0, 735, 1540, 110)
    paintBackground(1,0,0)
    glViewport(0,735,100,110)
    paintBackground(0, 0, 1)
    #display()
    glViewport(100,735,100,110)
    paintBackground(0,1,0)
    glViewport(200, 735, 100, 110)
    paintBackground(0, 0, 1)
    glViewport(300, 735, 100, 110)
    paintBackground(0, 1, 0)

def draw():
    global selectedPanel
    global optionsPanel
    glViewport(0, 0, 1540, 735)
    paintBackground(1, 1, 1)
    if(selectedPanel==panelOptions[0]):
        pencilDraw()

def convertMousePosDrawAxis(mouseDrawPositionX,mouseDrawPositionY): #convert mouse position to drawing axis position
    point = []
    point.append ((mouseDrawPositionX-770)/770)
    point.append( (110+367.5-mouseDrawPositionY)/367.5)

    return point

def pencilDraw():
    global mousePositionX, mousePositionY
    global mouseDrawPositionX,mouseDrawPositionY
    global points

    #if(isClicked):
    point = convertMousePosDrawAxis(mouseDrawPositionX,mouseDrawPositionY)
    points.append(point)

    glPointSize(5.0)
    glColor(0, 0, 0)

    glBegin(GL_POINTS)

    for i in range (len(points)):
        glVertex2f(points[i][0],points[i][1])

    glEnd()

def paint():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # gluPerspective( fovy, aspect, zNear, zFar )
    # gluPerspective(150, 1.5, 1, 20)
    controlPanel()
    draw()
    glutSwapBuffers()

def mouseFunction(*args):
    global selectedPanel,panelOptions
    global mousePositionX,mousePositionY,isClicked

    print(args)
    mousePositionX = args[2]
    mousePositionY = args[3]
    if(args[0]==GLUT_LEFT_BUTTON):
        if(mousePositionX<100 and mousePositionY<110):
            selectedPanel=panelOptions[0]
        if(args[1] == 0 ):
            isClicked = True
        elif(args[1] == 1):
            isClicked = False

    glutPostRedisplay()

def mouseControl( mx, my):
    global mouseDrawPositionX,mouseDrawPositionY
    mouseDrawPositionX = mx
    mouseDrawPositionY = my

    print (str(mouseDrawPositionX) + "," + str( mouseDrawPositionY ))


def main():
    global windowWidth
    global windowHeight
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
    glutInitWindowSize(windowWidth, windowHeight)
    glutInitWindowPosition(0,0)
    glutCreateWindow(b"Paint 3D")
    glutDisplayFunc(paint)
    glutIdleFunc(paint)
    glutMouseFunc(mouseFunction)
    glutPassiveMotionFunc(mouseControl)
    #glutSpecialFunc(keyPressed)
    InitGL()
    glutMainLoop()


main()
