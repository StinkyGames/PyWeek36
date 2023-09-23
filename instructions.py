import arcade, arcade.gui

class InstructionsView(arcade.View):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.window.set_mouse_visible(True)
        self.window.set_location(int((arcade.get_display_size()[0] - screen_width) / 2),
                          int((arcade.get_display_size()[1] - screen_height) / 2))

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.background = arcade.load_texture('Assets/Menu.png')

    def on_show_view(self):
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

        continue_button = arcade.gui.UIFlatButton(text="Continue", width=200, style=red_style)

        continue_button.on_click = self.on_click_continue

        self.v_box.add(continue_button)

        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.v_box))

    def on_hide_view(self):
        self.manager.disable()

    def on_click_continue(self, event):
        from .level_select import LevelSelectView
        level_view = LevelSelectView(self.screen_width, self.screen_height, None)
        self.window.show_view(level_view)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(
            self.screen_width // 2, self.screen_height // 2,
            self.screen_width, self.screen_height,
            self.background
        )
        self.manager.draw()
        instructions_text = [
            "Use the WSAD keys to move.",
            "Use left mouse click to fire weapon.",
            "Kill drones to recharge your dark matter drive.",
            "Kill the boss to jump to the next sector.",
            "Defeat all the bosses to win!"
        ]
        y = 500
        for line in instructions_text:
            # Center the text
            text_width = len(line) * 14
            x = (self.screen_width - text_width) // 2 + 100
            arcade.draw_text(line, x, y, arcade.color.WHITE, 14)
            y -= 20