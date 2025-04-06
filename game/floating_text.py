import pygame

class FloatingText:
    def __init__(self, x, y, text, color=(255, 255, 255)):
        self.font = pygame.font.SysFont(None, 24)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect(center=(x, y))
        self.lifetime = 60  # frames a mostrar (~1 seg a 60 FPS)
        self.velocity = -1  # sube lentamente

    def update(self):
        self.rect.y += self.velocity
        self.lifetime -= 1

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_alive(self):
        return self.lifetime > 0
