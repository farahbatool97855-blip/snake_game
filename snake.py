import turtle
import random
import time

wn = turtle.Screen()
wn.title("Snake Game Pro")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)

# Snake head
head = turtle.Turtle()
head.shape("square")
head.color("green")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Food
food = turtle.Turtle()
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

segments = []

score = 0
high_score = 0

# Score display
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)

def update_score():
    pen.clear()
    pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Arial", 14, "normal"))

update_score()

# Movement
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    if head.direction == "down":
        head.sety(head.ycor() - 20)
    if head.direction == "left":
        head.setx(head.xcor() - 20)
    if head.direction == "right":
        head.setx(head.xcor() + 20)

# Controls
wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")

def reset_game():
    global score
    time.sleep(1)
    head.goto(0, 0)
    head.direction = "stop"

    for s in segments:
        s.goto(1000, 1000)
    segments.clear()

    score = 0
    update_score()

# Main loop
while True:
    wn.update()

    # Border collision
    if abs(head.xcor()) > 290 or abs(head.ycor()) > 290:
        reset_game()

    # Food collision
    if head.distance(food) < 20:
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x, y)

        new_segment = turtle.Turtle()
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.penup()
        segments.append(new_segment)

        score += 10
        if score > high_score:
            high_score = score

        update_score()

    # Move body
    for i in range(len(segments)-1, 0, -1):
        x = segments[i-1].xcor()
        y = segments[i-1].ycor()
        segments[i].goto(x, y)

    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    move()

    # Self collision
    for s in segments:
        if s.distance(head) < 20:
            reset_game()

    time.sleep(0.1)