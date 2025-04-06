import pygame
import sys
import time
import random

from game.settings import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE, DARK_GRAY, FPS
from game.menu import main_menu
from game.player import Player
from game.chest import Chest
from game.enemy import Enemy
from game.floating_text import FloatingText
from game.inventory import Inventory

# --- FUNCIÓN PARA RECOMPENSAS ALEATORIAS ---
def get_random_reward():
    categories = {
        "arma": ["Espada mágica", "Hacha de cazador", "Cuchillo de cazador"],
        "armadura": ["Armadura de cobre", "Armadura de oro"],
        "zapatos": ["Zapatos de viento", "Zapatos de daño"]
    }

    weights = {
        "Espada mágica": 0.4, "Hacha de cazador": 0.3, "Cuchillo de cazador": 0.3,
        "Armadura de cobre": 0.7, "Armadura de oro": 0.3,
        "Zapatos de viento": 0.5, "Zapatos de daño": 0.5
    }

    category = random.choice(list(categories.keys()))
    options = categories[category]
    item = random.choices(options, weights=[weights[o] for o in options])[0]
    return category, item

# Inicializar PyGame
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

player_name = main_menu(screen)
player = Player(100, 100, player_name)
enemy = Enemy(600, 200, 15)
chests = []
player_start_pos = player.rect.center
spawned_extra_enemies = False
extra_enemies = []

inventory = Inventory(player)

running = True
game_over = False
font = pygame.font.SysFont(None, 60)
font_small = pygame.font.SysFont(None, 20)
floating_texts = []
def draw_background(screen):
  for y in range(0, SCREEN_HEIGHT, 40):
      for x in range(0, SCREEN_WIDTH, 40):
          color = (30 + (x + y) % 40, 0, 60 + (x * y) % 60)
          pygame.draw.rect(screen, color, (x, y, 40, 40))

def spawn_enemies(num):
    return [Enemy(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50), random.choice([15, 20, 25]))
            for _ in range(num)]


while running:
    # Y en el bucle de juego reemplaza screen.fill por esto:
    draw_background(screen)
    keys = pygame.key.get_pressed()
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                inventory.toggle_menu(screen)
        if event.type == pygame.QUIT:
            running = False

    if player.health <= 0:
        game_over = True

    player.handle_keys()
    player.draw(screen)

    if game_over:
        text = font.render("💀 GAME OVER", True, (255, 0, 0))
        screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 30))
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False
        continue

    if enemy:
        enemy.update(player.rect)
        enemy.draw(screen)

        if player.rect.colliderect(enemy.rect):
            enemy.try_attack(player, floating_texts)

        if keys[pygame.K_SPACE]:
            if player.rect.colliderect(enemy.rect):
                current_time = pygame.time.get_ticks()
                if current_time - player.last_attack_time >= 1000:
                    defeated = enemy.take_damage(player.attack, floating_texts)
                    player.last_attack_time = current_time
                    if defeated:
                        chests.append(Chest(enemy.rect.centerx, enemy.rect.centery))
                        enemy = None

    for chest in chests[:]:
        just_opened = chest.update(player.rect, keys)
        chest.draw(screen)

        if just_opened:
            cat, item = get_random_reward()
            inventory.add_item(cat, item)

        if chest.opened and pygame.time.get_ticks() - chest.open_time >= 5000:
            chests.remove(chest)

        distance = ((player.rect.centerx - chest.rect.centerx) ** 2 + (player.rect.centery - chest.rect.centery) ** 2) ** 0.5
        if distance > 500:
            chests.remove(chest)

    for text in floating_texts[:]:
        text.update()
        text.draw(screen)
        if not text.is_alive():
            floating_texts.remove(text)

    distance = ((player.rect.centerx - player_start_pos[0]) ** 2 + (player.rect.centery - player_start_pos[1]) ** 2) ** 0.5
    if distance > 50:
      if len(extra_enemies) == 0:
          extra_enemies.extend(spawn_enemies(2))
          # Reinicia el punto de referencia para que más enemigos aparezcan después de otros 150 px
          player_start_pos = player.rect.center



    for e in extra_enemies[:]:
        e.update(player.rect)
        e.draw(screen)

        if player.rect.colliderect(e.rect):
            e.try_attack(player, floating_texts)

        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - player.last_attack_time >= 1000:
                defeated = e.take_damage(player.attack, floating_texts)
                player.last_attack_time = current_time
                if defeated:
                    extra_enemies.remove(e)
                    chests.append(Chest(e.rect.centerx, e.rect.centery))

    # Mostrar equipo actual (parte inferior izquierda)
    inventory.draw_equipped_text(screen, font_small, 10, SCREEN_HEIGHT - 70)

    # Notificaciones recientes (parte inferior derecha)
    inventory.draw_notifications(screen, font_small, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 70)

    # Controles
    controls = [
        "WASD: Moverse",
        "SPACE: Atacar",
        "E: Abrir cofres",
        "I: Inventario"
    ]

    for i, text in enumerate(controls):
        rendered = font_small.render(text, True, (200, 200, 200))
        screen.blit(rendered, (10, 10 + i * 20))

    inventory.update_draw(screen, events)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
