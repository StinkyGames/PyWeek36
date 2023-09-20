
import arcade
from menu import MenuView

screen_width = 1024
screen_height = 768
game_title = 'Dark Matter'

def main():
    window = arcade.Window(screen_width, screen_height, game_title)
    menu_view = MenuView(screen_width, screen_height)
    window.show_view(menu_view)
    arcade.run()

if __name__ == '__main__':
    main()