# final project

from OpenGL.GL import *
from OpenGL.GLUT import *
from PIL import Image

import sys

from DrawAction import DrawAction

windowWidth = 1920
windowHeight = 1080

mousePositionX = 0
mousePositionY = 0

mouseDrawPositionX = 0
mouseDrawPositionY = 0

selectedPencil = 0

pointSize=float()
points = []
color=[]

pencilPoints = []
eraserPoints = []

pencilTextureId = 0
eraserTextureId = 0
quadTextureId = 0

isClicked = False
isDrawing = False
isFirst = True

panelOptions = ["Pencil", "Eraser", "Quads"]  # Ekleme yapılacak
selectedPanel = str()

quads = []  # quadları tutan liste
quadPoints = []  # quadın koordinatlarını tutan liste

actionsPoints = []
actionsNames = []


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
    global selectedPanel, panelOptions, isDrawing, isClicked
    global mousePositionX, mousePositionY, mouseDrawPositionX, mouseDrawPositionY
    global  eraserPoints, pencilPoints, quadPoints, quads, actionsNames, actionsPoints
    global points,pointSize,color

    mousePositionX = args[2]
    mousePositionY = args[3]

    mouseDrawPositionX = mousePositionX
    mouseDrawPositionY = mousePositionY

    if (args[0] == GLUT_LEFT_BUTTON and args[1] == GLUT_DOWN):
        isClicked = True

        if (mousePositionY > 110):
            isDrawing = True

        if (mousePositionX < 100 and mousePositionY < 110):  #Kalem Secildi
            color=[0,0,0]
            pointSize=5.0

            if (len(actionsNames) == 0):
                selectedPanel = panelOptions[0]
                actionsNames.append(selectedPanel)

            elif (len(actionsNames) >= 1):

                if (actionsNames[len(actionsNames) - 1] == panelOptions[1]):

                    temp = eraserPoints.copy()
                    actionsPoints.append(temp)
                    eraserPoints.clear()

                    selectedPanel = panelOptions[0]
                    actionsNames.append(selectedPanel)

                elif (actionsNames[len(actionsNames) - 1] == panelOptions[2]):

                    temp = quads.copy()
                    actionsPoints.append(temp)
                    quads.clear()

                    selectedPanel = panelOptions[0]
                    actionsNames.append(selectedPanel)


            # eraserPoints.clear()

        elif 100 < mousePositionX < 200 and mousePositionY < 110: # Silgi secildi
            color = [1, 1, 1]
            pointSize = 20.0
            if (len(actionsNames) == 0):
                selectedPanel = panelOptions[1]
                actionsNames.append(selectedPanel)

            elif (len(actionsNames) >= 1):

                if (actionsNames[len(actionsNames) - 1] == panelOptions[0]):

                    temp = pencilPoints.copy()
                    actionsPoints.append(temp)
                    pencilPoints.clear()

                    selectedPanel = panelOptions[1]
                    actionsNames.append(selectedPanel)

                elif (actionsNames[len(actionsNames) - 1] == panelOptions[2]):

                    temp = quads.copy()
                    actionsPoints.append(temp)
                    quads.clear()

                    selectedPanel = panelOptions[1]
                    actionsNames.append(selectedPanel)


        elif 200 < mousePositionX < 300 and mousePositionY < 110: #Quad secildi
            color = [1, 0, 0]
            pointSize = 0.0
            if (len(actionsNames) == 0):
                selectedPanel = panelOptions[2]
                actionsNames.append(selectedPanel)

            elif (len(actionsNames) >= 1):

                if (actionsNames[len(actionsNames) - 1] == panelOptions[0]):

                    temp = pencilPoints.copy()
                    actionsPoints.append(temp)
                    pencilPoints.clear()

                    selectedPanel = panelOptions[2]
                    actionsNames.append(selectedPanel)

                elif (actionsNames[len(actionsNames) - 1] == panelOptions[1]):

                    temp = eraserPoints.copy()
                    actionsPoints.append(temp)
                    eraserPoints.clear()

                    selectedPanel = panelOptions[2]
                    actionsNames.append(selectedPanel)


        elif mousePositionY > 110 and selectedPanel == panelOptions[2]:  # farenin ilk dokunusunda koordinat alır
            if len(quadPoints) < 1:
                quadPoints.append(convertMousePosDrawAxis(mousePositionX, mousePositionY))
            else:
                point = convertMousePosDrawAxis(mousePositionX, mousePositionY)
                quadPoints[0][0] = point[0]
                quadPoints[0][1] = point[1]

    elif args[0] == GLUT_LEFT_BUTTON and args[1] == GLUT_UP:  # Fareden el kaldırıldıgındaki son noktayı alır
        isClicked = False
        isDrawing = False
        print(args)
        if mousePositionY > 110 and selectedPanel == panelOptions[2]:
            if len(quadPoints) < 2:
                quadPoints.append(convertMousePosDrawAxis(mousePositionX, mousePositionY))
            else:
                point = convertMousePosDrawAxis(mousePositionX, mousePositionY)
                quadPoints[1][0] = point[0]
                quadPoints[1][1] = point[1]

            point1 = [quadPoints[0][0], quadPoints[0][1]]
            point2 = [quadPoints[1][0], quadPoints[1][1]]

            temp=DrawAction()
            temp.points=[point1,point2]
            temp.color=color
            temp.pointSize=0.0

            quads.append(temp)
            quadPoints.clear()

        elif mousePositionY > 110 and selectedPanel == panelOptions[0]:
            points.append(convertMousePosDrawAxis(mousePositionX, mousePositionY))

            temp = DrawAction()
            temp.points = points.copy()
            temp.color = color
            temp.pointSize = pointSize

            pencilPoints.append(temp)
            points.clear()

        elif mousePositionY > 110 and selectedPanel == panelOptions[1]:
            points.append(convertMousePosDrawAxis(mousePositionX, mousePositionY))

            temp = DrawAction()
            temp.points = points.copy()
            temp.color = color
            temp.pointSize = pointSize

            eraserPoints.append(temp)
            points.clear()

    glutPostRedisplay()


def mouseControl(mx, my):
    global mouseDrawPositionX, mouseDrawPositionY

    mouseDrawPositionX = mx
    mouseDrawPositionY = my


def pencilDrawing(pencilPoints):  # Kalemin cizim yaptıgı fonksiyon


    for i in range(len(pencilPoints)):
        for j in range(len(pencilPoints[i].points) - 1):
            color = pencilPoints[i].color
            glColor(color[0], color[1], color[2])
            glLineWidth(pencilPoints[i].pointSize)

            point1 = pencilPoints[i].points[j]
            point2 = pencilPoints[i].points[j + 1]

            glBegin(GL_LINES)
            glVertex2f(point1[0], point1[1])
            glVertex2f(point2[0], point2[1])
            glEnd()


def eraser(eraserPoints):
    for i in range(len(eraserPoints)):
        for j in range(len(eraserPoints[i].points) - 1):
            color = eraserPoints[i].color
            glColor(color[0], color[1], color[2])
            glLineWidth(eraserPoints[i].pointSize)

            point1 = eraserPoints[i].points[j]
            point2 = eraserPoints[i].points[j + 1]

            glBegin(GL_LINES)
            glVertex2f(point1[0], point1[1])
            glVertex2f(point2[0], point2[1])
            glEnd()


def quadDraw(quadsPoints):

    if len(quadsPoints) > 0:


        for i in range(len(quadsPoints)):
            color = quadsPoints[i].color
            glColor(color[0], color[1], color[2])

            point1 = quadsPoints[i].points[0]
            point2 = quadsPoints[i].points[1]

            glBegin(GL_QUADS)
            glVertex2f(point1[0], point1[1])
            glVertex2f(point2[0], point1[1])
            glVertex2f(point2[0], point2[1])
            glVertex2f(point1[0], point2[1])
            glEnd()


def currentPencilDrawing():  # Kalemin anlık cizim yaptıgı fonksiyon
    global mouseDrawPositionX, mouseDrawPositionY
    global isClicked, isDrawing, points,color,pointSize

    glColor(color[0], color[1], color[2])
    glLineWidth(pointSize)

    if isClicked and isDrawing:
        point = convertMousePosDrawAxis(mouseDrawPositionX, mouseDrawPositionY)
        points.append(point)
        for j in range(len(points) - 1):
            glBegin(GL_LINES)
            glVertex2f(points[j][0], points[j][1])
            glVertex2f(points[j + 1][0], points[j + 1][1])
            glEnd()


def currentEraser():
    global mouseDrawPositionX, mouseDrawPositionY
    global isClicked, isDrawing, points,color,pointSize

    glColor(color[0], color[1], color[2])
    glLineWidth(pointSize)

    if isClicked and isDrawing:
        point = convertMousePosDrawAxis(mouseDrawPositionX, mouseDrawPositionY)
        points.append(point)
        for j in range(len(points) - 1):
            glBegin(GL_LINES)
            glVertex2f(points[j][0], points[j][1])
            glVertex2f(points[j + 1][0], points[j + 1][1])
            glEnd()


def currentQuadDraw():  # Dinamik olarak Dörtgeni cizdirir
    global mouseDrawPositionX, mouseDrawPositionY, quadPoints

    if isClicked and isDrawing:
        if len(quadPoints) > 1:
            quadPoints.pop()
        quadPoints.append(convertMousePosDrawAxis(mouseDrawPositionX, mouseDrawPositionY))

    if len(quadPoints) == 2:
        point1 = [quadPoints[0][0], quadPoints[0][1]]
        point2 = [quadPoints[1][0], quadPoints[1][1]]
        glColor3f(color[0]*0.5, color[1]*0.5, color[2]*0.5)
        glBegin(GL_QUADS)
        glVertex2f(point1[0], point1[1])
        glVertex2f(point2[0], point1[1])
        glVertex2f(point2[0], point2[1])
        glVertex2f(point1[0], point2[1])
        glEnd()


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


def oldDraw():
    global actionsNames, actionsPoints, panelOptions

    for k in range(len(actionsPoints)):

        if (actionsNames[k] == panelOptions[0]):
            pencilDrawing(actionsPoints[k])

        if (actionsNames[k] == panelOptions[1]):
            eraser(actionsPoints[k])

        if (actionsNames[k] == panelOptions[2]):
            quadDraw(actionsPoints[k])


def currentDrawing():
    global panelOptions, selectedPanel, pencilPoints, eraserPoints, quads

    if selectedPanel == panelOptions[0]:
        pencilDrawing(pencilPoints)
        currentPencilDrawing()

    if selectedPanel == panelOptions[1]:
        eraser(eraserPoints)
        currentEraser()

    if selectedPanel == panelOptions[2]:
        quadDraw(quads)
        currentQuadDraw()


def draw():  # beyaz ekrana yapılacak cizim

    glViewport(0, 0, 1540, 735)
    paintBackground(1, 1, 1)

    oldDraw()

    currentDrawing()

def controlPanel():  # panel
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
