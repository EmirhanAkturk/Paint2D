#final project

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image

import sys

windowWidth=1920
windowHeight=1080

def InitImage():
    pencilImg = Image.open("./img/kalem.png")
    xSize = pencilImg.size[0]
    ySize = pencilImg.size[1]
    rawReference = pencilImg.tobytes("raw", "RGB")

    glClearColor(0, 0, 0, 0)

    # Create Texture
    id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, id)  # bind Texture, 2d texture (x and y size)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
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
    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)

    glTexCoord2f(0.2, 0.2)
    glVertex3f(-0.5, 0.5, 0)

    glTexCoord2f(0.2, 0.69)
    glVertex3f(-0.5, -0.5, 0)

    glTexCoord2f(0.69, 0.69)
    glVertex3f(0.5, -0.5, 0)

    glTexCoord2f(0.69, 0)
    glVertex3f(0.5, 0.5, 0)
    glEnd()

    glutSwapBuffers()

def paintBackground(r,g,b):
    glColor3f(r,g,b)
    glBegin(GL_QUADS)
    glVertex2f(-1, 1)
    glVertex2f(-1, -1)
    glVertex2f(1, -1)
    glVertex2f(1, 1)
    glEnd()

def controlPanel():
    glViewport(0, 735, 1540, 100)
    paintBackground(1,0,0)
    glViewport(0,735,100,100)
    paintBackground(0,0,1)
    glViewport(100,735,100,100)
    paintBackground(0,1,0)
    glViewport(200, 735, 100, 100)
    paintBackground(0, 0, 1)
    glViewport(300, 735, 100, 100)
    paintBackground(0, 1, 0)

#def draw():

def paint():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # gluPerspective( fovy, aspect, zNear, zFar )
    # gluPerspective(150, 1.5, 1, 20)
    controlPanel()
    glutSwapBuffers()


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
    #glutSpecialFunc(keyPressed)
    InitGL()
    InitImage()
    glutDisplayFunc(display)
    glutMainLoop()


main()
