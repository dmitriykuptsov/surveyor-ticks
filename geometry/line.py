class Point3D():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "x= " + str(self.x) + " y=" + str(self.y) + " z=" + str(self.z)

class Line3D():
    def __init__(self, x1, y1, z1, x2, y2, z2):
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1

        self.x2 = x2
        self.y2 = y2
        self.z2 = z2

    def intersection(self, l2, p):

        x1 = l2.x1
        y1 = l2.y1
        z1 = l2.z1

        a1 = l2.x2 - x1
        b1 = l2.y2 - y1
        c1 = l2.z2 - z1

        x2 = self.x1
        y2 = self.y1
        z2 = self.z1

        a2 = 0
        b2 = 0
        c2 = 0

        if self.x1 - self.x2 == 0 and l2.y1 - l2.y2 != 0:
            # Case 1 WORKS
            if (l2.x1 - l2.x2) == 0:
                if (l2.y1 <= p.y and l2.y2 >= p.y):
                    a2 = l2.x2 - x2
                    b2 = p.y - y2
                else:
                    return False
            else:
                m1 = (l2.y1 - l2.y2) / (l2.x1 - l2.x2)
                b = l2.y1 - m1 * l2.x1
                a2 = (p.y - b) / m1 - x2
                b2 = p.y
                if b2 < l2.y1 or b2 > l2.y2:
                    return False
                b2 -= p.y
        elif self.y1 - self.y2 == 0 and l2.x1 - l2.x2 != 0:
            # CASE 2
            if (l2.y1 - l2.y2) == 0:
                if (l2.x1 <= p.x and l2.x2 >= p.x):
                    a2 = p.x - x2
                    b2 = l2.y2 - p.y
                else:
                    return False
            else:
                m1 = (l2.y1 - l2.y2) / (l2.x1 - l2.x2)
                b = l2.y1 - m1 * l2.x1
                a2 = p.x
                b2 = m1 * p.x + b - y2
                if a2 < l2.x1 or a2 > l2.x2:
                    return False
                a2 -= p.x
        elif l2.x1 - l2.x2 == 0 and self.y1 - self.y2 != 0:
            # Case 3 WORKS
            if (self.x1 - self.x2) == 0:
                if (l2.y1 <= p.y and l2.y2 >= p.y):
                    a2 = l2.x2 - x2
                    b2 = p.y - y2
                else:
                    return False
            else:
                m1 = (self.y1 - self.y2) / (self.x1 - self.x2)
                m1 = -1/m1
                b = p.y - m1 * p.x
                a2 = l2.x1 - p.x
                b2 = l2.x1 * m1 + b
                if b2 < l2.y1 or b2 > l2.y2:
                    return False
                b2 -= p.y
        elif l2.y1 - l2.y2 == 0 and self.x1 - self.x2 != 0:
            # CASE 4
            if (self.y1 - self.y2) == 0:
                if (l2.x1 <= p.x and l2.x2 >= p.x):
                    a2 = p.x - x2
                    b2 = l2.y2 - self.y2
                else:
                    return False
            else:
                m1 = (self.y1 - self.y2) / (self.x1 - self.x2)
                if m1 == 0:
                    return False
                m1 = -1/m1
                b = p.y - m1 * p.x
                a2 = (l2.y1 - b) / m1
                b2 = l2.y1 - p.y
                if a2 < l2.x1 or a2 > l2.x2:
                    return False
                a2 -= p.x
        elif l2.y1 - l2.y2 == 0 and self.y1 - self.y2 == 0:
            return False
        elif l2.x1 - l2.x2 == 0 and self.x1 - self.x2 == 0:
            return False
        else:
            # Case 5 WORKS
            m1 = (self.y2 - self.y1) / (self.x2 - self.x1)
            m2 = (l2.y2 - l2.y1) / (l2.x2 - l2.x1)
            if m1 == 0:
                return False
            m1 = -1/m1
            if (m1 == m2):
                return False
            b_1 = p.y - m1 * p.x
            b_2 = l2.y1 - m2 * l2.x1
            a2 = (b2 - b1) / (m1 - m2)
            b2 = m1 * a2 + b_1
            if a2 < l2.x1 or a2 > l2.x2:
                return False
            if b2 > l2.y1 or b2 < l2.y2:
                return False
            a2 -= p.x
            b2 -= p.y
        if a1 != 0:
            if a2 * b1 - a1 * b2 == 0:
                return False
            mu = (p.y * a1 - l2.y1 * a1 - b1 * p.x + b1 * l2.x1) / (a2 * b1 - a1 * b2)
            if mu == 0:
                return False
            if a1 == 0:
                return False
            lmb = (p.x - l2.x1 + mu * a2) / a1
            if lmb == 0:
                return False
            c2 = (l2.z1 - p.z + mu * c1) / mu
        else:
            if a2 * b1 - a1 * b2 == 0:
                return False
            # y2 = p.y
            # x1 = l2.x1
            # x2 = p.x
            # y1 = l2.y1
            mu = (l2.x1 * b1 + p.y * a1 - l2.y1 * a1 - p.x * b1) / (a2 * b1 - a1 * b2)
            if mu == 0:
                return False
            if b1 == 0:
                return False
            lmb = (p.y - l2.y1 + mu * b2) / b1
            if lmb == 0:
                return False
            c2 = (l2.z1 - p.z + mu * c1) / mu
        return Point3D(p.x + a2, p.y + b2, p.z + c2)


print("Doing tests...")
print("Case 1")
l1 = Line3D(2, 2, 0, 1, 4, 0)
l2 = Line3D(1, 2, 2, 1, 4, 2)
p = Point3D(1, 3, 2)
p = l2.intersection(l1, p)
if p != False:
    print(p)

from math import sqrt

print("Case 5")
l1 = Line3D(0, 1, 2, 1, 0, 2)
l2 = Line3D(0, 2, 1, 2, 0, 1)
p = Point3D(sqrt(2), sqrt(2), 2)
p = l1.intersection(l2, p)
if p != False:
    print(p)

print("Case 2")
l1 = Line3D(0, 1, 2, 1, 1, 2)
l2 = Line3D(0, 0, 0, 1, 1, 0)
p = Point3D(0.5, 1, 2)
p = l1.intersection(l2, p)
if p != False:
    print(p)

print("Case 4")
print("-------------")
l2 = Line3D(0, 1, 0, 2, 1, 0)
l1 = Line3D(0, 2, 2, 2, 1.5, 2)
p = Point3D(1, 1.75, 2)
p = l1.intersection(l2, p)
if p != False:
    print(p)
print("-------------")

print("Case 2")
print("-------------")
l1 = Line3D(0, 1, 0, 2, 1, 0)
l2 = Line3D(0, 2, 2, 2, 1.5, 2)
p = Point3D(1, 1, 2)
p = l1.intersection(l2, p)
if p != False:
    print(p)
print("-------------")

print("Case 3")
l1 = Line3D(2, 0, 3, 3, 2, 3)
l2 = Line3D(1, 0, 1, 1, 4, 1)
p = Point3D(2.5, 1, 3)
p = l1.intersection(l2, p)
if p != False:
    print(p)