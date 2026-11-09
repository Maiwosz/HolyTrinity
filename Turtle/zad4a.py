import turtle


class KochSnowflake:
    def __init__(self, turtle_obj, size, depth):
        self.t = turtle_obj
        self.size = size
        self.depth = depth

    def koch_curve(self, length, n):
        if n == 0:
            self.t.forward(length)
            return
        self.koch_curve(length / 3, n - 1)
        self.t.left(60)
        self.koch_curve(length / 3, n - 1)
        self.t.right(120)
        self.koch_curve(length / 3, n - 1)
        self.t.left(60)
        self.koch_curve(length / 3, n - 1)

    def draw(self):
        self.t.penup()
        self.t.goto(-self.size / 2, self.size / 3)
        self.t.pendown()
        for _ in range(3):
            self.koch_curve(self.size, self.depth)
            self.t.right(120)


if __name__ == "__main__":
    pen = turtle.Turtle()
    pen.speed("fastest")
    KochSnowflake(pen, 300, 4).draw()
    turtle.done()
