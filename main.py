# -*- coding: utf-8 -*-

import pygame
import random
from Player import Player
from Enemy import Enemy
from Projectile import Projectile

global playerBlue

playerRed = (255, 0, 0)
playerBlue = (0, 0, 255)

pygame.init()
size    = (500, 500)
BGCOLOR = (255, 255, 255)
screen = pygame.display.set_mode(size)
scoreFont = pygame.font.Font("fonts/UpheavalPro.ttf", 30)
healthFont = pygame.font.Font("fonts/OmnicSans.ttf", 50)
healthRender = healthFont.render('z', True, pygame.Color('red'))
pygame.display.set_caption("Top Down Shooter")

done = False
hero = pygame.sprite.GroupSingle(Player(screen.get_size(), playerBlue))
player2 = pygame.sprite.GroupSingle(Player(screen.get_size(), playerRed))
enemies = pygame.sprite.Group()
lastEnemy = 0
score = 0
clock = pygame.time.Clock()

def move_entities(hero, enemies, player2, timeDelta):
    score = 0
    hero.sprite.move(screen.get_size(), timeDelta)
    player2.sprite.move(screen.get_size(), timeDelta)
    for enemy in enemies:
        enemy.move(enemies, hero.sprite.rect.topleft, timeDelta)
        enemy.shoot(hero.sprite.rect.topleft)
    for proj in Enemy.projectiles:
        proj.move(screen.get_size(), timeDelta)
        if pygame.sprite.spritecollide(proj, hero, False):
            proj.kill()
            hero.sprite.health -= 1
            if hero.sprite.health <= 0:
                hero.sprite.alive = False
    for proj in Player.projectiles:
        proj.move(screen.get_size(), timeDelta)
        enemiesHit = pygame.sprite.spritecollide(proj, enemies, True)
        if enemiesHit:
            proj.kill()
            score += len(enemiesHit)
    return score

def render_entities(hero, enemies, player2):
    hero.sprite.render(screen)
    player2.sprite.render(screen)
    for proj in Player.projectiles:
        proj.render(screen)
    for proj in Enemy.projectiles:
        proj.render(screen)
    for enemy in enemies:
        enemy.render(screen)
    
    
def process_keys(keys, hero, player2):
    if keys[pygame.K_w]:
        hero.sprite.movementVector[1] -= 1
    if keys[pygame.K_a]:
        hero.sprite.movementVector[0] -= 1
    if keys[pygame.K_s]:
        hero.sprite.movementVector[1] += 1
    if keys[pygame.K_d]:
        hero.sprite.movementVector[0] += 1
    if keys[pygame.K_1]:
        hero.sprite.equippedWeapon = hero.sprite.availableWeapons[0]
    if keys[pygame.K_2]:
        hero.sprite.equippedWeapon = hero.sprite.availableWeapons[1]
    if keys[pygame.K_3]:
        hero.sprite.equippedWeapon = hero.sprite.availableWeapons[2]
    if keys[pygame.K_UP]:
        player2.sprite.movementVector[1] -= 1
    if keys[pygame.K_LEFT]:
        player2.sprite.movementVector[0] -= 1
    if keys[pygame.K_DOWN]:
        player2.sprite.movementVector[1] += 1
    if keys[pygame.K_RIGHT]:
        player2.sprite.movementVector[0] += 1
    if keys[pygame.K_1]:
        player2.sprite.equippedWeapon = player2.sprite.availableWeapons[0]
    if keys[pygame.K_2]:
        player2.sprite.equippedWeapon = player2.sprite.availableWeapons[1]
    if keys[pygame.K_3]:
        player2.sprite.equippedWeapon = player2.sprite.availableWeapons[2]
    if keys[pygame.K_SPACE]:
        player2.sprite.shoot(pygame.mouse.get_pos())
        
def process_mouse(mouse, hero, player2):
    if mouse[0]:
        hero.sprite.shoot(pygame.mouse.get_pos())

def game_loop():
    done = False
    hero = pygame.sprite.GroupSingle(Player(screen.get_size(), playerBlue))
    player2 = pygame.sprite.GroupSingle(Player(screen.get_size(), playerRed))
    enemies = pygame.sprite.Group()
    lastEnemy = pygame.time.get_ticks()
    score = 0
    
    bg = pygame.image.load("bg.png").convert_alpha()

    while hero.sprite.alive and player2.sprite.alive and not done:
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        currentTime = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

        screen.blit(bg, (0,0))
        
        process_keys(keys, hero, player2)
        process_mouse(mouse, hero, player2)
        
        # Enemy spawning process
        if lastEnemy < currentTime - 800 and len(enemies) < 10:
            spawnSide = random.random()
            if spawnSide < 0.25:
                enemies.add(Enemy((0, random.randint(0, size[1]))))
            elif spawnSide < 0.5:
                enemies.add(Enemy((size[0], random.randint(0, size[1]))))
            elif spawnSide < 0.75:
                enemies.add(Enemy((random.randint(0, size[0]), 0)))
            else:
                enemies.add(Enemy((random.randint(0, size[0]), size[1])))
            lastEnemy = currentTime
        
        score += move_entities(hero, enemies, player2, clock.get_time()/17)
        render_entities(hero, enemies, player2)
        
        # Health and score render
        for hp in range(hero.sprite.health):
            screen.blit(healthRender, (15 + hp*35, 0))
        scoreRender = scoreFont.render(str(score), True, pygame.Color('black'))
        scoreRect = scoreRender.get_rect()
        scoreRect.right = size[0] - 20
        scoreRect.top = 20
        screen.blit(scoreRender, scoreRect)
        
        pygame.display.flip()
        clock.tick(120)

done = game_loop()
while not done:
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    currentTime = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    if keys[pygame.K_r]:
        done = game_loop()
pygame.quit()
