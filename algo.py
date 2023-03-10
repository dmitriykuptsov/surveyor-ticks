#!/usr/bin/python3

# Copyright (C) 2023 Micromine
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = "Dmitriy Kuptsov"
__copyright__ = "Copyright 2023, Micromine"
__license__ = "GPL"
__version__ = "0.0.1a"
__maintainer__ = "Dmitriy Kuptsov"
__email__ = "dkuptsov@micromine.com"
__status__ = "development"

from sys import argv
from geometry import line
from geometry import strings

import matplotlib.pyplot as plt

import math

NO_ERROR = 0x0
CONTOURS_ARE_NOT_CLOSED_ERROR = 0x2
NOT_EVEN_NUMBER_OF_CONTOURS = 0x4
CONTOURS_OVERLAP = 0x8


def run(strings_file, output_file, step):
    step = float(step)
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
    #print("Do contours overlap? " + str(boxes.do_overlap()))
    if boxes.do_overlap():
        return (False, CONTOURS_OVERLAP)

    b = boxes.get_boxes()
    for i in range(0, len(b)):
        s1 = boxes.get_strings(i)
        if not s1.is_closed_contour():
            return (False, CONTOURS_ARE_NOT_CLOSED_ERROR)
    
    boxes.sort()

    if len(b) % 2 != 0:
        #print("Number of contours is not even. Continue?")
        return (False, NOT_EVEN_NUMBER_OF_CONTOURS)

    line_counter = 0
    ticks = []

    # Complexity O(nmk)
    # Where n is the number of contours
    # m is the average number strings in first contour
    # k is the average number of strings in the second contour
    for i in range(0, len(b), 2):
        s1 = boxes.get_strings(i)
        s2 = boxes.get_strings(i + 1)
        offset = 0
        j = 1
        while j < len(s1.get_points()):
            p1 = s1.get_points()[j - 1]
            p2 = s1.get_points()[j]
            line1 = line.Line3D(p1.x, p1.y, p1.z, p2.x, p2.y, p2.z)
            min_distance = math.inf
            optimal_line = None

            if offset > line1.length():
                offset -= line1.length()
                j += 1
                continue
            
            mark_point = line1.point_on_line(offset)
            for k in range(1, len(s2.get_points())):
                p21 = s2.get_points()[k - 1]
                p22 = s2.get_points()[k]
                line2 = line.Line3D(p21.x, p21.y, p21.z, p22.x, p22.y, p22.z)      
                pi = line1.intersection(line2, mark_point)
                if pi != False:
                    line3 = line.Line3D(mark_point.x, mark_point.y, mark_point.z, pi.x, pi.y, pi.z)
                    if line3.length() < min_distance:
                        optimal_line = line3
                        min_distance = line3.length()

            if optimal_line:
                if line_counter % 2 == 0:
                    ticks.append(optimal_line)
                else:
                    optimal_line_length = optimal_line.length() / 2
                    mid_point = optimal_line.point_on_line(optimal_line_length)                
                    half_line = line.Line3D(optimal_line.x1, optimal_line.y1, optimal_line.z1, mid_point.x, mid_point.y, mid_point.z)
                    ticks.append(half_line)
                line_counter += 1
            
            if line1.length() - (offset + step) >= 0:
                offset += step
            else:
                offset = (offset + step) - line1.length()
                j += 1

    fd = open(output_file, "w")
    fd.write("EAST;NORTH;RL;JOIN\n")
    idx = 1
    for line1 in ticks:
        fd.write(str(line1.x1) + ";" + str(line1.y1) + ";" + str(line1.z1) + ";" + str(idx) + "\n")
        fd.write(str(line1.x2) + ";" + str(line1.y2) + ";" + str(line1.z2) + ";" + str(idx) + "\n")
        idx += 1
    fd.close()

    fig = plt.figure()
    ax = plt.axes(projection ='3d')

    for j in range(0, boxes.length()):
        s1 = boxes.get_strings(j)
        X = []
        Y = []
        Z = []
        for i in range(0, len(s1.get_points())):
            p1 = s1.get_points()[i]
            X.append(p1.x)
            Y.append(p1.y)
            Z.append(p1.z)

        ax.plot3D(X, Y, Z, 'green')

    for line1 in ticks:
        X = []
        Y = []
        Z = []
        X.append(line1.x1)
        X.append(line1.x2)
        Y.append(line1.y1)
        Y.append(line1.y2)
        Z.append(line1.z1)
        Z.append(line1.z2)
        ax.plot3D(X, Y, Z, 'red')

    ax.set_title('Surveyor ticks drawing')
    plt.show()

    return (True, NO_ERROR)
