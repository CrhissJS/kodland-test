import pygame

class Chest:
    def __init__(self, x, y):
        self.frames = [
            pygame.image.load(f"assets/chests/frames/chest_{i}.png").convert_alpha()
            for i in range(8)
        ]

        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.is_opening = False
        self.opened = False
        self.animation_speed = 0.2
        self.animation_counter = 0

    def update(self, player_rect, keys):
        just_opened = False

        if not self.opened and self.rect.colliderect(player_rect) and keys[pygame.K_e]:
            self.is_opening = True

        if self.is_opening and not self.opened:
            self.animation_counter += self.animation_speed
            if self.animation_counter >= 1:
                self.animation_counter = 0
                self.frame_index += 1
                if self.frame_index >= len(self.frames):
                    self.frame_index = len(self.frames) - 1
                    self.opened = True
                    self.open_time = pygame.time.get_ticks()
                    just_opened = True
                self.image = self.frames[self.frame_index]

        return just_opened



    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def give_reward(self):
        self.open_time = pygame.time.get_ticks()
        print("🎁 ¡Has obtenido una recompensa!")
