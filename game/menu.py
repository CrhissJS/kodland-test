import pygame
import pygame_menu
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE

player_name = "Jugador"

def main_menu(screen):
    global player_name
    running = True

    def set_name(value):
        global player_name
        player_name = value

    def start_the_game():
        nonlocal running
        running = False

    theme = pygame_menu.themes.THEME_DARK.copy()
    theme.widget_font = pygame_menu.font.FONT_NEVIS
    theme.title_font_size = 30
    theme.title_font_color = (200, 200, 255)
    theme.widget_font_size = 30
    theme.widget_margin = (25, 15)
    theme.background_color = (30, 30, 60)
    theme.selection_color = (100, 100, 255)

    menu = pygame_menu.Menu(GAME_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT, theme=theme)
    menu.add.text_input('Nombre: ', default='Jugador', onchange=set_name)
    menu.add.button('Jugar', start_the_game)
    menu.add.button('Salir', pygame_menu.events.EXIT)

    def draw_background(surface):
        surface.fill((10, 10, 30))
        for i in range(0, SCREEN_HEIGHT, 10):
            color = (10 + i//4, 10 + i//4, 50 + i//3)
            pygame.draw.rect(surface, color, (0, i, SCREEN_WIDTH, 10))

    while running:
        draw_background(screen)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        menu.update(events)
        menu.draw(screen)
        pygame.display.flip()

    return player_name
