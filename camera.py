class Camera:
    def __init__(self):
        self.x_pos = 0
        self.y_pos = 0
        self.x_vel = 0
        self.y_vel = 0

    def update(self, x_pos: float, y_pos: float):
        self.x_pos = x_pos
        self.y_pos = y_pos
