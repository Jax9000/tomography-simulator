class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def bresnham_line(a, b):
    d, dx, dy, ai, bi, xi, yi = 0
    x = a.x, y = a.y

    # set drawing direction
    if a.x < b.x:
        xi = 1
        dx = b.x - a.x
    else:
        xi = -1
        dx = a.x - b.x

    if a.y < b.y:
        yi = 1
        dy = b.y - a.y
    else:
        yi = -1
        dy = a.y - b.y

    line = [Point(x, y)]

    if dx > dy:
        ai = (dy - dx) * 2
        bi = dy * 2
        d = bi - dx

        while x != b.x:
            if d >= 0:
                x += xi
                y += yi
                d += ai
            else:
                d += bi
                x += xi
            line.append(Point(x, y))
    else:
        ai = (dx - dy) * 2
        bi = dx * 2
        d = bi - dy

        while y != b.y:
            if d >= 0:
                x += xi
                y += yi
                d += ai
            else:
                d += bi
                y += yi
            line.append(Point(x, y))
