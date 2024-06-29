from turtle import Turtle


class GameOver(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.up()
        self.color("white")
        self.goto(0,0)

    def game_over(self):
        self.clear()
        self.goto(0, 20)
        self.write("GAME OVER", False, "center", ("Courier", 30, "bold"))
        self.goto(0, -40)
        self.write("Try Again", False, "center", ("Courier", 15, "normal"))
        self.goto(0, -100)
        self.write("Quit", False, "center", ("Courier", 15, "normal"))

    def check_click(self, x, y):
        # Coordinates for "Restart" button
        if -60 < x < 60 and -50 < y < -20:
            return "restart"
        # Coordinates for "Quit" button
        elif -35 < x < 35 and -120 < y < -80:
            return "quit"
        return None
