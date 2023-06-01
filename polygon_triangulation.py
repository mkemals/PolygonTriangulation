import turtle
from typing import List
from datetime import datetime
import random
import npolygon


def Triangulation(pCount: int = 20, drawTrace: bool = True):
    PolyGen = npolygon.Polygon(pCount)
    cPoints: List[npolygon.CornerPoint] = PolyGen.Generate()
    sumAngle = 0
    for cp in cPoints:
        print(str(cp.LeftPoint.PIndex) + " --> " + str(cp.CenterPoint.PIndex) + " (" + str(cp.Angle) + ") <-- " + str(cp.RightPoint.PIndex))
        sumAngle += cp.Angle

    cPointLeastAngleIndex = PolyGen.FindPointWithLeastAngle()
    print("En Küçük Açı: " + str(cPoints[cPointLeastAngleIndex].LeftPoint.PIndex) + " --> " + str(cPoints[cPointLeastAngleIndex].CenterPoint.PIndex) + "(" + str(cPoints[cPointLeastAngleIndex].Angle) + ") <-- " + str(cPoints[cPointLeastAngleIndex].RightPoint.PIndex))
    print("Toplam Açı: " + str(sumAngle))

    turtle.speed(0)
    turtle.color("green")
    turtle.pensize(2)
    turtle.penup()
    turtle.setposition(cPoints[0].CenterPoint.X, cPoints[0].CenterPoint.Y)
    turtle.pendown()
    style = ('Courier', 16, 'italic')

    i = 1
    while i < pCount:
        if drawTrace:
            sumX = cPoints[i].LeftPoint.X + cPoints[i].CenterPoint.X + cPoints[i].RightPoint.X
            sumY = cPoints[i].LeftPoint.Y + cPoints[i].CenterPoint.Y + cPoints[i].RightPoint.Y
            triCenter: npolygon.Point = npolygon.Point(sumX / 3, sumY / 3, 0)
            tx = turtle.xcor()
            ty = turtle.ycor()
            turtle.penup()
            turtle.setposition(triCenter.X, triCenter.Y)
            if cPoints[i].InternalAngle == 1:
                turtle.color("orange")
            else:
                turtle.color("lightblue")
            turtle.pensize(4)
            turtle.dot()
            turtle.pensize(2)
            turtle.color("green")
            turtle.setposition(tx, ty)
            turtle.pendown()
        point1 = (cPoints[i-1].CenterPoint.X, cPoints[i-1].CenterPoint.Y)
        point2 = (cPoints[i].CenterPoint.X, cPoints[i].CenterPoint.Y)
        turtle.goto(point1)
        turtle.write(str(cPoints[i-1].CenterPoint.PIndex), font=style, align='center')
        turtle.color("red")
        turtle.pensize(4)
        turtle.dot()
        turtle.pensize(2)
        turtle.color("green")
        turtle.goto(point2)
        turtle.write(str(cPoints[i].CenterPoint.PIndex), font=style, align='center')
        i += 1
    turtle.color("red")
    turtle.pensize(4)
    turtle.dot()
    turtle.pensize(2)
    turtle.color("green")
    turtle.goto(cPoints[0].CenterPoint.X, cPoints[0].CenterPoint.Y)
    turtle.write(str(cPoints[0].CenterPoint.PIndex), font=style, align='center')

    turtle.color("blue")

    i = 0
    while i < pCount:
        cPointLeastAngleIndex = PolyGen.FindPointWithLeastAngle()
        turtle.penup()
        turtle.setposition(cPoints[cPointLeastAngleIndex].LeftPoint.X, cPoints[cPointLeastAngleIndex].LeftPoint.Y)
        turtle.pendown()
        turtle.goto(cPoints[cPointLeastAngleIndex].RightPoint.X, cPoints[cPointLeastAngleIndex].RightPoint.Y)
        # iki komşusu birleştirilen nokta kapatılıyor
        cPoints[cPointLeastAngleIndex].CenterPoint = None
        # sağ ve sol komşu noktaların indisleri. bu noktalar birbirilerine komşu olarak tanıtılacak
        cPointRightPointIndex = cPoints[cPointLeastAngleIndex].RightPoint.PIndex
        cPointLeftPointIndex = cPoints[cPointLeastAngleIndex].LeftPoint.PIndex
        # Noktanın sağ komşusu, sol komşusunu artık yeni sol komşusu olarak kabul ediyor
        cPoints[cPointRightPointIndex].LeftPoint = cPoints[cPointLeastAngleIndex].LeftPoint
        # Noktanın sol komşusu, sağ komşusunu artık yeni sağ komşusu olarak kabul ediyor
        cPoints[cPointLeftPointIndex].RightPoint = cPoints[cPointLeastAngleIndex].RightPoint
        i += 1


for i in range(1, 5):
    turtle.Screen().clear()
    pc = random.randint(4, 60)
    dt = True
    Triangulation(pc, dt)
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + str(pc) + str(dt)[0]
    turtle.getscreen().getcanvas().postscript(file="samples/" + filename + ".eps")

turtle.hideturtle()
turtle.exitonclick()

