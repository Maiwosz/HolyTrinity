import turtle

t = turtle.Turtle()
t.speed("fastest")


def triangle(x):
    for _ in range(3):
        t.forward(x)
        t.left(120)


def sierpinski(x, n):
    if n == 0:
        triangle(x)
        return
    # dolny lewy trójkąt
    sierpinski(x / 2, n - 1)
    # dolny prawy trójkąt
    t.forward(x / 2)
    sierpinski(x / 2, n - 1)
    t.backward(x / 2)
    # górny trójkąt
    t.left(60)
    t.forward(x / 2)
    t.right(60)
    sierpinski(x / 2, n - 1)
    t.left(60)
    t.backward(x / 2)
    t.right(60)


x = 300
n = 5
t.penup()
t.goto(-x / 2, -x / 3)
t.pendown()
sierpinski(x, n)
turtle.done()
