import turtle

t = turtle.Turtle()
t.speed("fastest")

def frac_nested(x):
    if x < 2:
        return
    t.left(90)
    t.forward(x)
    t.right(90)
    t.forward(x)
    t.right(90)
    t.forward(x)
    t.right(90)
    t.forward(x)
    t.right(180)
    frac_nested(x * 0.9)

x = 300
t.penup()
t.goto(-x / 2, -x / 2)
t.pendown()
frac_nested(x)
turtle.done()
