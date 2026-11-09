import turtle


class BinaryTree:
    def __init__(self, turtle_obj, trunk, depth, angle=45, ratio=0.6):
        self.t = turtle_obj
        self.trunk = trunk
        self.depth = depth
        self.angle = angle
        self.ratio = ratio

    def branch(self, length, n):
        if n == 0:
            return
        self.t.forward(length)
        self.t.left(self.angle)
        self.branch(length * self.ratio, n - 1)
        self.t.right(2 * self.angle)
        self.branch(length * self.ratio, n - 1)
        self.t.left(self.angle)
        self.t.backward(length)

    def draw(self):
        self.t.left(90)
        self.t.penup()
        self.t.goto(0, -200)
        self.t.pendown()
        self.branch(self.trunk, self.depth)


if __name__ == "__main__":
    pen = turtle.Turtle()
    pen.speed("fastest")
    BinaryTree(pen, 100, 9).draw()
    turtle.done()
