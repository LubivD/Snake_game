import turtle
import time
import random
from helpdb import *

# Game speed
delay = 0.1

# Score on the start game
score = 0
eaten = 0
goal = 10
high_score = 0
db = CreateDB()
db.create()
db = ReadDB()

# Snakes segments on the start game
segments = []

# Set up the screen
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("#304251")
wn.setup(width=650, height=650)
wn.tracer(0)  # Turns off the screen updates


# Board
def boarder():
    board.begin_fill()
    for i in range(4):
        board.forward(580)
        board.left(90)
    board.end_fill()


board = turtle.Turtle()
board.color('#3E5363')
board.pencolor("#B8CEE0")
board.pensize(1)
board.speed(0)
board.setpos(-290, -290)
board.speed(0)
board.hideturtle()
boarder()

# Write greeting & Score
pen = turtle.Turtle()
pen.screen = turtle.Screen()
pen.speed(0)
pen.shape("square")
pen.color("#B8CEE0")
pen.penup()
pen.hideturtle()
pen.goto(0, -130)
pen.write("Hi! This is a Snake game\n\n"
          "Try to eat the maximum amount\n"
          "of turtles.\n\n"
          "Every eaten 10 turtles\n"
          "you will earn + 100 points.\n\n"
          "Press key-buttons to start game.",
          align="center", font=("Courier", 20, "bold"))

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("#55D43F")
head.penup()
head.setpos(0, 0)
head.direction = "stop"

# Snake food
food = turtle.Turtle()
food.speed(0)
food.shape("turtle")
colors = ['pink', 'red', 'blue', 'purple', 'orange', 'yellow']
# food.color('white', random.choice(colors))
food.color('#70B7BA')
food.penup()
food.goto(0, 100)


# Functions
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


# Keyboard bindings
while True:
    scheme = str.lower(pen.screen.textinput("Control scheme",
                                            "What type of control scheme do you want to chose?\n"
                                            "Type '1' for 'WASD' or\n"
                                            "          '2' for 'Arrow'"))

    if scheme == "1":
        up = "w"
        down = "s"
        left = "a"
        right = "d"
        print("You chose 'WASD' scheme")
        break
    elif scheme == "2":
        up = "Up"
        down = "Down"
        left = "Left"
        right = "Right"
        print("You chose 'Arrow' scheme")
        break
    else:
        print("Your command is not recognized")

wn.listen()
wn.onkeypress(go_up, up)
wn.onkeypress(go_down, down)
wn.onkeypress(go_left, left)
wn.onkeypress(go_right, right)


def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)

    if head.direction == "down":
        head.sety(head.ycor() - 20)

    if head.direction == "left":
        head.setx(head.xcor() - 20)

    if head.direction == "right":
        head.setx(head.xcor() + 20)


# Score printing
def print_score_table(points):
    # Select latest added Player score from DB
    # If database is not empty:
    if len(db.read_db()) > 0:
        last_player = max(db.read_db()[:], key=lambda item: item[3])

    # If database is empty:
    else:
        last_player = ["0"] * 3

    # Printing Score table
    print_result = str(
        f"Score: {points}  High Score: {db.read_high_db()[0][0]:<3}\n"
        f"Your place is {last_player[0]:^3}\nand you've owned {last_player[2]:^3} points\n\n"
        f"Place Player\t   Points\n")

    # Parsing Score table
    for i in db.read_db()[:9]:
        print_result += str(f"{i[0]:<5} {i[1]:<12.12} {i[2]:<5}\n")

    # Show last player result
    print_result += str(f"{'.' * 20:^24}\n{last_player[0]:<5} {last_player[1]:<12.12} {last_player[2]:<5}\n")

    pen.clear()  # clear field
    pen.goto(0, -288)
    pen.write(print_result, align="center", font=("Courier", 24, "bold"))
    time.sleep(5)


def show_score(points):
    pen.clear()
    pen.goto(0, 290)
    pen.write(f"Score: {points} High Score: {db.read_high_db()[0][0]}"
              f" Eaten: {eaten} Goal: {goal}",
              align="center", font=("Courier", 18, "bold"))


def write_score_to_db(points):
    # Input name window-mode
    while True:

        name = pen.screen.textinput(f"Type your name",
                                    f"Use less then 12 letters, please.")

        if name is None:
            data_score = WriteDB(str(name), points)
            data_score.write_to_db()
            break
        elif len(name) <= 12:
            data_score = WriteDB(str(name), points)
            data_score.write_to_db()
            break
        elif len(name) > 12:
            print("You use more then 12 letters!\n"
                  "Try again!\n")

    # Input name terminal-mode
    # name = str(input("Type your name. Use less then 12 letters, please.\n"))
    # data_score = WriteDB(str(name), points)
    # data_score.write_to_db()

    # Without wn.listen() window mode doesn't work
    wn.listen()


# Main game loop
while True:
    wn.update()

    # Check for a collision with the border
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        time.sleep(1)
        head.goto(0, 0)
        head.direction = "stop"

        # Hide the segments after crashing
        for segment in segments:
            segment.goto(-310, -310)

        # Write score to DB
        write_score_to_db(high_score)

        # Showing score
        print_score_table(score)

        # Clear the segments list
        segments.clear()

        # Reset the score
        score = 0
        high_score = 0
        eaten = 0
        goal = 10

        # Print clear score
        show_score(score)

        # Reset the delay
        delay = 0.1

    # Check for a collision with the food
    if head.distance(food) < 20:
        # Move the food to a random spot

        # My idea
        x = [i * 20 for i in range(-14, 15)]
        y = [i * 20 for i in range(-14, 15)]
        food.goto(random.choice(x), random.choice(y))

        # Original
        # x = random.randint(-290, 290)
        # y = random.randint(-290, 290)
        # food.goto(x, y)

        # Suggested in video
        # x = random.randrange(-280, 280, 20)
        # y = random.randrange(-280, 280, 20)
        # food.goto(x, y)

        # Need to check colour food changing
        # food.color(random.choice(colors), random.choice(colors))
        # food.color('#70B7BA')

        # Add a segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        # new_segment.color('grey', random.choice(colors))
        new_segment.color('#304251', '#67FF4D')
        new_segment.penup()
        segments.append(new_segment)

        # Shorten the delay
        delay -= 0.001  # Also, you can increase game speed!

        # Increase the score
        score += 10

        eaten += 1

        if eaten % 10 == 0:
            goal += 10
            score += 100

        if score > high_score:
            high_score = score

        show_score(score)

    # Move the end segments first in reverse order
    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 to where the head is
    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    move()

    # Check for head collision with the body segments
    for segment in segments:
        if segment.distance(head) < 20:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"

            # Hide the segments
            for element in segments:
                element.goto(1000, 1000)

            # Write score to DB
            write_score_to_db(high_score)

            # Update the score display
            print_score_table(score)

            # Clear the segments list
            segments.clear()

            # Reset the score
            score = 0
            high_score = 0
            eaten = 0
            goal = 10

            # Print clear score
            show_score(score)

            # Reset the delay
            delay = 0.1

    time.sleep(delay)
# wn.mainloop()
