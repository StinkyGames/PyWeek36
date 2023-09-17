import math
import arcade

screen_width = 640
screen_height = 480
game_title = 'Dark Matter'

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__('sprites/player.png')
        # set initial values
        self.center_x = screen_width / 2
        self.center_y = screen_height / 2
        self.z = 0
        self.move_speed = 6.5
        self.scale = 2

    def update(self):
        # set movement
        self.center_x += self.change_x
        self.center_y += self.change_y

        # set boundaries
        if self.right > screen_width:
            self.right = screen_width
        elif self.left < 0:
            self.left = 0
        if self.bottom < 0:
            self.bottom = 0
        elif self.top > screen_height:
            self.top = screen_height

class GamePlay(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.set_mouse_visible(False)
        self.set_location(int((arcade.get_display_size()[0] - screen_width) / 2),
                          int((arcade.get_display_size()[1] - screen_height) / 2))
        # set movement keys, arrow keys or WSAD
        self.move_keys = {
            arcade.key.UP: (0, 1),
            arcade.key.DOWN: (0, -1),
            arcade.key.W: (0, 1),
            arcade.key.S: (0, -1),
            arcade.key.LEFT: (-1, 0),
            arcade.key.RIGHT: (1, 0),
            arcade.key.A: (-1, 0),
            arcade.key.D: (1, 0)
        }
        self.setup_game()  # call the setup/new game function

    def setup_game(self):
        self.player = Player()

    def on_draw(self):
        arcade.start_render()
        self.player.draw()

    def update(self, delta_time):
        self.player.update()

    def on_key_press(self, key, modifiers):
        if key in self.move_keys:
            x_dir, y_dir = self.move_keys[key]
            diagonal_speed = self.player.move_speed / math.sqrt(
                2)  # approximate diagonal movement speed to cardinal movement
            self.player.change_x += x_dir * diagonal_speed
            self.player.change_y += y_dir * diagonal_speed

    def on_key_release(self, key, modifiers):
        if key in self.move_keys:
            x_dir, y_dir = self.move_keys[key]
            diagonal_speed = self.player.move_speed / math.sqrt(
                2)  # approximate diagonal movement speed to cardinal movement
            if self.player.change_x == x_dir * diagonal_speed and (
                    y_dir == 0 or self.player.change_y == y_dir * diagonal_speed):
                self.player.change_x = 0
            if self.player.change_y == y_dir * diagonal_speed and (
                    x_dir == 0 or self.player.change_x == x_dir * diagonal_speed):
                self.player.change_y = 0

def main():
    game = GamePlay(screen_width, screen_height, game_title)
    arcade.run()

if __name__ == '__main__':
    main()