from sys import argv
from geometry import line
from geometry import strings

if len(argv) < 3:
    print("Usage: python run.py data/input.csv [step]")
    exit()

strings_file = argv[1]
step = float(argv[2])
fd = open(strings_file)
lines = fd.readlines()

strings_ = []
points_ = []
idx = None

for i in range(1, len(lines)):
    l = lines[i].split(";")
    if idx == None:
        idx = int(l[3])
        points_.append(line.Point3D(float(l[0]), float(l[1]), float(l[2])))
    else:
        if idx == int(l[3]):
            points_.append(line.Point3D(float(l[0]), float(l[1]), float(l[2])))
        else:
            strings_.append(strings.String(points_, int(idx)))
            idx = int(l[3])
            points_ = []
            points_.append(line.Point3D(float(l[0]), float(l[1]), float(l[2])))

strings_.append(strings.String(points_, int(idx)))
boxes = strings.Boxes(strings_)
print("Do contours overlap? " + str(boxes.do_overlap()))
boxes.sort()

# Complexity O(nmk)
# Where n is the number of contours
# m is the average number strings in first contour
# k is the average number of strings in the second contour
b = boxes.get_boxes()
for i in range(0, len(b), 2):
    #print(box[1])
    s1 = boxes.get_strings(i)
    s2 = boxes.get_strings(i + 1)
    offset = 0
    for j in range(1, len(s1.get_points())):
        p1 = s1.get_points()[j - 1]
        p2 = s1.get_points()[j]
        

