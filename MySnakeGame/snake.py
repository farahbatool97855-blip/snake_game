
import turtle
import time
import random

# گیم کی بنیادی سیٹنگز
delay = 0.1
score = 0
high_score = 0

# اسکرین سیٹ اپ
wn = turtle.Screen()
wn.title("Modern Snake Game")
wn.bgcolor("#1a1a2e") # ڈارک تھیم بیک گراؤنڈ
wn.setup(width=600, height=600)
wn.tracer(0) # اسکرین اپڈیٹس کو خودکار طور پر روکتا ہے تاکہ گیم اسموتھ چلے

# سانپ کا سر (Snake Head)
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("#00eff6") # چمکدار نیلا رنگ
head.penup()
head.goto(0, 0)
head.direction = "stop"

# سانپ کی خوراک (Food)
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("#ff007f") # چمکدار گلابی رنگ
food.penup()
food.goto(0, 100)

# سانپ کے جسم کے حصے (Body Segments)
segments = []

# اسکور بورڈ (Scoreboard)
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Arial", 16, "bold"))

# گیم پاز (Pause) کی حالت
is_paused = False

# حرکات کے فنکشنز (Movement Functions)
def go_up():
    if head.direction != "down" and not is_paused:
        head.direction = "up"

def go_down():
    if head.direction != "up" and not is_paused:
        head.direction = "down"

def go_left():
    if head.direction != "right" and not is_paused:
        head.direction = "left"

def go_right():
    if head.direction != "left" and not is_paused:
        head.direction = "right"

def toggle_pause():
    global is_paused
    if is_paused:
        is_paused = False
        pen.clear()
        pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Arial", 16, "bold"))
    else:
        is_paused = True
        pen.clear()
        pen.write("GAME PAUSED (Press SPACE to Resume)", align="center", font=("Arial", 16, "bold"))

def move():
    if is_paused:
        return

    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

def reset_game():
    global score, delay
    time.sleep(1)
    head.goto(0, 0)
    head.direction = "stop"

    # پرانے جسم کے حصے غائب کرنا
    for segment in segments:
        segment.goto(1000, 1000)
    segments.clear()

    # اسکور ری سیٹ کرنا
    score = 0
    delay = 0.1
    pen.clear()
    pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Arial", 16, "bold"))

# کی بورڈ بائنڈنگز (Controls)
wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")
wn.onkeypress(toggle_pause, "space") # اسپیس بار سے گیم پاز ہوگی

# مین گیم لوپ (Main Game Loop)
while True:
    wn.update()

    # دیواروں سے ٹکراؤ کی جانچ (Border Collisions)
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        reset_game()

    # خوراک کھانے کی جانچ (Food Collision)
    if head.distance(food) < 20:
        # خوراک کو نئی رینڈم جگہ پر بھیجنا
        x = random.randint(-280, 280)
        y = random.randint(-280, 260)
        food.goto(x, y)

        # سانپ کا نیا حصہ بنانا
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("#00bfff") # تھوڑا ہلکا نیلا رنگ جسم کے لیے
        new_segment.penup()
        segments.append(new_segment)

        # اسپیڈ بڑھانا (تاکہ گیم مشکل ہو)
        delay -= 0.003

        # اسکور بڑھانا
        score += 10
        if score > high_score:
            high_score = score

        pen.clear()
        pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Arial", 16, "bold"))

    # جسم کے حصوں کو سانپ کے پیچھے چلانا
    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move()

    # اپنے ہی جسم سے ٹکرانے کی جانچ (Body Collisions)
    for segment in segments:
        if segment.distance(head) < 20:
            reset_game()

    time.sleep(delay)

wn.mainloop()
