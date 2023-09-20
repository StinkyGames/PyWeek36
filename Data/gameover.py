import arcade, arcade.gui

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

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_click_restart(self, event):
        from level_select import LevelSelectView
        level_view = LevelSelectView(self.screen_width, self.screen_height)
        self.window.show_view(level_view)

    def on_click_exit(self, event):
        arcade.close_window()