import math

class String():

    def __init__(self, points, order):
        self.points = points
        self.order = order

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
            if p.y < max_y:
                max_y = p.y
        return (min_x, min_y, max_x, max_y)
