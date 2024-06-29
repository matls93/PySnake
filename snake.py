from turtle import Turtle
STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]
MOVE_DISTANCE = 20
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0


class Snake:
    def __init__(self):
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]
        self.x_coordinate = 0
        self.y_coordinate = 0

    def create_snake(self):
        for position in STARTING_POSITIONS:
            self.add_segment(position)

    def add_segment(self, position):
        new_snake = Turtle("square")
        new_snake.color("white")
        new_snake.up()
        new_snake.goto(position)
        self.segments.append(new_snake)

    def reset(self):
        for seg in self.segments:
            seg.goto(1000, 1000)
        self.segments.clear()
        self.create_snake()
        self.head = self.segments[0]

    def extend(self):
        self.add_segment(self.segments[-1].position())

    def move(self):
        for num in range(len(self.segments) - 1, 0, -1):
            new_x = self.segments[num - 1].xcor()
            new_y = self.segments[num - 1].ycor()
            self.segments[num].goto(new_x, new_y)
        self.head.forward(MOVE_DISTANCE)

    def teleport_x(self):
        new_xcor = 0
        if self.head.xcor() > 0:
            new_xcor = -self.head.xcor()
        else:
            new_xcor = 280
        self.head.goto(new_xcor, self.head.ycor())
        self.move()

    def teleport_y(self):
        new_ycor = 0
        if self.head.ycor() > 0:
            new_ycor = -self.head.ycor()
        else:
            new_ycor = 280
        self.head.goto(self.head.xcor(), new_ycor)
        self.move()

    def right(self):
        if self.head.heading() != LEFT:
            self.head.seth(RIGHT)

    def up(self):
        if self.head.heading() != DOWN:
            self.head.seth(UP)

    def left(self):
        if self.head.heading() != RIGHT:
            self.head.seth(LEFT)

    def down(self):
        if self.head.heading() != UP:
            self.head.seth(DOWN)

