import math

class String():

    def __init__(self, points, order):
        self.points = points
        self.order = order

    def get_points(self):
        return self.points

    def is_closed_contour(self):
        if self.points[0].x == self.points[-1].x and \
            self.points[0].y == self.points[-1].y and \
            self.points[0].z == self.points[-1].z:
            return True
        return False

    def find_bounding_box(self):
        min_x = math.inf
        max_x = 0
        min_y = math.inf
        max_y = 0
        for p in self.points:
            if p.x < min_x:
                min_x = p.x
            if p.y < min_y:
                min_y = p.y
            if p.x > max_x:
                max_x = p.x
            if p.y > max_y:
                max_y = p.y
        return Box(min_x, min_y, max_x, max_y)

class Box():
    def __init__(self, min_x, min_y, max_x, max_y):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
    
    def __str__(self):
        return "min_x = " + str(self.min_x) + " min_y = " + str(self.min_y) + " max_x = " + str(self.max_x) + " max_y = " + str(self.max_y)

class Boxes():
    def __init__(self, strings):
        self.bbox = []
        idx = 0
        self.strings = strings
        for string in strings:
            box = string.find_bounding_box()
            self.bbox.append((idx, box))
            
    # Complexity is O(n^2)
    def do_overlap(self):
        # We need to apply different algorithm here
        # Take the line from the string and check if it
        # intersects the line from the second contour
        overlap = False
        for i in range(0, len(self.bbox) - 1):
            for j in range(i + 1, len(self.bbox)):
                if (self.bbox[i][1].min_x >=  self.bbox[j][1].min_x and \
                    self.bbox[i][1].max_x >=  self.bbox[j][1].max_x) or \
                    (self.bbox[i][1].min_y >=  self.bbox[j][1].min_y and \
                    self.bbox[i][1].max_y <=  self.bbox[j][1].max_y):
                    overlap = True
        return overlap

    # Complexity is O(n^2)
    def sort(self):
        for i in range(0, len(self.bbox) - 1):
            for j in range(i + 1, len(self.bbox)):
                if self.bbox[i][1].min_x >=  self.bbox[j][1].min_x and \
                    self.bbox[i][1].max_x <=  self.bbox[j][1].max_x and \
                    self.bbox[i][1].min_y >=  self.bbox[j][1].min_y and \
                    self.bbox[i][1].max_y <=  self.bbox[j][1].max_y:
                    tmp = self.bbox[i]
                    self.bbox[i] = self.bbox[j]
                    self.bbox[j] = tmp

    def iterate(self):
        for box in self.bbox:
            yield box
    
    def get_boxes(self):
        return self.bbox

    def length(self):
        return len(self.bbox)

    def get_strings(self, idx):
        return self.strings[idx]
