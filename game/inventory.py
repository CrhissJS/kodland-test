import pygame
import pygame_menu
import time
import random

class Inventory:
    def __init__(self, player):
        self.items = {"arma": [], "armadura": [], "zapatos": []}
        self.equipped = {"arma": None, "armadura": None, "zapatos": None}
        self.menu_open = False
        self.menu = None
        self.notifications = []
        self.player = player

    def add_item(self, category, item_name):
        if item_name not in self.items[category]:
            self.items[category].append(item_name)
            self.notifications.append((f"+ {item_name}", time.time()))
            print(f"🧳 Añadido: {item_name}")

    def equip_item(self, category, item_name):
        self.equipped[category] = item_name
        print(f"🗡️ Equipado: {item_name}")
        self.apply_stats()

    def unequip_item(self, category):
        self.equipped[category] = None
        print(f"❌ Desequipado: {category}")
        self.apply_stats()

    def apply_stats(self):
        self.player.attack = 5
        self.player.speed = 5
        self.player.defense = 0

        # Armas
        arma = self.equipped["arma"]
        if arma == "Espada mágica":
            self.player.attack = 10
        elif arma == "Hacha de cazador":
            self.player.attack = 8
        elif arma == "Cuchillo de cazador":
            self.player.attack = 6

        # Armaduras
        armadura = self.equipped["armadura"]
        if armadura == "Armadura de cobre":
            self.player.defense = 2
        elif armadura == "Armadura de oro":
            self.player.defense = 5

        # Zapatos
        zapatos = self.equipped["zapatos"]
        if zapatos == "Zapatos de viento":
            self.player.speed = 8
        elif zapatos == "Zapatos de daño":
            self.player.attack += 2

    def toggle_menu(self, screen):
        if not self.menu_open:
            self.menu = pygame_menu.Menu("🎒 Inventario", 400, 300, theme=pygame_menu.themes.THEME_DARK)
            for category in self.items:
                for item in self.items[category]:
                    self.menu.add.button(f"Equipar {item}", lambda i=item, c=category: self.equip_item(c, i))
                if self.equipped[category]:
                    self.menu.add.button(f"Desequipar {category}", lambda c=category: self.unequip_item(c))
            self.menu.add.button("Cerrar", self.close_menu)
        self.menu_open = not self.menu_open

    def close_menu(self):
        self.menu_open = False

    def update_draw(self, screen, events):
        if self.menu_open and self.menu:
            self.menu.update(events)
            self.menu.draw(screen)

    def draw_equipped_text(self, screen, font, x, y):
        for i, (key, item) in enumerate(self.equipped.items()):
            name = item if item else "ninguna"
            line = f"{key.capitalize()}: {name}"
            text = font.render(line, True, (255, 255, 0))
            screen.blit(text, (x, y + i * 20))

    def draw_notifications(self, screen, font, x, y):
        now = time.time()
        for msg, t in self.notifications[:]:
            if now - t > 2:
                self.notifications.remove((msg, t))
            else:
                txt = font.render(msg, True, (0, 255, 255))
                screen.blit(txt, (x, y))
                y += 25
