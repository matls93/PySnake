from turtle import Screen
import time
from snake import Snake
from food import Food
from scoreboard import ScoreBoard
from game_over import GameOver
from random import randint


screen = Screen()
screen.setup(600, 600)
screen.bgcolor("black")
screen.title("My Snake Game")
screen.tracer(0)

snake = Snake()
food = Food()
score = ScoreBoard()
game_over = GameOver()

sleep_time = 0.1
invisible = False
slow = False
mirror = False
game_paused = False
game_is_on = True
game_quit = False

screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")


def restart_game():
    global game_is_on, sleep_time, invisible, slow, mirror, game_paused
    game_is_on = True
    game_paused = False
    sleep_time = 0.1
    invisible = False
    slow = False
    mirror = False
    score.reset_scoreboard()
    snake.reset()
    game_over.clear()
    screen.update()
    food.move_location()


def quit_game():
    global game_is_on, game_quit
    game_is_on = False
    game_quit = True
    screen.bye()


def handle_click(x, y):
    global game_paused
    action = game_over.check_click(x, y)
    if action == "restart":
        restart_game()
    elif action == "quit":
        quit_game()


def set_food():
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


screen.onscreenclick(handle_click)


while game_is_on:

    if not game_paused and not game_quit:
        screen.update()
        time.sleep(sleep_time)
        snake.move()

        # detect collision with food
        if snake.head.distance(food) < 15:
            snake.extend()
            score.increase_score()
            if slow:
                sleep_time = 0.2
                invisible = False
                mirror = False
                slow = False
            elif mirror:
                sleep_time = 0.1
                invisible = True
                mirror = False
            else:
                sleep_time = 0.1
                invisible = False
                mirror = False

            set_food()

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
                    if game_quit:
                        break
                    game_over.game_over()
                    screen.update()
                    time.sleep(0.3)
                if not game_is_on:
                    break
                score.reset_scoreboard()
                snake.reset()
                game_over.clear()

        # detect collision with tail
        for segment in snake.segments[1:]:
            if snake.head.distance(segment) < 10 and not invisible:
                game_paused = True
                while game_paused:
                    if game_quit:
                        break
                    game_over.game_over()
                    screen.update()
                    time.sleep(0.3)
                if not game_is_on:
                    break
                score.reset_scoreboard()
                snake.reset()
                game_over.clear()

    screen.onscreenclick(handle_click)

screen.exitonclick()
