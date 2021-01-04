'''final project '''


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


pointSize = 5.0
points = []

pencilPoints = []
eraserPoints = []
waterColorPoints=[]

textureIDs=[]

isClicked = False
isDrawing = False
isUndoClicked = False

isRedSelected = 0
isGreenSelected = 0
isBlueSelected = 0

panelOptions = ["Pencil", "Eraser", "Quads","WaterColor"]  # Ekleme yapılacak
selectedPanel = str()

quads = []  # quadları tutan liste
quadPoints = []  # quadın koordinatlarını tutan liste

actionsPoints = []
actionsNames = []


def LoadTexture(file):
    Img = Image.open(file)
    xSize = Img.size[0]
    ySize = Img.size[1]
    rawReference = Img.tobytes("raw", "RGB")

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
    global textureIDs
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glActiveTexture(GL_TEXTURE0)

    textureIDs.append(LoadTexture("./img/pencil.png"))
    textureIDs.append(LoadTexture("./img/eraser.png"))
    textureIDs.append(LoadTexture("./img/quad.jpg"))
    textureIDs.append(LoadTexture("./img/paintBrush.jpg"))
    textureIDs.append(LoadTexture("./img/undo.png"))

    glEnable(GL_TEXTURE_2D)
    glClearColor(0.0, 0.0, 0.0, 0.0)  # darkmode
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def convertMousePosDrawAxis(mouseDrawPositionX, mouseDrawPositionY):  # convert mouse position to drawing axis position
    point = list()
    point.append((mouseDrawPositionX - 770) / 770)
    point.append((110 + 367.5 - mouseDrawPositionY) / 367.5)

    return point


def mouseFunction(*args):
    global selectedPanel, isDrawing, isClicked
    global mousePositionX, mousePositionY, mouseDrawPositionX, mouseDrawPositionY
    global eraserPoints, pencilPoints, waterColorPoints, quads, actionsNames, actionsPoints
    global points, pointSize,quadPoints
    global isRedSelected, isGreenSelected, isBlueSelected,isUndoClicked

    mousePositionX = args[2]
    mousePositionY = args[3]

    mouseDrawPositionX = mousePositionX
    mouseDrawPositionY = mousePositionY

    if args[0] == GLUT_LEFT_BUTTON and args[1] == GLUT_DOWN:
        isClicked = True

        if mousePositionY > 110:
            isDrawing = True

        if mousePositionX < 100 and mousePositionY < 110:  # Kalem Secildi

            #o anki renk beyaz ise siyah olarak değiştir
            if isRedSelected ==1 and isGreenSelected == 1 and isBlueSelected == 1:
                isRedSelected = 0
                isGreenSelected = 0
                isBlueSelected = 0

            if pointSize < 5:
                pointSize = 5.0

            if len(actionsNames) == 0:
                selectedPanel = panelOptions[0]
                actionsNames.append(selectedPanel)

            elif len(actionsNames) >= 1:

                if actionsNames[len(actionsNames) - 1] == panelOptions[1]:

                    temp = eraserPoints.copy()
                    actionsPoints.append(temp)
                    eraserPoints.clear()

                    selectedPanel = panelOptions[0]
                    actionsNames.append(selectedPanel)

                elif actionsNames[len(actionsNames) - 1] == panelOptions[2]:

                    temp = quads.copy()
                    actionsPoints.append(temp)
                    quads.clear()

                    selectedPanel = panelOptions[0]
                    actionsNames.append(selectedPanel)

                elif actionsNames[len(actionsNames) - 1] == panelOptions[3]:

                    temp = waterColorPoints.copy()
                    actionsPoints.append(temp)
                    waterColorPoints.clear()

                    selectedPanel = panelOptions[0]
                    actionsNames.append(selectedPanel)


        elif 100 < mousePositionX < 200 and mousePositionY < 110:  # Silgi secildi
            isRedSelected = 1
            isGreenSelected = 1
            isBlueSelected = 1


            if pointSize < 20.0:
                pointSize = 20.0

            if len(actionsNames) == 0:
                selectedPanel = panelOptions[1]
                actionsNames.append(selectedPanel)

            elif len(actionsNames) >= 1:

                if actionsNames[len(actionsNames) - 1] == panelOptions[0]:

                    temp = pencilPoints.copy()
                    actionsPoints.append(temp)
                    pencilPoints.clear()

                    selectedPanel = panelOptions[1]
                    actionsNames.append(selectedPanel)

                elif actionsNames[len(actionsNames) - 1] == panelOptions[2]:

                    temp = quads.copy()
                    actionsPoints.append(temp)
                    quads.clear()

                    selectedPanel = panelOptions[1]
                    actionsNames.append(selectedPanel)

                elif actionsNames[len(actionsNames) - 1] == panelOptions[3]:

                    temp = waterColorPoints.copy()
                    actionsPoints.append(temp)
                    waterColorPoints.clear()

                    selectedPanel = panelOptions[1]
                    actionsNames.append(selectedPanel)


        elif 200 < mousePositionX < 300 and mousePositionY < 110:  # Quad secildi
            pointSize = 0.0
            if len(actionsNames) == 0:
                selectedPanel = panelOptions[2]
                actionsNames.append(selectedPanel)

            elif len(actionsNames) >= 1:

                if actionsNames[len(actionsNames) - 1] == panelOptions[0]:

                    temp = pencilPoints.copy()
                    actionsPoints.append(temp)
                    pencilPoints.clear()

                    selectedPanel = panelOptions[2]
                    actionsNames.append(selectedPanel)

                elif actionsNames[len(actionsNames) - 1] == panelOptions[1]:

                    temp = eraserPoints.copy()
                    actionsPoints.append(temp)
                    eraserPoints.clear()

                    selectedPanel = panelOptions[2]
                    actionsNames.append(selectedPanel)

                elif actionsNames[len(actionsNames) - 1] == panelOptions[3]:

                    temp = waterColorPoints.copy()
                    actionsPoints.append(temp)
                    waterColorPoints.clear()

                    selectedPanel = panelOptions[2]
                    actionsNames.append(selectedPanel)


        elif 300< mousePositionX < 400 and mousePositionY < 110:  # Fırca Secildi

            if pointSize < 5:
                pointSize = 5.0

            if len(actionsNames) == 0:
                selectedPanel = panelOptions[3]
                actionsNames.append(selectedPanel)

            elif len(actionsNames) >= 1:
                if actionsNames[len(actionsNames) - 1] == panelOptions[0]:
                    temp=pencilPoints.copy()
                    actionsPoints.append(temp)
                    pencilPoints.clear()

                    selectedPanel = panelOptions[3]
                    actionsNames.append(selectedPanel)

                elif actionsNames[len(actionsNames) - 1] == panelOptions[1]:

                    temp = eraserPoints.copy()
                    actionsPoints.append(temp)
                    eraserPoints.clear()

                    selectedPanel = panelOptions[3]
                    actionsNames.append(selectedPanel)

                elif actionsNames[len(actionsNames) - 1] == panelOptions[2]:

                    temp = quads.copy()
                    actionsPoints.append(temp)
                    quads.clear()

                    selectedPanel = panelOptions[3]
                    actionsNames.append(selectedPanel)


        elif mousePositionY < 110 and 400 < mousePositionX < 500: #undo secildi
            isUndoClicked=True
            undoDrawAction()

        elif mousePositionY < 110 and 500 < mousePositionX < 600: #Kırmızı renk secildi
            if isRedSelected == 1:
                isRedSelected = 0
            else:
                isRedSelected = 1

        elif mousePositionY < 110 and 600 < mousePositionX < 700: #Yesil Renk Secildi
            if isGreenSelected == 1:
                isGreenSelected = 0
            else:
                isGreenSelected = 1

        elif mousePositionY < 110 and 700 < mousePositionX < 800: #Mavi Renk Secildi
            if isBlueSelected == 1:
                isBlueSelected = 0
            else:
                isBlueSelected = 1




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
        isUndoClicked=False
        print(args)

        if mousePositionY > 110 and selectedPanel == panelOptions[0]:
            points.append(convertMousePosDrawAxis(mousePositionX, mousePositionY))

            temp = DrawAction()
            temp.points = points.copy()
            temp.color = [isRedSelected, isGreenSelected, isBlueSelected]
            temp.pointSize = pointSize

            pencilPoints.append(temp)
            points.clear()

        elif mousePositionY > 110 and selectedPanel == panelOptions[1]:
            points.append(convertMousePosDrawAxis(mousePositionX, mousePositionY))

            temp = DrawAction()
            temp.points = points.copy()
            temp.color = [isRedSelected, isGreenSelected, isBlueSelected]
            temp.pointSize = pointSize

            eraserPoints.append(temp)
            points.clear()


        elif mousePositionY > 110 and selectedPanel == panelOptions[2]:
            if len(quadPoints) < 2:
                quadPoints.append(convertMousePosDrawAxis(mousePositionX, mousePositionY))
            else:
                point = convertMousePosDrawAxis(mousePositionX, mousePositionY)
                quadPoints[1][0] = point[0]
                quadPoints[1][1] = point[1]

            point1 = [quadPoints[0][0], quadPoints[0][1]]
            point2 = [quadPoints[1][0], quadPoints[1][1]]

            temp = DrawAction()
            temp.points = [point1, point2]
            temp.color = [isRedSelected, isGreenSelected, isBlueSelected]
            temp.pointSize = 0.0

            quads.append(temp)
            quadPoints.clear()

        elif mousePositionY > 110 and selectedPanel == panelOptions[3]:
            points.append(convertMousePosDrawAxis(mousePositionX, mousePositionY))

            temp = DrawAction()
            temp.points = points.copy()
            temp.color = [isRedSelected, isGreenSelected, isBlueSelected]
            temp.pointSize = pointSize

            waterColorPoints.append(temp)
            points.clear()

    glutPostRedisplay()


def mouseControl(mx, my):
    global mouseDrawPositionX, mouseDrawPositionY

    mouseDrawPositionX = mx
    mouseDrawPositionY = my


def undoDrawAction():
    global actionsPoints, pencilPoints,quads,waterColorPoints

    if selectedPanel == panelOptions[0] and len(pencilPoints) > 0:
        pencilPoints.pop()

    elif selectedPanel == panelOptions[1] and len(eraserPoints) > 0:
        eraserPoints.pop()

    elif selectedPanel == panelOptions[2] and len(quads) > 0:
        quads.pop()

    elif selectedPanel==panelOptions[3] and len(waterColorPoints)>0:
        waterColorPoints.pop()

    else:
        if len(actionsPoints) > 0:
            for i in range(len(actionsPoints)):
                if len(actionsPoints[len(actionsPoints) - 1 -i]) > 0:
                    actionsPoints[len(actionsPoints) - 1 -i].pop()
                    break


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

def waterColorDrawing(waterColorPoints):  # Kalemin cizim yaptıgı fonksiyon

    for i in range(len(waterColorPoints)):
        for j in range(len(waterColorPoints[i].points) - 1):
            color = waterColorPoints[i].color
            glColor4f(color[0], color[1], color[2],0.6)

            glLineWidth(waterColorPoints[i].pointSize)

            point1 = waterColorPoints[i].points[j]
            point2 = waterColorPoints[i].points[j + 1]

            glBegin(GL_LINES)
            glVertex2f(point1[0], point1[1])
            glVertex2f(point2[0], point2[1])
            glEnd()

def eraser(eraserPoints):
    for i in range(len(eraserPoints)):
        for j in range(len(eraserPoints[i].points) - 1):
            glColor(1, 1, 1)
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
    global points, isRedSelected, isGreenSelected, isBlueSelected

    # o anki renk beyaz ise siyak olarak değiştir
    if isRedSelected == 1 and isGreenSelected == 1 and isBlueSelected == 1 and selectedPanel==panelOptions[0]:
        isRedSelected = 0
        isGreenSelected = 0
        isBlueSelected = 0
    if selectedPanel==panelOptions[0]:
        glColor(isRedSelected, isGreenSelected, isBlueSelected)
    elif selectedPanel==panelOptions[3]:
        glColor4f(isRedSelected, isGreenSelected, isBlueSelected,0.6)
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
    global points
    global isRedSelected, isGreenSelected, isBlueSelected

    isRedSelected = 1
    isGreenSelected = 1
    isBlueSelected = 1

    glColor(isRedSelected, isGreenSelected, isBlueSelected)
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
    global quadPoints

    if isClicked and isDrawing:
        if len(quadPoints) > 1:
            quadPoints.pop()
        quadPoints.append(convertMousePosDrawAxis(mouseDrawPositionX, mouseDrawPositionY))

    if len(quadPoints) == 2:
        point1 = [quadPoints[0][0], quadPoints[0][1]]
        point2 = [quadPoints[1][0], quadPoints[1][1]]

        glColor4f(isRedSelected, isGreenSelected, isBlueSelected, 0.5)
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

    for k in range(len(actionsPoints)):

        if actionsNames[k] == panelOptions[0]:
            pencilDrawing(actionsPoints[k])

        if actionsNames[k] == panelOptions[1]:
            eraser(actionsPoints[k])

        if actionsNames[k] == panelOptions[2]:
            quadDraw(actionsPoints[k])

        if actionsNames[k]==panelOptions[3]:
            waterColorDrawing(actionsPoints[k])


def currentDrawing():

    if selectedPanel == panelOptions[0]:
        pencilDrawing(pencilPoints)
        currentPencilDrawing()

    if selectedPanel == panelOptions[1]:
        eraser(eraserPoints)
        currentEraser()

    if selectedPanel == panelOptions[2]:
        quadDraw(quads)
        currentQuadDraw()

    if selectedPanel==panelOptions[3]:
        waterColorDrawing(waterColorPoints)
        currentPencilDrawing()


def draw():  # beyaz ekrana yapılacak cizim

    glViewport(0, 0, 1540, 735)

    paintBackground(1, 1, 1)

    oldDraw()

    currentDrawing()


def controlPanel():  # panel

    glViewport(0, 735, 1540, 110) # control panelini oluşturur
    paintBackground(0.4, 0.4, 0.4)

    glViewport(0, 735, 100, 110) #kalem butonu
    if selectedPanel != panelOptions[0]:
        paintBackground(0.6, 0.6, 0.6)
    else:
        paintBackground(0.9, 0.9, 0.9)

    display(textureIDs[0])

    glViewport(100, 735, 100, 110)#silgi butonu
    if selectedPanel != panelOptions[1]:
        paintBackground(0.6, 0.6, 0.6)
    else:
        paintBackground(0.9, 0.9, 0.9)

    display(textureIDs[1])

    glViewport(200, 735, 100, 110)#dortgen sekil butonu
    if selectedPanel != panelOptions[2]:
        paintBackground(0.6, 0.6, 0.6)
    else:
        paintBackground(0.9, 0.9, 0.9)

    display(textureIDs[2])

    glViewport(300,735,100,110)#sulu boya butonu
    if selectedPanel !=panelOptions[3]:
        paintBackground(0.6,0.6,0.6)
    else:
        paintBackground(0.9,0.9,0.9)

    display(textureIDs[3])

    glViewport(400, 735, 100, 110) # geri alma butonu
    if isUndoClicked == True:
        paintBackground(0.9, 0.9, 0.9)
    else:
        paintBackground(0.6, 0.6, 0.6)

    display(textureIDs[4])

    glViewport(500, 735, 100, 110) #kırmızı renk butonu
    if isRedSelected != 1:
        paintBackground(0.5, 0, 0)
    else:
        paintBackground(1, 0, 0)

    glViewport(600, 735, 100, 110) #yeşil renk butonu
    if isGreenSelected != 1:
        paintBackground(0, 0.5, 0)
    else:
        paintBackground(0, 1, 0)

    glViewport(700, 735, 100, 110) # mavi renk butonu
    if isBlueSelected != 1:
        paintBackground(0, 0, 0.5)
    else:
        paintBackground(0, 0, 1)

    glViewport(800, 735, 100, 110)  # beyaz renk butonu
    if isRedSelected == 1 and isBlueSelected == 1 and isGreenSelected == 1:
        paintBackground(1, 1, 1)
    else:
        paintBackground(0.5, 0.5, 0.5)

    glViewport(900, 735, 100, 110)  # sarı renk butonu
    if isRedSelected == 1 and isGreenSelected == 1 and isBlueSelected != 1:
        paintBackground(1, 1, 0)
    else:
        paintBackground(0.5, 0.5, 0)

    glViewport(1000, 735, 100, 110)  # mor renk butonu
    if isRedSelected == 1  and isGreenSelected != 1 and isBlueSelected == 1:
        paintBackground(1, 0, 1)
    else:
        paintBackground(0.5, 0, 0.5)

    glViewport(1100, 735, 100, 110)  # cyan renk butonu
    if isRedSelected != 1 and isBlueSelected == 1 and isGreenSelected == 1:
        paintBackground(0, 1, 1)
    else:
        paintBackground(0, 0.5, 0.5)

    glViewport(1200, 735, 100, 110)  # siyah renk butonu
    if isRedSelected != 1 and isBlueSelected != 1 and isGreenSelected != 1:
        paintBackground(0, 0, 0)
    else:
        paintBackground(0.25, 0.25, 0.25)

def keyboardFunc(*args):
    global pointSize
    if (args[0] == b'w' or args[0] == b'W') and selectedPanel != panelOptions[2]:
        if pointSize < 100:
            pointSize += 10
    elif (args[0]==b's' or args[0] == b'S'):
        if pointSize > 5:
            pointSize -= 5

    print(pointSize)


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
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(windowWidth, windowHeight)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Paint 3D")
    glutDisplayFunc(paint)
    glutIdleFunc(paint)
    glutMouseFunc(mouseFunction)
    glutMotionFunc(mouseControl)
    glutKeyboardFunc(keyboardFunc)
    InitGL()
    glutMainLoop()


main()
