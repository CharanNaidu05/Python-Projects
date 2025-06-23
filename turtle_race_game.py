import turtle
import random
import time
from playsound import playsound
import threading

# Draw checkerboard finish line
def draw_checkerboard(t):
    colors = ["black", "white"]
    start_x, start_y = -150, 250

    for row in range(2):
        x = start_x
        y = start_y - (25 * row)
        for i in range(12):
            t.penup()
            t.goto(x, y)
            t.pendown()
            t.begin_fill()
            t.fillcolor(colors[(i + row) % 2])
            for _ in range(4):
                t.forward(25)
                t.right(90)
            t.end_fill()
            x += 25

# Setup screen and labels
def setup_screen(p1, p2):
    s = turtle.Screen()
    s.title("Turtle Race Game")
    s.setup(1.0, 1.0)
    s.bgcolor("white")
    s.colormode(255)

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)

    # Draw middle line
    t.penup()
    t.goto(0, -200)
    t.setheading(90)
    t.pendown()
    t.forward(400)

    # Start/finish labels
    t.penup()
    t.goto(0, -225)
    t.write("Start Line", align="center", font=["Arial", 15, "bold"])
    t.goto(0, 255)
    t.write("Finish Line", align="center", font=["Arial", 15, "bold"])

    draw_checkerboard(t)

    # Player names
    t.goto(-600, 350)
    t.write(f"Player 1: {p1}", font=["Arial", 20, "bold"])
    t.goto(600, 350)
    t.write(f"Player 2: {p2}", align="right", font=["Arial", 20, "bold"])

    return s, t

# Countdown with beep
def countdown(t):
    t.penup()
    t.goto(0, 0)
    t.color("black")
    for i in range(3, 0, -1):
        t.write(f"Starting in {i}...", align="center", font=["Arial", 25, "bold"])
        playsound("beep.mp3")
        time.sleep(1)
        t.undo()
    t.write("GO!", align="center", font=["Arial", 25, "bold"])
    playsound("beep.mp3")
    time.sleep(1)
    t.undo()

# Setup turtles
def setup_turtles():
    t1 = turtle.Turtle()
    t1.shape("turtle")
    t1.color("blue")
    t1.penup()
    t1.goto(-75, -200)
    t1.setheading(90)

    t2 = turtle.Turtle()
    t2.shape("turtle")
    t2.color("red")
    t2.penup()
    t2.goto(75, -200)
    t2.setheading(90)

    return t1, t2

# Race logic
def start_race(t1, t2, screen):
    t1_dist = 0
    t2_dist = 0

    while True:
        t1_step = random.randint(1, 5)
        t2_step = random.randint(1, 5)
        t1.forward(t1_step)
        t2.forward(t2_step)
        t1_dist += t1_step
        t2_dist += t2_step

        screen.bgcolor((0, 255, 255) if t1_dist > t2_dist else (255, 192, 203))

        if t1_dist >= 390 or t2_dist >= 390:
            break

    return t1_dist, t2_dist

# Play winner music (5 sec limit)
def play_winner_music_5s():
    def play():
        playsound("winner.mp3")
    t = threading.Thread(target=play)
    t.start()
    time.sleep(5)

# Show winner and play music
def display_result(t, p1, p2, t1_dist, t2_dist):
    t.penup()
    t.goto(0, -325)
    t.color((50, 0, 180))

    if t1_dist == t2_dist:
        t.write("It's a Tie!", align="center", font=["Arial", 35, "bold"])
    else:
        winner = p1 if t1_dist > t2_dist else p2
        margin = abs(t1_dist - t2_dist)
        t.write(f"Winner is {winner} !!", align="center", font=["Arial", 35, "bold"])
        t.goto(0, -360)
        t.write(f"Won by {margin} steps", align="center", font=["Arial", 15, "normal"])

    threading.Thread(target=play_winner_music_5s).start()

# Ask if user wants to play again
def ask_restart():
    answer = turtle.textinput("Play Again?", "Do you want to restart the game? (yes/no)")
    if answer:
        return answer.lower().startswith("y")
    return False

# Main game function
def turtle_race_game():
    while True:
        turtle.clearscreen()
        p1 = turtle.textinput("Player 1", "Enter name of Player 1:")
        p2 = turtle.textinput("Player 2", "Enter name of Player 2:")

        if not p1 or not p2:
            break  # Exit if players cancel input

        screen, t = setup_screen(p1, p2)
        countdown(t)
        t1, t2 = setup_turtles()
        t1_dist, t2_dist = start_race(t1, t2, screen)
        display_result(t, p1, p2, t1_dist, t2_dist)

        if not ask_restart():
            break

    turtle.bye()  # Close the window

# Run the game
if __name__ == "__main__":
    turtle_race_game()
