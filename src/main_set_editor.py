from pathlib import Path
import struct
import re
import pygame
import sys

from core.set import SetEnemy, SetFile

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128,0,128)

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
SCALE = 5

TYPE_MAP = {
    'Prm0005' : [BLACK, 'Bat'],
    'Prm0006' : [GREEN, 'Spike Wheel'],
    'Prm0008' : [WHITE, 'Bat'],
    'Prm0012' : [RED, 'Bustard'],
    'Prm0088' : [(125, 125, 10), 'Orange Soldier'],
    'Prm0083': [BLACK, 'Shooting Crab']
}

class Enemy(pygame.sprite.Sprite):
    def __init__(self, set_enemy: SetEnemy):
        super().__init__()
        self.set_enemy = set_enemy

        if type in TYPE_MAP.keys():
            pair = TYPE_MAP.get(set_enemy.type)
            self.color = pair[0]
            self.name = pair[1]
        else:
            self.color = BLACK
            self.name = set_enemy.type

        width = 10
        height = 10
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()

        # Only ints are allowed
        x = int(self.set_enemy.x)
        y = int(self.set_enemy.y)
        self.rect.move_ip(x * SCALE, y * SCALE)
        self.reset_color()

    def reset_color(self):
        self.image.fill(self.color)

class Level():
    def __init__(self, enemies):
        self.enemy_list = pygame.sprite.Group()
        self.world_shift_x = 0
        self.world_shift_y = 0

        for enemy in enemies:
            enemy_sprite = Enemy(enemy)
            self.enemy_list.add(enemy_sprite)

    def get_sprite_enemy(self, idx):
        return self.enemy_list.sprites()[idx]

    def update(self):
        self.enemy_list.update()

    def draw(self, screen):
        screen.fill(BLUE)
        self.enemy_list.draw(screen)

    def shift_world(self, shift_x, shift_y):
        temp_x = self.world_shift_x + shift_x
        temp_y = self.world_shift_y + shift_y

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
            enemy.rect.y += shift_y

        self.world_shift_x = temp_x
        self.world_shift_y = temp_y

    def shift_reset(self):
        for enemy in self.enemy_list:
            enemy.rect.x -= self.world_shift_x
            enemy.rect.y -= self.world_shift_y
        self.world_shift_x = 0
        self.world_shift_y = 0


if __name__ == '__main__':
    # Load SET
    set_file = SetFile(r'C:\Users\xeroj\Desktop\Local_Programming\Python-RockManX8\game\set\Set06_00.set')

    pygame.init()
    pygame.font.init()
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("X8 Level Editor Prototype")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    change_x = 0
    change_y = 0
    current_level = Level(set_file.enemies)

    enemy_idx = 0

    font = pygame.font.SysFont('Verdana', 20)
    text_level_name = font.render(set_file.stage_name, False, WHITE)
    text_enemy_info = font.render('Use [ and ] keys to step through the enemy list.', False, WHITE)

    # -------- Main Program Loop -----------
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    change_x = 20
                if event.key == pygame.K_RIGHT:
                    change_x = -20
                if event.key == pygame.K_UP:
                    change_y = 6
                if event.key == pygame.K_DOWN:
                    change_y = -6

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT \
                        or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    change_x = change_y = 0
                if event.key == pygame.K_RIGHTBRACKET or event.key == pygame.K_LEFTBRACKET:
                    # Unselect previous sprite
                    prev_sprite_enemy = current_level.get_sprite_enemy(enemy_idx)
                    prev_sprite_enemy.reset_color()

                    # Move sprite index
                    if event.key == pygame.K_LEFTBRACKET:
                        enemy_idx -= 1
                    else:
                        enemy_idx += 1

                    # Reset camera
                    current_level.shift_reset()

                    # Get enemy sprite and set info
                    enemy_idx = max(min(len(current_level.enemy_list) - 1, enemy_idx), 0)
                    enemy_sprite: Enemy = current_level.get_sprite_enemy(enemy_idx)
                    enemy_set = enemy_sprite.set_enemy

                    # Select by coloring and centering on screen
                    enemy_sprite.image.fill(PURPLE)
                    x = -int(enemy_set.x * SCALE) + SCREEN_WIDTH/2
                    y = -int(enemy_set.y * SCALE)+SCREEN_HEIGHT/2
                    current_level.shift_world(x, y)

                    # UI text
                    st = f'Enemy: {enemy_sprite.name}, #{enemy_idx}/{len(current_level.enemy_list) - 1}'
                    text_enemy_info = font.render(st, True, WHITE)

        # Updates
        current_level.shift_world(change_x, change_y)
        current_level.update()

        # == Draw UI on top of level
        current_level.draw(screen)
        screen.blit(text_level_name, (0, 0))
        screen.blit(text_enemy_info, (0, 30))
        clock.tick(60)
        pygame.display.flip()

    pygame.quit()
    sys.exit()