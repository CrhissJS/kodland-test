import pygame
import random
from game.floating_text import FloatingText

class Enemy:
    id_counter = 1

    def __init__(self, x, y, health):
        self.health = health
        self.max_health = health
        self.last_attack_time = pygame.time.get_ticks()
        self.attack_cooldown = 5000

        if health == 15:
            self.color = (255, 100, 100)
            self.shape = "circle"
            self.damage = 1
        elif health == 20:
            self.color = (255, 140, 0)
            self.shape = "square"
            self.damage = 2
        else:
            self.color = (200, 0, 255)
            self.shape = "diamond"
            self.damage = 3

        self.rect = pygame.Rect(x, y, 32, 32)
        self.name = f"Goblin {Enemy.id_counter}"
        Enemy.id_counter += 1
        self.speed = 1.2

    def update(self, player_rect):
        if player_rect.x > self.rect.x:
            self.rect.x += self.speed
        elif player_rect.x < self.rect.x:
            self.rect.x -= self.speed
        if player_rect.y > self.rect.y:
            self.rect.y += self.speed
        elif player_rect.y < self.rect.y:
            self.rect.y -= self.speed

    def draw(self, screen):
        center = self.rect.center
        if self.shape == "circle":
            pygame.draw.circle(screen, self.color, center, 16)
        elif self.shape == "square":
            pygame.draw.rect(screen, self.color, self.rect)
        elif self.shape == "diamond":
            points = [
                (center[0], self.rect.top),
                (self.rect.right, center[1]),
                (center[0], self.rect.bottom),
                (self.rect.left, center[1])
            ]
            pygame.draw.polygon(screen, self.color, points)

        font = pygame.font.SysFont(None, 20)
        name_text = font.render(self.name, True, (255, 255, 255))
        screen.blit(name_text, (self.rect.x, self.rect.y - 25))

        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 10, 32, 5))
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 10, 32 * health_ratio, 5))

    def take_damage(self, amount, floating_texts):
        self.health -= amount
        floating_texts.append(
            FloatingText(self.rect.centerx, self.rect.y, f"-{amount}", (255, 255, 0))
        )
        return self.health <= 0

    def try_attack(self, player, floating_texts):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_cooldown:
            player.health -= self.damage
            self.last_attack_time = current_time
            self.rect.x += 5
            floating_texts.append(
                FloatingText(player.rect.centerx, player.rect.y, f"-{self.damage}", (255, 50, 50))
            )
