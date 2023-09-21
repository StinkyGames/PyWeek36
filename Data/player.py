import arcade, math

class Player(arcade.Sprite):
    def __init__(self, screen_width, screen_height, physics_engine):
        super().__init__(':resources:images/space_shooter/playerShip2_orange.png')
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

        self.physics_engine = physics_engine

        self.hit_sound = arcade.load_sound(':resources:sounds/hurt1.wav')
        self.death_sound = arcade.load_sound(':resources:sounds/explosion1.wav')
        self.collision_sound = arcade.load_sound(':resources:sounds/hit5.wav')

    def move(self, up_pressed, down_pressed, left_pressed, right_pressed, mouse_x, mouse_y):
        start_x = self.center_x
        start_y = self.center_y

        dest_x = mouse_x
        dest_y = mouse_y

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        self.angle = math.degrees(angle) - 90

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

        # set movement
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Add friction
        if self.change_x > self.friction:
            self.change_x -= self.friction
        elif self.change_x < -self.friction:
            self.change_x += self.friction
        else:
            self.change_x = 0

        if self.change_y > self.friction:
            self.change_y -= self.friction
        elif self.change_y < -self.friction:
            self.change_y += self.friction
        else:
            self.change_y = 0

        # Apply acceleration based on the keys pressed
        if up_pressed and not down_pressed:
            self.change_y += self.acceleration_rate
        elif down_pressed and not up_pressed:
            self.change_y += -self.acceleration_rate
        if left_pressed and not right_pressed:
            self.change_x += -self.acceleration_rate
        elif right_pressed and not left_pressed:
            self.change_x += self.acceleration_rate

        if self.change_x > self.max_speed:
            self.change_x = self.max_speed
        elif self.change_x < -self.max_speed:
            self.change_x = -self.max_speed
        if self.change_y > self.max_speed:
            self.change_y = self.max_speed
        elif self.change_y < -self.max_speed:
            self.change_y = -self.max_speed

        self.physics_engine.sprites[self].body.position = (self.center_x, self.center_y)
        self.physics_engine.sprites[self].body.angle = self.angle

class Bullet(arcade.Sprite):
    def __init__(self):
        super().__init__(':resources:images/space_shooter/laserRed01.png')
        # set initial values
        self.speed = 10
        self.scale = 1
