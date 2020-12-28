# final project

from OpenGL.GL import *
from OpenGL.GLUT import *
from PIL import Image

import sys

windowWidth = 1920
windowHeight = 1080

mousePositionX = 0
mousePositionY = 0

mouseDrawPositionX = 0
mouseDrawPositionY = 0

selectedPencil = 0

pencilPoints = []
eraserPoints = []

pencilTextureId = 0
eraserTextureId = 0
quadTextureId = 0

isClicked = False
isFirst = True

panelOptions = ["Pencil", "Eraser", "Quads"]  # Ekleme yapılacak
selectedPanel = str()
quads = []  # quadları tutan liste
quadPoints = []  # quadın koordinatlarını tutan liste


def LoadTexture(file):
    pencilImg = Image.open(file)
    xSize = pencilImg.size[0]
    ySize = pencilImg.size[1]
    rawReference = pencilImg.tobytes("raw", "RGB")

    glClearColor(1, 1, 1, 0)

    # Create Texture
    id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, id)  # bind Texture, 2d texture (x and y size)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, xSize, ySize, 0, GL_RGB, GL_UNSIGNED_BYTE, rawReference)
    glEnable(GL_TEXTURE_2D)
    return id

def InitGL():
    global pencilTextureId, eraserTextureId, quadTextureId
    glActiveTexture(GL_TEXTURE0)
    pencilTextureId = LoadTexture("./img/pencil.png")
    eraserTextureId = LoadTexture("./img/eraser2.png")
    quadTextureId = LoadTexture("./img/quads.png")
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.0, 0.0, 0.0, 0.0)  # darkmode
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def convertMousePosDrawAxis(mouseDrawPositionX, mouseDrawPositionY):  # convert mouse position to drawing axis position
    point = []
    point.append((mouseDrawPositionX - 770) / 770)
    point.append((110 + 367.5 - mouseDrawPositionY) / 367.5)

    return point

def mouseFunction(*args):
    global selectedPanel, panelOptions, isFirst
    global mousePositionX, mousePositionY, isClicked, selectedPencil, eraserPoints, quadPoints, quads

    mousePositionX = args[2]
    mousePositionY = args[3]

    if (args[0] == GLUT_LEFT_BUTTON and args[1] == GLUT_DOWN):
        isClicked = True
        if (mousePositionX < 100 and mousePositionY < 110):
            selectedPanel = panelOptions[0]
            eraserPoints = []
        elif 100 < mousePositionX < 200 and mousePositionY < 110:
            selectedPanel = panelOptions[1]
        elif 200 < mousePositionX < 300 and mousePositionY < 110:
            selectedPanel = panelOptions[2]
        elif mousePositionY > 110 and selectedPanel == panelOptions[2]:  # farenin ilk dokunusunda koordinat alır
            if len(quadPoints) < 1:
                quadPoints.append(convertMousePosDrawAxis(mousePositionX, mousePositionY))
            else:
                point = convertMousePosDrawAxis(mousePositionX, mousePositionY)
                quadPoints[0][0] = point[0]
                quadPoints[0][1] = point[1]
    elif args[0] == GLUT_LEFT_BUTTON and args[1] == GLUT_UP:  # Fareden el kaldırıldıgındaki son noktayı alır
        isClicked = False
        if mousePositionY > 110 and selectedPanel == panelOptions[2]:
            if len(quadPoints) < 2:
                quadPoints.append(convertMousePosDrawAxis(mousePositionX, mousePositionY))
            else:
                point = convertMousePosDrawAxis(mousePositionX, mousePositionY)
                quadPoints[1][0] = point[0]
                quadPoints[1][1] = point[1]

            point1 = [quadPoints[0][0], quadPoints[0][1]]
            point2 = [quadPoints[1][0], quadPoints[1][1]]

            quads.append([point1, point2])
            quadPoints.clear()

    else:
        isClicked = False

    glutPostRedisplay()


def mouseControl(mx, my):
    global mouseDrawPositionX, mouseDrawPositionY, quadPoints, quads
    mouseDrawPositionX = mx
    mouseDrawPositionY = my
    if mousePositionY > 110 and selectedPanel == panelOptions[2]:
        if len(quadPoints) > 1:
            quadPoints.pop()
        quadPoints.append(convertMousePosDrawAxis(mouseDrawPositionX, mouseDrawPositionY))


def pencilDraw():  # Kalemin cizim yaptıgı fonksiyon
    global mousePositionX, mousePositionY
    global mouseDrawPositionX, mouseDrawPositionY
    global pencilPoints

    if isClicked == True:
        point = convertMousePosDrawAxis(mouseDrawPositionX, mouseDrawPositionY)
        pencilPoints.append(point)


def eraser():
    global mousePositionX, mousePositionY
    global mouseDrawPositionX, mouseDrawPositionY
    global eraserPoints
    if isClicked == True:
        point = convertMousePosDrawAxis(mouseDrawPositionX, mouseDrawPositionY)
        eraserPoints.append(point)
    glPointSize(10.0)
    glColor(0, 1, 0)


def quadDraw():  # Dinamik olarak Dörtgeni cizdirir
    global quadPoints
    if len(quadPoints) == 2:
        point1 = [quadPoints[0][0], quadPoints[0][1]]
        point2 = [quadPoints[1][0], quadPoints[1][1]]
        glColor3f(1, 0.5, 0.5)
        glBegin(GL_QUADS)
        glVertex2f(point1[0], point1[1])
        glVertex2f(point2[0], point1[1])
        glVertex2f(point2[0], point2[1])
        glVertex2f(point1[0], point2[1])
        glEnd()

def searchAndRemove(idx):
    global pencilPoints, eraserPoints
    for i in range(len(pencilPoints)):
        if len(eraserPoints) > idx:
            if (abs(pencilPoints[i][0] - eraserPoints[idx][0]) <= 0.01 and abs(
                    pencilPoints[i][1] - eraserPoints[idx][1]) <= 0.01):
                pencilPoints.pop(i)
                return True
    return False

def paintBackground(r, g, b):
    glColor3f(r, g, b)
    glBegin(GL_QUADS)
    glVertex2f(-1, 1)
    glVertex2f(-1, -1)
    glVertex2f(1, -1)
    glVertex2f(1, 1)
    glEnd()

def display(id):
    """Glut display function."""
    # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # LoadTexture("img/pencil.png")
    glBindTexture(GL_TEXTURE_2D, id)
    glBegin(GL_QUADS)

    glTexCoord2f(0, 0)
    glVertex3f(-1, 1, 0)

    glTexCoord2f(0, 1)
    glVertex3f(-1, -1, 0)

    glTexCoord2f(1, 1)
    glVertex3f(1, -1, 0)

    glTexCoord2f(1, 0)
    glVertex3f(1, 1, 0)
    glEnd()
    glFlush()


def draw():  # beyaz ekrana yapılacak cizim
    global selectedPanel
    global panelOptions
    global pencilPoints
    global quadPoints, quads
    glViewport(0, 0, 1540, 735)
    paintBackground(1, 1, 1)
    if selectedPanel == panelOptions[0]:
        pencilDraw()
    glPointSize(5.0)
    glColor(0, 0, 0)
    glBegin(GL_POINTS)
    for i in range(len(pencilPoints)):
        glVertex2f(pencilPoints[i][0], pencilPoints[i][1])
    glEnd()
    if selectedPanel == panelOptions[1]:
        eraser()
        glPointSize(15.0)
        glColor(1, 1, 1)
        glBegin(GL_POINTS)
        for i in range(len(eraserPoints)):
            searchAndRemove(i)
        glEnd()
    if selectedPanel == panelOptions[2]:
        quadDraw()
    if len(quads) > 0:
        glColor3f(1, 0, 0)
        glBegin(GL_QUADS)
        for i in range(len(quads)):
            point1 = quads[i][0]
            point2 = quads[i][1]
            glVertex2f(point1[0], point1[1])
            glVertex2f(point2[0], point1[1])
            glVertex2f(point2[0], point2[1])
            glVertex2f(point1[0], point2[1])
        glEnd()

def controlPanel():  # panel
    global selectedPencil
    global panelOptions
    glViewport(0, 735, 1540, 110)
    paintBackground(1, 0, 0)
    glViewport(0, 735, 100, 110)
    if selectedPanel == panelOptions[0]:
        paintBackground(0.6, 0.6, 0.6)
    else:
        paintBackground(0.9, 0.9, 0.9)

    display(pencilTextureId)
    glViewport(100, 735, 100, 110)
    if selectedPanel == panelOptions[1]:
        paintBackground(0.6, 0.6, 0.6)
    else:
        paintBackground(0.9, 0.9, 0.9)
    display(eraserTextureId)
    glViewport(200, 735, 100, 110)
    if selectedPanel == panelOptions[2]:
        paintBackground(0.6, 0.6, 0.6)
    else:
        paintBackground(0.9, 0.9, 0.9)
    display(quadTextureId)
    glViewport(300, 735, 100, 110)
    paintBackground(0, 1, 0)


def paint():  # Ana Fonksiyon
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # gluPerspective( fovy, aspect, zNear, zFar )
    # gluPerspective(150, 1.5, 1, 20)
    controlPanel()
    draw()
    glutSwapBuffers()

def main():
    global windowWidth
    global windowHeight
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
    glutInitWindowSize(windowWidth, windowHeight)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Paint 3D")
    glutDisplayFunc(paint)
    glutIdleFunc(paint)
    glutMouseFunc(mouseFunction)
    glutMotionFunc(mouseControl)
    InitGL()
    glutMainLoop()


main()
