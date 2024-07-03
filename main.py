from turtle import Screen
import time
from snake import Snake
from food import Food
from scoreboard import ScoreBoard
from game_over import GameOver
from random import randint

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = "black"
TITLE = "My Snake Game"
INITIAL_SLEEP_TIME = 0.1
FOOD_DISTANCE_THRESHOLD = 16
WALL_DISTANCE_THRESHOLD = 280
TAIL_DISTANCE_THRESHOLD = 10


class SnakeGame:
    def __init__(self):
        self.screen = Screen()
        self.screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen.bgcolor(BACKGROUND_COLOR)
        self.screen.title(TITLE)
        self.screen.tracer(0)

        self.snake = Snake()
        self.food = Food()
        self.score = ScoreBoard()
        self.game_over = GameOver()

        self.sleep_time = INITIAL_SLEEP_TIME
        self.invisible = False
        self.slow = False
        self.mirror = False
        self.game_paused = False
        self.game_is_on = True

        self.screen.listen()
        self.screen.onkey(self.snake.up, "Up")
        self.screen.onkey(self.snake.down, "Down")
        self.screen.onkey(self.snake.left, "Left")
        self.screen.onkey(self.snake.right, "Right")
        self.screen.onscreenclick(self.handle_click)

    def restart_game(self):
        """Restarts the game by resetting game state and objects."""
        self.game_paused = False
        self.sleep_time = INITIAL_SLEEP_TIME
        self.invisible = False
        self.slow = False
        self.mirror = False
        self.score.reset_scoreboard()
        self.snake.reset()
        self.reset_food_properties()
        self.screen.update()

    def quit_game(self):
        """Quits the game by closing the screen."""
        self.game_is_on = False
        self.screen.bye()

    def handle_click(self, x, y):
        """Handles screen click events for game over actions."""
        if self.game_paused:
            action = self.game_over.check_click(x, y)
            if action == "restart":
                self.restart_game()
            elif action == "quit":
                self.quit_game()

    def reset_food_properties(self):
        """Randomizes food properties and moves it to a new location."""
        random_num = randint(0, 6)
        if random_num == 1:
            self.slow = True
            self.food.color('green')
        elif random_num == 2:
            self.mirror = True
            self.food.color('red')
        else:
            self.food.color('blue')
        self.food.move_location()

    def food_collision(self):
        """Handles the effects of the snake colliding with food."""
        if self.slow:
            self.sleep_time = 0.2
            self.invisible = False
            self.slow = False
        elif self.mirror:
            self.invisible = True
            self.sleep_time = 0.1
            self.mirror = False
        else:
            self.sleep_time = 0.1
            self.invisible = False

    def pause_game(self):
        """Displays the game over screen and pauses the game."""
        self.game_over.display()
        self.screen.update()
        time.sleep(0.3)

    def wall_collisions(self):
        """Handles collisions of the snake with the walls."""
        if abs(self.snake.head.xcor()) > WALL_DISTANCE_THRESHOLD or abs(self.snake.head.ycor()) > WALL_DISTANCE_THRESHOLD:
            if self.invisible:
                if abs(self.snake.head.xcor()) > WALL_DISTANCE_THRESHOLD:
                    self.snake.teleport_x()
                elif abs(self.snake.head.ycor()) > WALL_DISTANCE_THRESHOLD:
                    self.snake.teleport_y()
            else:
                self.game_paused = True
                while self.game_paused:
                    self.pause_game()
                self.game_over.clear()

    def tail_collisions(self):
        """Handles collisions of the snake with its own tail."""
        for segment in self.snake.segments[1:]:
            if self.snake.head.distance(segment) < TAIL_DISTANCE_THRESHOLD and not self.invisible:
                self.game_paused = True
                while self.game_paused:
                    self.pause_game()
                self.game_over.clear()
                break  # Exit loop early if collision is detected

    def check_collisions(self):
        """Checks and handles all types of collisions in the game."""
        # Detect collisions with food
        if self.snake.head.distance(self.food) < FOOD_DISTANCE_THRESHOLD:
            self.snake.extend()
            self.score.increase_score()
            self.food_collision()
            self.reset_food_properties()

        # Detect collision with wall
        self.wall_collisions()

        # Detect collision with tail
        self.tail_collisions()

    def main_game_loop(self):
        """Main game loop to continuously update the game state."""
        while self.game_is_on:
            self.screen.update()
            time.sleep(self.sleep_time)
            self.snake.move()
            self.check_collisions()


if __name__ == "__main__":
    game = SnakeGame()
    game.main_game_loop()
    game.screen.exitonclick()
