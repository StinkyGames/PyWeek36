import arcade, arcade.gui, random
from player import Player
from enemies import *

#Had to place Game Over view in the same file as otherwise it errors out talking about cyclical module calls
class GameOverView(arcade.View):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.window.set_mouse_visible(True)
        self.window.set_location(int((arcade.get_display_size()[0] - screen_width) / 2),
                          int((arcade.get_display_size()[1] - screen_height) / 2))

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

        red_style = {
            "font_name": ("calibri", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": None,
            "bg_color": arcade.color.REDWOOD,
            "bg_color_pressed": arcade.color.WHITE,
            "border_color_pressed": arcade.color.RED,  # also used when hovered
            "font_color_pressed": arcade.color.RED,
        }

        self.v_box = arcade.gui.UIBoxLayout(space_between=20)

        title_label = arcade.gui.UILabel(text="Game Over", width=400, height=50, font_size=18, font_name=("calibri", "arial"), text_color=arcade.color.WHITE, align="center")
        restart_button = arcade.gui.UIFlatButton(text="Restart", width=200, style=red_style)
        exit_button = arcade.gui.UIFlatButton(text="Exit", width=200, style=red_style)

        restart_button.on_click = self.on_click_restart
        exit_button.on_click = self.on_click_exit

        self.v_box.add(title_label)
        self.v_box.add(restart_button)
        self.v_box.add(exit_button)

        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.v_box))

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_click_restart(self, event):
        game_view = GameView(self.screen_width, self.screen_height)
        self.window.show_view(game_view)

    def on_click_exit(self, event):
        arcade.close_window()

class GameView(arcade.View):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.window.set_mouse_visible(False)
        self.window.set_location(int((arcade.get_display_size()[0] - screen_width) / 2),
                          int((arcade.get_display_size()[1] - screen_height) / 2))
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.setup()

    def setup(self):
        self.player = Player(self.screen_width, self.screen_height)
        self.enemy_list = arcade.SpriteList()

        for i in range(0, 10):
            drone = Drone(10, 1)
            drone.center_x = random.randrange(self.screen_width)
            drone.center_y = random.randrange(self.screen_height)

            self.enemy_list.append(drone)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.AMAZON)
        self.window.set_mouse_visible(False)

    def on_draw(self):
        self.clear()
        self.enemy_list.draw()
        self.player.draw()

        hull_display = f"Hull: {self.player.hull}"
        arcade.draw_text(hull_display, 10, 30, arcade.color.WHITE, 14)

    def on_update(self, delta_time):
        self.player.update()
        self.enemy_list.update()

        for enemy in self.enemy_list:
            enemy.follow_sprite(self.player)

        hit_list = arcade.check_for_collision_with_list(self.player, self.enemy_list)

        for enemy in hit_list:
            enemy.remove_from_sprite_lists()
            self.player.hull -= 1

        if self.player.hull == 0:
            game_over_view = GameOverView(self.screen_width, self.screen_height)
            self.window.set_mouse_visible(True)
            self.window.show_view(game_over_view)

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

    def on_mouse_motion(self, x, y, dx, dy):
        self.player.face_point((x,y))