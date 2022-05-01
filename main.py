import turtle
import random

screen = turtle.Screen()
screen.colormode(255)
screen.bgcolor(224, 255, 255)

writer_turtle = turtle.Turtle()
writer_turtle.penup()
writer_turtle.ht()
writer_turtle.goto(-200, 200)
writer_turtle.color("black")
writer_turtle.write("Score:0", font=("Arial", 17, "normal"))


writer_turtle_lose = turtle.Turtle()
global lives
lives = 3
writer_turtle_lose.speed(0)
writer_turtle_lose.color("black")
writer_turtle_lose.penup()
writer_turtle_lose.goto(80, 200)
writer_turtle_lose.ht()
writer_turtle_lose.clear()
writer_turtle_lose.write("Lives: " + str(lives), font=("Arial", 17, "normal"))

writer_turtle_you_lose = turtle.Turtle()

ball_size = 10.0
box_size = 400.0
boundary = (box_size / 2.0) - ball_size

paddle_speed = 30
paddle_width = box_size / 6.0
paddle_thickness = paddle_width / 10.0

box_drawer = turtle.Turtle()
box_drawer.penup()
box_drawer.speed(0)
box_drawer.goto(-box_size / 2.0, -box_size / 2.0)
box_drawer.pendown()
box_drawer.color(235, 94, 52)
for i in range(4):
    box_drawer.forward(box_size)
    box_drawer.left(90)
box_drawer.ht()

paddle = turtle.Turtle()
paddle.color(255, 69, 0)
paddle.shape("square")
paddle.shapesize(paddle_thickness/20.0, paddle_width / 20.0)

paddle.penup()
paddle.speed(0)
paddle.goto(0, -boundary + 20)


def paddle_right():
    if (paddle.xcor() + paddle_width / 2.0) < boundary:
        paddle.forward(paddle_speed)


def paddle_left():
    if (paddle.xcor() - paddle_width / 2.0) > -boundary:
        paddle.backward(paddle_speed)


screen.onkey(paddle_right, "Right")
screen.onkey(paddle_left, "Left")

num_bricks = 10
gap_size = 10.0
brick_width = (box_size - (num_bricks + 1)*gap_size) / num_bricks
brick_thickness = brick_width / 2.0


def make_brick_row(color, y):
    row = []
    xBrick = (- box_size / 2.0) + gap_size + (brick_width / 2.0)
    for i in range(num_bricks):
        brick = turtle.Turtle()
        brick.speed(0)
        brick.shape("square")
        brick.shapesize(brick_thickness / 20.0, brick_width/20.0)
        brick.color(color)
        brick.penup()
        brick.goto(xBrick, y)
        row.append(brick)
        xBrick = xBrick + brick_width + gap_size

    return row


y_brick = (box_size / 2.0) - gap_size - (brick_thickness / 2.0)
row1 = make_brick_row((255, 69, 0), y_brick)
row2 = make_brick_row((255, 140, 0), y_brick - ((brick_thickness) + gap_size))
row3 = make_brick_row((218, 165, 32), y_brick - 2 *
                      ((brick_thickness) + gap_size))
row4 = make_brick_row((240, 230, 140), y_brick - 3 *
                      ((brick_thickness) + gap_size))

ball = turtle.Turtle()
ball.speed(0)
ball.color(210, 205, 30)
ball.shape("circle")
ball.penup()
ball.goto(0, paddle.ycor() + (paddle_thickness / 2.0) + ball_size)

heading = random.randint(10, 170)
ball.setheading(heading)


def bounce_wall():
    if ball.xcor() > boundary or ball.xcor() < -boundary:
        if ball.ycor() > boundary:
            ball.left(180)
        else:
            ball.setheading(180 - ball.heading())
    elif ball.ycor() > boundary:
        ball.setheading(360 - ball.heading())


def bounce_paddle():
    if ball.ycor() - ball_size < paddle.ycor() + (paddle_thickness / 2.0) and 180 < ball.heading():
        if ball.xcor() + ball_size > paddle.xcor() - (paddle_width / 2.0):
            if ball.xcor() - ball_size < paddle.xcor() + (paddle_width / 2.0):
                ball.setheading(360 - ball.heading())


score = 0


def bounce_brick_row(row):
    for brick in row:
        if ball.ycor() + ball_size > brick.ycor() - (brick_thickness / 2.0):  # ball up, brick down
            if ball.ycor() - ball_size < brick.ycor() + (brick_thickness / 2.0):  # ball down , brick up
                if ball.xcor() + ball_size > brick.xcor() - (brick_width / 2.0):  # ball right , brick left
                    if ball.xcor() - ball_size < brick.xcor() + (brick_width / 2.0):  # ball left , brick right
                        if brick.isvisible():
                            brick.ht()
                            global score
                            score += 1
                            writer_turtle.clear()
                            writer_turtle.goto(-200, 200)
                            writer_turtle.write(
                                "Score:" + str(score), font=("Arial", 20, "normal"))
                            ball.setheading(360 - ball.heading())
                        break


def bounce_bricks():
    bounce_brick_row(row1)
    bounce_brick_row(row2)
    bounce_brick_row(row3)
    bounce_brick_row(row4)


def change_bricks(row):

    if score == 10:

        for brick in row:
            brick.speed(0)
            if brick.isvisible():
                brick.shape("triangle")
    else:
        for brick in row:
            brick.speed(0)

            if brick.isvisible():
                brick.shape("turtle")


def bricks_gone_row(row):
    for brick in row:
        if brick.isvisible():
            return False
    return True


def startGame():
    ball_speed = 5.0
    lose = False
    shape_changer = True
    shape_changer1 = True

    global lives

    while True:
        ball.forward(ball_speed)
        if ball.ycor() <= -boundary:
            lives -= 1
            writer_turtle_lose.clear()
            writer_turtle_lose.write(
                "Lives: " + str(lives), font=("Arial", 20, "normal"))
            if lives >= 1:
                ball.goto(0, paddle.ycor() +
                          (paddle_thickness / 2.0) + ball_size)
                ball.setheading(random.randint(10, 170))
            elif lives == 0:
                writer_turtle_you_lose.speed(0)
                writer_turtle_you_lose.color("black")
                writer_turtle_you_lose.penup()
                writer_turtle_you_lose.goto(-100, 0)
                writer_turtle_you_lose.ht()
                writer_turtle_you_lose.write(
                    "You lose :( Try again", font=("Arial", 15, "normal"))
                lose = True

        if lose:
            break

        bounce_wall()
        bounce_paddle()
        bounce_bricks()
        if score == 10 and shape_changer:
            change_bricks(row1)
            change_bricks(row2)
            change_bricks(row3)
            change_bricks(row4)
            shape_changer = False

        if score == 20 and shape_changer1:
            change_bricks(row1)
            change_bricks(row2)
            change_bricks(row3)
            change_bricks(row4)
            shape_changer1 = False

        if score == 30:
            ball_speed = 8.0

        if score == 40:
            ball_speed = 12.0


screen.onkey(startGame, "space")
screen.listen()
screen.exitonclick()
