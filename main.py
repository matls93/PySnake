from turtle import Screen
import time
from snake import Snake
from food import Food
from scoreboard import ScoreBoard
from game_over import GameOver
from random import randint

# Set up the screen
screen = Screen()
screen.setup(600, 600)
screen.bgcolor("black")
screen.title("My Snake Game")
screen.tracer(0)

# Create game objects
snake = Snake()
food = Food()
score = ScoreBoard()
game_over = GameOver()

# Initialise game state variables
sleep_time = 0.1
invisible = False
slow = False
mirror = False
game_paused = False
game_is_on = True


def restart_game():
    global game_is_on, sleep_time, invisible, slow, mirror, game_paused
    game_paused = False
    sleep_time = 0.1
    invisible = False
    slow = False
    mirror = False
    score.reset_scoreboard()
    snake.reset()
    reset_food()
    screen.update()


def quit_game():
    screen.bye()


def handle_click(x, y):
    action = game_over.check_click(x, y)
    if action == "restart":
        restart_game()
    elif action == "quit":
        quit_game()


def reset_food():
    global slow, mirror
    random_num = randint(0, 6)
    if random_num == 1:
        slow = True
        food.color('green')
    elif random_num == 2:
        mirror = True
        food.color('red')
    else:
        food.color('blue')
    food.move_location()


def food_collision():
    global sleep_time, invisible, mirror, slow
    if slow:
        sleep_time = 0.2
        invisible = False
        slow = False
    elif mirror:
        invisible = True
        sleep_time = 0.1
        mirror = False
    else:
        sleep_time = 0.1
        invisible = False


screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")
screen.onscreenclick(handle_click)


while game_is_on:

    screen.update()
    time.sleep(sleep_time)
    snake.move()

    # detect collision with food
    if snake.head.distance(food) < 17:
        snake.extend()
        score.increase_score()
        food_collision()
        reset_food()

    # detect collision with wall
    if snake.head.xcor() > 280 or snake.head.xcor() < -280 or snake.head.ycor() > 280 or snake.head.ycor() < -280:
        if invisible:
            if snake.head.xcor() > 280 or snake.head.xcor() < -280:
                snake.teleport_x()
            elif snake.head.ycor() > 280 or snake.head.ycor() < -280:
                snake.teleport_y()
        else:
            game_paused = True
            while game_paused:
                game_over.display()
                screen.update()
                time.sleep(0.3)
            game_over.clear()

    # detect collision with tail
    for segment in snake.segments[1:]:
        if snake.head.distance(segment) < 10 and not invisible:
            game_paused = True
            while game_paused:
                game_over.display()
                screen.update()
                time.sleep(0.3)
            game_over.clear()

screen.exitonclick()
