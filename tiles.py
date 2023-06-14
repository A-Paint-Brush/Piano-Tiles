class tile:
    def __init__(self, row, y):
        self.clicked = False
        self.width = 71
        self.height = 132
        self.row = row
        self.pos_x = self.width * self.row - self.width
        self.pos_y = y
        self.color = (0, 0, 0)

    def move(self, height):
        self.pos_y += height

    def update(self, screen_width):
        self.pos_x = (screen_width // 2 - 142) + (self.width * self.row - self.width)
