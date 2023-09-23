# **************************************************************************
# Rastgele poligon üretir
#
# Mustafa Kemal Sürmeneli, 2021
# **************************************************************************
import math
import random
from typing import List


class Point:
    def __init__(self, x, y, i):
        self.PIndex = i
        self.X = x
        self.Y = y


class CornerPoint:
    def __init__(self, p0: Point, p1: Point, p2: Point):
        self.CenterPoint: Point = p0
        self.LeftPoint: Point = p1
        self.RightPoint: Point = p2
        self.InternalAngle = 0
        # köşe açıları hesaplanıyor
        # Köşe noktası 0'a taşınıyor
        U = Point(p1.X - p0.X, p1.Y - p0.Y, 0)
        V = Point(p2.X - p0.X, p2.Y - p0.Y, 0)
        cosTheta = (U.X * V.X + U.Y * V.Y) / (math.sqrt(U.X * U.X + U.Y * U.Y) * math.sqrt(V.X * V.X + V.Y * V.Y))
        self.Angle = math.acos(cosTheta) * 180.0 / math.pi


class Polygon:
    def __init__(self, pcount):
        self.pCount = pcount
        self.InternalAngle = 0
        self.CornerPointList: List[CornerPoint] = []

    def Generate(self):
        # Poligon noktaları dizisi
        points: List[Point] = []
        # Poligon noktalarının açısal konumları için seçilecek bölgelerin genişliği
        thetaStep = 360 / self.pCount
        i = 0
        while i < self.pCount:
            # Poligon noktalarının (r, theta) kutupsal koordinatları hesaplanıyor
            t = random.uniform(1, thetaStep)
            # Poligon noktalarıın açısal değerleri için rasgele seçilecek değerler
            theta = i * thetaStep + t
            # Poligon noktasının orijinden uzaklığı
            r = random.randint(50, 300)
            px = r * math.sin(theta * math.pi / 180)
            py = r * math.cos(theta * math.pi / 180)
            points.append(Point(px, py, i))
            i += 1
        i = 0
        while i < self.pCount:
            p0 = points[i]
            j = i - 1
            if j < 0:
                j = self.pCount - 1
            p1 = points[j]
            j = i + 1
            if j > self.pCount - 1:
                j = 0
            p2 = points[j]
            self.CornerPointList.append(CornerPoint(p0, p1, p2))
            i += 1
        i = 0
        # Açı hesaplamakta kullanılan üç nokta poligonun içine mi bakıyor yoksa dışına mı?
        #  Yani; bu noktadan hesaplanan açı biir iç açı mıdır?
        #  Bunu anlamanın bir yolu olarak şöyle yapıldı:
        #  3 noktanın merkez noktası poligonun içindeyse açı bir iç açıdır, yoksa dış açıdır
        while i < self.pCount:
            sumX = self.CornerPointList[i].LeftPoint.X + self.CornerPointList[i].CenterPoint.X \
                   + self.CornerPointList[i].RightPoint.X
            sumY = self.CornerPointList[i].LeftPoint.Y + self.CornerPointList[i].CenterPoint.Y \
                   + self.CornerPointList[i].RightPoint.Y
            triCenter: Point = Point(sumX / 3, sumY / 3, 0)
            self.CornerPointList[i].InternalAngle = self.PointInPolygon(triCenter)
            if self.CornerPointList[i].InternalAngle == 0:
                self.CornerPointList[i].Angle = 360 - self.CornerPointList[i].Angle
            i += 1
        return self.CornerPointList

    def FindPointWithLeastAngle(self):
        leastAngle = 360  # self.CornerPointList[0].Angle
        i = 0
        leastAngleIndex = 0
        while i < len(self.CornerPointList):
            if self.CornerPointList[i].CenterPoint is not None:
                if self.CornerPointList[i].Angle < leastAngle:
                    leastAngle = self.CornerPointList[i].Angle
                    leastAngleIndex = i
            i += 1
        return leastAngleIndex  # self.CornerPointList[leastAngleIndex]

    def PointInPolygon(self, p: Point):
        # Ray Casting Method:
        #   http://geospatialpython.com/2011/01/point-in-polygon.html
        n = len(self.CornerPointList)
        inside = False
        p1: Point = self.CornerPointList[0].CenterPoint
        for i in range(n + 1):
            p2 = self.CornerPointList[i % n].CenterPoint
            if p.Y > min(p1.Y, p2.Y):
                if p.Y <= max(p1.Y, p2.Y):
                    if p.X <= max(p1.X, p2.X):
                        xints = p.X  # init
                        if p1.Y != p2.Y:
                            xints = (p.Y - p1.Y) * (p2.X - p1.X) / (p2.Y - p1.Y) + p1.X
                        if p1.X == p2.X or p.X <= xints:
                            inside = not inside
            p1 = p2
        return inside


