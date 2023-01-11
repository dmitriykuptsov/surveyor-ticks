#d = 0.5 r2 = 0.5
#Mark point: x= -15.189008394440275 y=6.706728812806562 z=20.0
#Original line: Line3D: x1=-14.877392 y1=7.097747 z1=20.0 x2=-14.426257 y2=7.663834 z2=20.0
#Offset: 0.5
#Line 1 length: 0.7238627492791712

from math import sqrt
from math import atan2
from math import sin
from math import cos

d = 0.5
x1=-14.877392
y1=7.097747
x2=-14.426257
y2=7.663834
z2 = 20
z1 = 20

r = sqrt((x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1))
print("d = " + str(d))
print("r = " + str(r))

x_sign = 1
if x2 < x1:
	x_sign = -1
y_sign = 1
if y2 < y1:
	y_sign = -1
z_sign = 1
if z2 < z1:
	z_sign = -1


beta = atan2((z2 - z1), r)
alpha = atan2(abs(y2 - y1), abs(x2 - x1))
print("beta = " + str(beta))
print("alpha = " + str(alpha))
r2 = cos(beta) * d
print("d = " + str(d) + " r2 = " + str(r2))  
        
print("dx = " + str(cos(alpha) * r2))
print("dy = " + str(sin(alpha) * r2))
z_p = z1 + z_sign * sin(beta) * d
x_p = x2 - cos(alpha) * r2
y_p = y1 + y_sign * sin(alpha) * r2
print("z_p = " + str(z_p))
print("x_p = " + str(x_p))
print("y_p = " + str(y_p))
print("x1 = " + str(x1))
print("x2 = " + str(x2))
print("y1 = " + str(y1))
print("y2 = " + str(y2))

