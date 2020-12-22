from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import sys
def InitGL():
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-6, 6, -6, 6)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #gluPerspective( fovy, aspect, zNear, zFar )
    #gluPerspective(150, 1.5, 1, 20)
    glColor3f(0.0,0.0,0.0)
    glutSolidTeapot(0.5)
    glutSwapBuffers()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
    glutInitWindowSize(800, 400)
    glutInitWindowPosition(200, 200)
    glutCreateWindow(b"Paint 3D")
    glutDisplayFunc(draw)
    glutIdleFunc(draw)
    #glutSpecialFunc(keyPressed)
    InitGL()
    glutMainLoop()


main()
