import arcade, arcade.gui
from Views.instructions import InstructionsView

class MenuView(arcade.View):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.window.set_mouse_visible(True)
        self.window.set_location(int((arcade.get_display_size()[0] - screen_width) / 2),
                          int((arcade.get_display_size()[1] - screen_height) / 2))

        self.screen_width = screen_width
        self.screen_height = screen_height
    
    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)

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

        title_label = arcade.gui.UILabel(text="Dark Matter", width=400, height=50, font_size=18, font_name=("calibri", "arial"), text_color=arcade.color.BLACK, align="center")
        start_button = arcade.gui.UIFlatButton(text="Start", width=200, style=red_style)
        exit_button = arcade.gui.UIFlatButton(text="Exit", width=200, style=red_style)

        start_button.on_click = self.on_click_start
        exit_button.on_click = self.on_click_exit

        self.v_box.add(title_label)
        self.v_box.add(start_button)
        self.v_box.add(exit_button)

        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.v_box))

    def on_click_start(self, event):
        instructions_view = InstructionsView(self.screen_width, self.screen_height)
        self.window.show_view(instructions_view)

    def on_click_exit(self, event):
        arcade.close_window()

    def on_draw(self):
        self.clear()
        self.manager.draw()