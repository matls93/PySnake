from turtle import Turtle
with open("data.txt") as file:
    high_score = file.read()

if high_score == '':
    high_score = 0
else:
    high_score = int(high_score)


class ScoreBoard(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.score = 0
        self.up()
        self.color("white")
        self.goto(0, 270)
        self.highscore = high_score
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.write(f"Score: {self.score} High Score: {self.highscore}", False, "center", ("Courier", 20, "normal"))

    def increase_score(self):
        self.score += 1
        self.update_scoreboard()

    def reset_scoreboard(self):
        if self.score > self.highscore:
            self.highscore = self.score
            with open("data.txt", mode="w") as file:
                file.write(str(self.highscore))
        self.score = 0
        self.update_scoreboard() 

    def game_over(self):
        self.goto(0,0)
        self.write("GAME OVER", False, "center", ("Courier", 30, "normal"))

