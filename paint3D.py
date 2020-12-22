#final project

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
windowWidth=1920
windowHeight=1080

def InitGL():
    glClearColor(0.0, 0.0, 0.0, 0.0) #darkmode
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    #gluOrtho2D(-6, 6, -6, 6)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

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
    glutMainLoop()


main()
