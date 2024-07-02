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
    """Restarts the game by resetting game state and objects"""
    global sleep_time, invisible, slow, mirror, game_paused
    game_paused = False
    sleep_time = 0.1
    invisible = False
    slow = False
    mirror = False
    score.reset_scoreboard()
    snake.reset()
    reset_food_properties()
    screen.update()


def quit_game():
    """Quits game by closing the screen"""
    screen.bye()


def handle_click(x, y):
    """Handles the screen click event for game over actions."""
    if game_paused:
        action = game_over.check_click(x, y)
        if action == "restart":
            restart_game()
        elif action == "quit":
            quit_game()


def reset_food_properties():
    """Sets random food property and moves it to a new location"""
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
    """Handles the effects of the snake when colliding with food"""
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


def pause_game():
    """Displays game over screen and pauses game play"""
    game_over.display()
    screen.update()
    time.sleep(0.3)


def wall_collisions():
    """Handles collisions with the walls"""
    global game_paused
    if abs(snake.head.xcor()) > 280 or abs(snake.head.ycor()) > 280:
        if invisible:
            if abs(snake.head.xcor()) > 280:
                snake.teleport_x()
            elif abs(snake.head.ycor()) > 280:
                snake.teleport_y()

        else:
            game_paused = True
            while game_paused:
                pause_game()
            game_over.clear()


def tail_collisions():
    """Handles collisions of the snake with its own tail"""
    global game_paused
    for segment in snake.segments[1:]:
        if snake.head.distance(segment) < 10 and not invisible:
            game_paused = True
            while game_paused:
                pause_game()
            game_over.clear()
            break


def check_collisions():
    """Handles the overarching logic for all collisions"""
    # Detect collisions with food
    if snake.head.distance(food) < 16:
        snake.extend()
        score.increase_score()
        food_collision()
        reset_food_properties()

    # detect collision with wall
    wall_collisions()

    # detect collision with tail
    tail_collisions()


def main_game_loop():
    """Main gameplay loop to continuously update game state"""
    global game_is_on

    while game_is_on:
        screen.update()
        time.sleep(sleep_time)
        snake.move()
        check_collisions()


# Bind keyboard events
screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")
screen.onscreenclick(handle_click)

# Run the game
main_game_loop()

screen.exitonclick()
