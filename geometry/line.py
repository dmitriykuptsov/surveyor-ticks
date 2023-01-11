from math import sqrt
from math import sin
from math import cos
from math import atan2
from math import pi

class Point3D():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def distance(self, p):
        return sqrt((self.x - p.x)*(self.x - p.x) + \
            (self.y - p.y)*(self.y - p.y) + \
                (self.z - p.z)*(self.z - p.z))

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
    
    def __str__(self):
        return str("Line3D: x1=" + str(self.x1) + " y1=" + str(self.y1) + " z1=" + str(self.z1) + " x2=" + str(self.x2) + " y2=" + str(self.y2) + " z2=" + str(self.z2))

    def is_point_on_the_line(self, p):

        a = self.x2 - self.x1
        b = self.y2 - self.y1
        c = self.z2 - self.z1

        l1 = (p.x - self.x1) / a
        l2 = (p.y - self.y1) / b
        l3 = (p.z - self.z1) / c

        return (l1 == l2 and l2 == l3)


    def point_on_line(self, d):
        if d == 0:
            return Point3D(self.x1, self.y1, self.z1)
        
        r = sqrt((self.x2 - self.x1)*(self.x2 - self.x1) + (self.y2 - self.y1)*(self.y2 - self.y1))

        beta = atan2((self.z2 - self.z1), r)
        alpha = atan2((self.y2 - self.y1),(self.x2 - self.x1))

        x_sign = 1
        if self.x2 < self.x1:
            x_sign = -1
        y_sign = 1
        if self.y2 < self.y1:
            y_sign = -1
        z_sign = 1
        if self.z2 < self.z1:
            z_sign = -1
        
        r2 = cos(beta) * d
        print("d = " + str(d) + " r2 = " + str(r2))  
        z_p = self.z1 + z_sign * sin(beta) * d
        x_p = self.x1 + x_sign * cos(alpha) * r2
        y_p = self.y1 + y_sign * sin(alpha) * r2

        return Point3D(x_p, y_p, z_p)

    def length(self):
        return sqrt((self.x1 - self.x2)*(self.x1 - self.x2) + \
            (self.y1 - self.y2)*(self.y1 - self.y2) + \
                (self.z1 - self.z2)*(self.z1 - self.z2))

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
            #print("CASE 1")
            if (l2.x1 - l2.x2) == 0:
                if (l2.y1 < l2.y2):
                    if (l2.y1 <= p.y and l2.y2 >= p.y):
                        a2 = l2.x2 - x2
                        b2 = p.y - p.y
                    else:
                        return False
                else:
                    if (l2.y1 >= p.y and l2.y2 <= p.y):
                        a2 = l2.x2 - x2
                        b2 = p.y - p.y
                    else:
                        return False
            else:
                m1 = (l2.y1 - l2.y2) / (l2.x1 - l2.x2)
                b = l2.y1 - m1 * l2.x1
                a2 = (p.y - b) / m1 - p.x
                b2 = p.y
                if l2.y1 < l2.y2:
                    if b2 < l2.y1 or b2 > l2.y2:
                        return False
                else:
                    if b2 > l2.y1 or b2 < l2.y2:
                        return False
                b2 -= p.y
        elif self.y1 - self.y2 == 0 and l2.x1 - l2.x2 != 0:
            # CASE 2 WORKS
            #print("CASE 2")
            if (l2.y1 - l2.y2) == 0:
                if (l2.x1 <= p.x and l2.x2 >= p.x and l2.x1 < l2.x2):
                    a2 = p.x - p.x
                    b2 = l2.y2 - p.y

                elif (l2.x1 >= p.x and l2.x2 <= p.x and l2.x1 > l2.x2):
                    a2 = p.x - p.x
                    b2 = l2.y2 - p.y
                else:
                    return False
            else:
                m1 = (l2.y1 - l2.y2) / (l2.x1 - l2.x2)
                b = l2.y1 - m1 * l2.x1
                a2 = p.x
                b2 = m1 * p.x + b - p.y
                #print(a2)
                #print(b2)
                if l2.x1 < l2.x2:
                    if a2 < l2.x1 or a2 > l2.x2:
                        return False
                else:
                    if a2 > l2.x1 or a2 < l2.x2:
                        return False
                a2 -= p.x
        elif l2.x1 - l2.x2 == 0 and self.y1 - self.y2 != 0:
            # Case 3 WORKS
            #print("CASE 3")
            if (self.x1 - self.x2) == 0:
                if (l2.y1 < l2.y2):
                    if (l2.y1 <= p.y and l2.y2 >= p.y):
                        a2 = l2.x2 - x2
                        b2 = p.y - p.y
                    else:
                        return False
                else:
                    if (l2.y1 >= p.y and l2.y2 <= p.y):
                        a2 = l2.x2 - x2
                        b2 = p.y - p.y
                    else:
                        return False
            else:
                m1 = (self.y1 - self.y2) / (self.x1 - self.x2)
                m1 = -1/m1
                b = p.y - m1 * p.x
                a2 = l2.x1 - p.x
                b2 = l2.x1 * m1 + b
                if l2.y1 < l2.y2:
                    if b2 < l2.y1 or b2 > l2.y2:
                        return False
                else:
                    if b2 > l2.y1 or b2 < l2.y2:
                        return False
                b2 -= p.y
        elif l2.y1 - l2.y2 == 0 and self.x1 - self.x2 != 0:
            # CASE 4 WORKS
            #print("CASE 4")
            if (self.y1 - self.y2) == 0:
                if (l2.x1 < l2.x2):
                    if (l2.x1 <= p.x and l2.x2 >= p.x):
                        a2 = p.x - p.x
                        b2 = l2.y2 - self.y2
                    else:
                        return False
                else:
                    if (l2.x1 >= p.x and l2.x2 <= p.x):
                        a2 = p.x - p.x
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
                if l2.x1 < l2.x2:
                    if a2 < l2.x1 or a2 > l2.x2:
                        return False
                else:
                    if a2 > l2.x1 or a2 < l2.x2:
                        return False
                a2 -= p.x
        elif l2.y1 - l2.y2 == 0 and self.y1 - self.y2 == 0:
            return False
        elif l2.x1 - l2.x2 == 0 and self.x1 - self.x2 == 0:
            return False
        elif self.x1 - self.x2 == 0 and l2.y1 - l2.y2 == 0:
            return False
        elif l2.x1 - l2.x2 == 0 and self.y1 - self.y2 == 0:
            return False
        else:
            # Case 5 WORKS WORKS
            #print("CASE 5")
            m1 = (self.y2 - self.y1) / (self.x2 - self.x1)
            m2 = (l2.y2 - l2.y1) / (l2.x2 - l2.x1)
            if m1 == 0:
                return False
            m1 = -1/m1
            if (m1 == m2):
                return False
            #print("p.y = " + str(p.y))
            b_1 = p.y - m1 * p.x
            b_2 = l2.y1 - m2 * l2.x1
            a2 = (b_2 - b_1) / (m1 - m2)
            b2 = m1 * a2 + b_1
            #print("m1 = " + str(m1))
            #print("m2 = " + str(m2))
            #print("b_2 = " + str(b_2))
            #print("b_1 = " + str(b_1))
            #print("a2 = " + str(a2))
            #print("b2 = " + str(b2))
            if l2.x1 < l2.x2:
                if a2 < l2.x1 or a2 > l2.x2:
                    #print("Should not be here")
                    return False
            else:
                if a2 > l2.x1 or a2 < l2.x2:
                    #print("Should not be here")
                    return False
            #if b2 > l2.y2 or b2 < l2.y1:
            #    return False
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
            #if lmb == 0:
            #    return False
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
            #if lmb == 0:
            #    return False
            c2 = (l2.z1 - p.z + mu * c1) / mu
        return Point3D(p.x + a2, p.y + b2, p.z + c2)

"""
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

print("--------------")
print("Special cases")
l1 = Line3D(3, 0, 0, 4, 0, 0)
l2 = Line3D(3, 2, 10, 4, 2, 10)
p = Point3D(3, 0, 10)
p = l1.intersection(l2, p)
if p != False:
    print(p)

"""

"""
print("Special cases")

l1 = Line3D(0, 1, 0, 1, 0, 0)
l2 = Line3D(2, 3, 10, 3, 2, 10)

p = Point3D(0, 1, 0)
p = l1.intersection(l2, p)
if p != False:
    print(p)

l1 = Line3D(0, 7, 0, 1, 8, 0)
l2 = Line3D(2, 5, 10, 3, 6, 10)

p = Point3D(1, 8, 0)
p = l1.intersection(l2, p)
if p != False:
    print(p)

l1 = Line3D(10, 8, 0, 11, 7, 0)
l2 = Line3D(7, 6, 10, 9, 4, 10)

p = Point3D(10, 8, 0)
p = l1.intersection(l2, p)
if p != False:
    print(p)

l1 = Line3D(10, 0, 0, 11, 1, 0)
l2 = Line3D(8, 2, 10, 8, 3, 10)

p = Point3D(10, 0, 0)
p = l1.intersection(l2, p)
if p != False:
    print(p)

l1 = Line3D(10, 0, 0, 11, 1, 0)
l2 = Line3D(8, 3, 10, 9, 4, 10)

p = Point3D(11, 1, 0)
p = l1.intersection(l2, p)
if p != False:
    print(p)

l1 = Line3D(0, 1, 0, 0, 7, 0)
l2 = Line3D(2, 3, 10, 2, 5, 10)

p = Point3D(0, 4, 0)
p = l1.intersection(l2, p)
if p != False:
    print(p)

l1 = Line3D(1, 8, 0, 10, 8, 0)
l2 = Line3D(3, 6, 10, 7, 6, 10)

p = Point3D(5, 8, 0)
p = l1.intersection(l2, p)
if p != False:
    print(p)

l1 = Line3D(1, 0, 0, 10, 0, 0)
l2 = Line3D(4, 2, 10, 5, 1, 10)

p = Point3D(4.5, 0, 0)
p = l1.intersection(l2, p)
if p != False:
    print(p)

l1 = Line3D(1, 0, 0, 10, 0, 0)
l2 = Line3D(5, 1, 10, 7, 1, 10)

p = Point3D(6, 0, 0)
p = l1.intersection(l2, p)
if p != False:
    print(p)

l1 = Line3D(11, 1, 0, 11, 7, 0)
l2 = Line3D(8, 2, 10, 8, 3, 10)

p = Point3D(11, 2.5, 0)
p = l1.intersection(l2, p)
if p != False:
    print(p)

l1 = Line3D(11, 1, 0, 11, 7, 0)
l2 = Line3D(8, 3, 10, 9, 4, 10)

p = Point3D(11, 3.5, 0)
p = l1.intersection(l2, p)
if p != False:
    print(p)

l1 = Line3D(10, 0, 0, 11, 1, 0)
l2 = Line3D(9, 4, 10, 8, 3, 10)

p = Point3D(10.707106781186548, 0.7071067811865476, 0)
print(l2)
p = l1.intersection(l2, p)
if p != False:
    print(p)

l1 = Line3D(11, 1, 10, 11, 7, 10)
l2 = Line3D(8, 2, 0, 7, 1, 0)

p = Point3D(11, 1.5857864376269049, 10)
print(l2)
p = l1.intersection(l2, p)
if p != False:
    print(p)
else:
    print("No intersection")


l1 = Line3D(1, 0, 10, 10, 0, 10)
l2 = Line3D(5, 1, 0, 7, 1, 0)

p = Point3D(6, 0, 10)
print(l2)
p = l1.intersection(l2, p)
if p != False:
    print(p)
else:
    print("No intersection")

l1 = Line3D(11, 1, 10, 11, 7, 10)
l2 = Line3D(8, 3, 0, 8, 2, 0)

p = Point3D(11, 2.585786437626905, 10)
print(l2)
p = l1.intersection(l2, p)
if p != False:
    print(p)
else:
    print("No intersection")
"""