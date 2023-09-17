import arcade

screen_width = 1024
screen_height = 768
game_title = 'Dark Matter'

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

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.set_mouse_visible(False)
        self.set_location(int((arcade.get_display_size()[0] - screen_width) / 2),
                          int((arcade.get_display_size()[1] - screen_height) / 2))
        # idle at start
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.setup()  # call the setup/new game function

    def setup(self):
        self.player = Player()

    def on_draw(self):
        arcade.start_render()
        self.player.draw()

    def update(self, delta_time):
        self.player.update()

        # Add friction
        if self.player.change_x > self.player.friction:
            self.player.change_x -= self.player.friction
        elif self.player.change_x < -self.player.friction:
            self.player.change_x += self.player.friction
        else:
            self.player.change_x = 0

        if self.player.change_y > self.player.friction:
            self.player.change_y -= self.player.friction
        elif self.player.change_y < -self.player.friction:
            self.player.change_y += self.player.friction
        else:
            self.player.change_y = 0

        # Apply acceleration based on the keys pressed
        if self.up_pressed and not self.down_pressed:
            self.player.change_y += self.player.acceleration_rate
        elif self.down_pressed and not self.up_pressed:
            self.player.change_y += -self.player.acceleration_rate
        if self.left_pressed and not self.right_pressed:
            self.player.change_x += -self.player.acceleration_rate
        elif self.right_pressed and not self.left_pressed:
            self.player.change_x += self.player.acceleration_rate

        if self.player.change_x > self.player.max_speed:
            self.player.change_x = self.player.max_speed
        elif self.player.change_x < -self.player.max_speed:
            self.player.change_x = -self.player.max_speed
        if self.player.change_y > self.player.max_speed:
            self.player.change_y = self.player.max_speed
        elif self.player.change_y < -self.player.max_speed:
            self.player.change_y = -self.player.max_speed

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.D:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.D:
            self.right_pressed = False

def main():
    game = MyGame(screen_width, screen_height, game_title)
    arcade.run()

if __name__ == '__main__':
    main()