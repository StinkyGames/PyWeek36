class Player(arcade.Sprite):
    def __init__(self):
        super().__init__('sprites/player.png')
        # set initial values
        self.center_x = screen_width / 2
        self.center_y = screen_height / 2
        self.z = 0
        self.scale = 1
        # movement traits
        self.max_speed = 3.0
        self.acceleration_rate = 0.1
        self.friction = 0.02

    def update(self):
        # set movement
        self.center_x += self.change_x
        self.center_y += self.change_y

        # set boundaries
        if self.right > screen_width:
            self.right = screen_width
            self.change_x = 0 # Zero x speed
        elif self.left < 0:
            self.left = 0
            self.change_x = 0
        if self.bottom < 0:
            self.bottom = 0
            self.change_y = 0
        elif self.top > screen_height:
            self.top = screen_height
            self.change_y = 0