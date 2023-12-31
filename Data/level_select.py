import arcade, arcade.gui

class LevelSelectView(arcade.View):
    def __init__(self, screen_width, screen_height, hide_boss):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.window.set_mouse_visible(True)
        self.window.set_location(int((arcade.get_display_size()[0] - screen_width) / 2),
                          int((arcade.get_display_size()[1] - screen_height) / 2))

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.background = arcade.load_texture('Assets/Menu.png')

        self.hide_boss = hide_boss

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

        title_label = arcade.gui.UILabel(text="Level Select", width=400, height=50, font_size=18, font_name=("calibri", "arial"), text_color=arcade.color.WHITE, align="center")
        onslaught_button = arcade.gui.UIFlatButton(text="Onslaught", width=200, style=red_style)
        reaver_button = arcade.gui.UIFlatButton(text="Reaver", width=200, style=red_style)
        bulwark_button = arcade.gui.UIFlatButton(text="Bulwark", width=200, style=red_style)
        exit_button = arcade.gui.UIFlatButton(text="Exit", width=200, style=red_style)

        onslaught_button.on_click = self.on_click_onslaught
        reaver_button.on_click = self.on_click_reaver
        bulwark_button.on_click = self.on_click_bulwark
        exit_button.on_click = self.on_click_exit

        self.v_box.add(title_label)
        self.v_box.add(onslaught_button)
        self.v_box.add(reaver_button)
        self.v_box.add(bulwark_button)
        # Remove boss choices if they exist in the dictionary that is defined from game.py when killing a boss
        from . import values
        if "Onslaught" in values.hide_boss:
            self.v_box.remove(onslaught_button)
        if "Reaver" in values.hide_boss:
            self.v_box.remove(reaver_button)
        if "Bulwark" in values.hide_boss:
            self.v_box.remove(bulwark_button)
        self.v_box.add(exit_button)
        # Take you to the winner screen if all boss names exist in the dictionary
        if all(boss in values.hide_boss for boss in ["Onslaught", "Reaver", "Bulwark"]):
            from .winner import WinView
            win_view = WinView(self.screen_width, self.screen_height)
            self.window.show_view(win_view)

        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.v_box))

    def on_hide_view(self):
        self.manager.disable()

    def on_click_onslaught(self, event):
        from .game import GameView
        game_view = GameView(self.screen_width, self.screen_height, boss="Onslaught")
        self.window.show_view(game_view)
    
    def on_click_reaver(self, event):
        from .game import GameView
        game_view = GameView(self.screen_width, self.screen_height, boss="Reaver")
        self.window.show_view(game_view)
    
    def on_click_bulwark(self, event):
        from .game import GameView
        game_view = GameView(self.screen_width, self.screen_height,boss="Bulwark")
        self.window.show_view(game_view)
    
    def on_click_exit(self, event):
        arcade.close_window()

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(
            self.screen_width // 2, self.screen_height // 2,
            self.screen_width, self.screen_height,
            self.background
        )
        self.manager.draw()