import arcade

class Player(arcade.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__(":resources:images/space_shooter/playerShip2_orange.png")
        # set initial orientation values
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.center_x = screen_width / 2
        self.center_y = screen_height / 2
        self.z = 0
        self.scale = 1
        # movement traits
        self.max_speed = 3.0
        self.acceleration_rate = 0.1
        self.friction = 0.02
        # stats
        self.hull = 10

    def update(self):
        # set movement
        self.center_x += self.change_x
        self.center_y += self.change_y

        # set boundaries
        if self.right > self.screen_width:
            self.right = self.screen_width
            self.change_x = 0 # Zero x speed
        elif self.left < 0:
            self.left = 0
            self.change_x = 0
        if self.bottom < 0:
            self.bottom = 0
            self.change_y = 0
        elif self.top > self.screen_height:
            self.top = self.screen_height
            self.change_y = 0