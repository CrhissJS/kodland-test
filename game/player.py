import pygame
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Player:
    def __init__(self, x, y, name="Jugador"):
        self.radius = 20
        self.speed = 5
        self.rect = pygame.Rect(x, y, self.radius * 2, self.radius * 2)
        self.name = name
        self.health = 100
        self.max_health = 100
        self.attack = 5
        self.last_attack_time = 0

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

        # Limites
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))

    def draw(self, screen):
        # Sombra
        pygame.draw.circle(screen, (50, 50, 50), self.rect.center, self.radius + 2)
        # Brillo borde
        pygame.draw.circle(screen, (0, 200, 150), self.rect.center, self.radius, 2)
        # Centro
        pygame.draw.circle(screen, (0, 255, 180), self.rect.center, self.radius - 2)

        # Nombre
        font = pygame.font.SysFont(None, 20)
        name_text = font.render(self.name, True, (255, 255, 255))
        screen.blit(name_text, (self.rect.x, self.rect.y - 25))

        # Vida
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 10, 40, 5))
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 10, 40 * health_ratio, 5))
