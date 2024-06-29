import turtle

class Menu:
    def __init__(self, score):
        self.running_score = score

    def quit_game(self):
        button = turtle.Turtle()
        for _ in range(2):
            button.forward(100)
            button.left(90)
            button.forward(60)
            button.left(90)

