import arcade, arcade.gui

class MenuView(arcade.View):
    def __init__(self, screen_width, screen_height, game_title):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title = game_title

        self.window.set_mouse_visible(True)
        self.window.set_location(int((arcade.get_display_size()[0] - screen_width) / 2),
                          int((arcade.get_display_size()[1] - screen_height) / 2))
        
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        
        self.background = arcade.load_texture('Assets/Menu.png')
        self.bg_music = arcade.load_sound(':resources:music/1918.mp3')
        self.bg_music_player = None


    
    def on_show_view(self):
        # Render button
        default_style = {
            "font_name": ("calibri", "arial"),
            "font_size": 14,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": None,
            "bg_color": (21, 19, 21),
            "bg_color_pressed": arcade.color.WHITE,
            "border_color_pressed": arcade.color.WHITE,
            "font_color_pressed": arcade.color.BLACK
        }

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

        title_label = arcade.gui.UILabel(text=f'{self.title}', width=400, height=50, font_size=18, font_name=("calibri", "arial"), text_color=arcade.color.WHITE, align="center")
        start_button = arcade.gui.UIFlatButton(text="Start", width=200, style=red_style)
        instructions_button = arcade.gui.UIFlatButton(text="Instructions", width=200, style=red_style)
        credits_button = arcade.gui.UIFlatButton(text="Credits", width=200, style=red_style)
        exit_button = arcade.gui.UIFlatButton(text="Exit", width=200, style=red_style)

        start_button.on_click = self.on_click_start
        instructions_button.on_click = self.on_click_instructions
        credits_button.on_click = self.on_click_credits
        exit_button.on_click = self.on_click_exit

        self.v_box.add(title_label)
        self.v_box.add(start_button)
        self.v_box.add(instructions_button)
        self.v_box.add(credits_button)
        self.v_box.add(exit_button)

        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.v_box))

    def on_hide_view(self):
        self.manager.disable()

    def on_click_start(self, event):
        from .level_select import LevelSelectView
        level_view = LevelSelectView(self.screen_width, self.screen_height, None)
        self.window.show_view(level_view)
    
    def on_click_instructions(self, event):
        from .instructions import InstructionsView
        instructions_view = InstructionsView(self.screen_width, self.screen_height)
        self.window.show_view(instructions_view)

    def on_click_credits(self, event):
        from .credits import CreditsView
        credits_view = CreditsView(self.screen_width, self.screen_height)
        self.window.show_view(credits_view)

    def on_click_exit(self, event):
        arcade.close_window()

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(
            self.screen_width // 2, self.screen_height // 2,
            self.screen_width, self.screen_height,
            self.background
        )
        if not self.bg_music_player or not self.bg_music_player.playing:
                self.bg_music_player = arcade.play_sound(self.bg_music, .2)
        self.manager.draw()