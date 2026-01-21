import pygame
import math
import random
import time


pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Searching for an entity that doesn't exist")
clock = pygame.time.Clock()

try:
    font = pygame.font.SysFont("Arial", 28)
    title_font = pygame.font.SysFont("Arial", 40, bold=True)
except:
    font = pygame.font.Font(None, 32)
    title_font = pygame.font.Font(None, 48)


WHITE = (255, 255, 255)
BG_COLOR = (10, 10, 15) 
PLAYER_COLOR = (0, 255, 100)
MONSTER_COLOR = (255, 50, 50)
TRASH_COLOR = (80, 80, 90)
EXIT_COLOR = (255, 215, 0)
ITEM_COLOR = (255, 165, 0)  
RED = (255, 0, 0)  


player = pygame.Rect(50, 50, 30, 30)
monster = pygame.Rect(700, 50, 40, 40)
exit_door = pygame.Rect(740, 540, 40, 40)

obstacles = []
for i in range(15):
    obs = pygame.Rect(random.randint(150, 600), random.randint(100, 500), 40, 40)
    obstacles.append(obs)

items = []  
for i in range(5): 
    item = pygame.Rect(random.randint(150, 600), random.randint(100, 500), 20, 20)
    items.append(item)

noise_level = 0
noise_threshold = 100
is_monster_awake = False
game_over = False
won = False
state = "STORY"
running = True
countdown = 30  


while running:
    screen.fill(BG_COLOR)  
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if state == "STORY":
                state = "PLAYING"  

        if state == "GAME OVER" and event.key == pygame.K_r:
            player.topleft = (50, 50)
            monster.topleft = (700, 50)
            noise_level = 0
            is_monster_awake = False
            game_over = False
            won = False

            countdown = 30

            items = []
            for i in range(5):
                item = pygame.Rect(
                    random.randint(150, 600),
                    random.randint(100, 500),
                    20, 20
                )
                items.append(item)

            state = "PLAYING"

    if state == "STORY":
        lines = [
        "SEARCHING FOR A NIL",
        "",
        "You always loved the thrill of abandoned places.",
        "",
        "Deep in the woods, you found it: ",
        "",
        "the mansion from the local legends.",
        "",
        "But the moment you stepped inside",
        "",
        "heavy doors locked themselves.",
        "",
        "The house is not empty. ",
        "",
        "Something is here, ",
        "",
        "and it is listening.",
        "",
        "It will find you.",
        "",
        "",
        "ARROWS: Move | SHIFT: Sneak faster",
        "",
        "GOAL: Find the back exit. Stay quiet. ",
        "",
        "collect all the keys (orange boxes) ",
        "",
        "that are scattered around the area",
        "",
        "PRESS ANY KEY TO ENTER",
    ]

        line_spacing = 18 
        total_height = len(lines) * line_spacing
        start_y = (HEIGHT - total_height) // 2

        for i, line in enumerate(lines):
            if i == 0:
                    text_surf = title_font.render(line, True, WHITE)

        
            elif line == "PRESS ANY KEY TO ENTER":
                    text_surf = title_font.render(line, True, WHITE)
                

            else:
                text_surf = font.render(line, True, WHITE)

            text_rect = text_surf.get_rect(
            center=(WIDTH // 2, start_y + i * line_spacing)
            )
            screen.blit(text_surf, text_rect)

    elif state == "PLAYING":
        if not game_over:
            countdown -= clock.get_time() / 1000  
            if countdown <= 0:
                game_over = True
                won = False

           
            keys = pygame.key.get_pressed()
            speed = 5  
            noise_inc = 0.2
            if keys[pygame.K_LSHIFT]:
                speed = 10  
                noise_inc = 2.0
            
            mx, my = 0, 0
            if keys[pygame.K_LEFT]: mx = -speed
            if keys[pygame.K_RIGHT]: mx = speed
            if keys[pygame.K_UP]: my = -speed
            if keys[pygame.K_DOWN]: my = speed

            player.x += mx
            player.y += my

            if mx != 0 or my != 0:
                noise_level += noise_inc

            
            for obs in obstacles:
                if player.colliderect(obs):
                    noise_level += 20
                    player.x -= mx
                    player.y -= my

            
            for item in items[:]:
                if player.colliderect(item):
                    speed += 2  
                    items.remove(item)  
                   
            
            if noise_level > 0:
                noise_level -= 0.5

    
            if noise_level >= noise_threshold:
                is_monster_awake = True

            if is_monster_awake:
                dx = player.x - monster.x
                dy = player.y - monster.y
                divba = math.hypot(dx, dy)
                if divba != 0:
                    monster.x += (dx / divba) * 2.8
                    monster.y += (dy / divba) * 2.8
                
                if noise_level <= 0:  
                    is_monster_awake = False

            if player.colliderect(monster):
                game_over = False
                state = "GAME OVER"
            if player.colliderect(exit_door) and len(items) == 0:  
                won = True
                state = "GAME OVER"

            
            pygame.draw.rect(screen, EXIT_COLOR, exit_door)
            for obs in obstacles:
                pygame.draw.rect(screen, TRASH_COLOR, obs)
            for item in items:
                pygame.draw.rect(screen, ITEM_COLOR, item) 
            pygame.draw.rect(screen, PLAYER_COLOR, player)
            pygame.draw.rect(screen, MONSTER_COLOR, monster)


            bar_color = (255, 50, 50) if is_monster_awake else WHITE
            pygame.draw.rect(screen, bar_color, (20, 550, max(0, min(noise_level * 2, 200)), 20))
            lbl = "IT HEARS YOU!" if is_monster_awake else "Noise Level"
            screen.blit(font.render(lbl, True, WHITE), (20, 520))

            
            timer_text = font.render(f"Time Left: {int(countdown)}", True, WHITE)
            screen.blit(timer_text, (WIDTH - 200, 20))

        elif state == "PLAYING":
            countdown -= clock.get_time() / 1000
        if countdown <= 0:
                won = False
                state = "GAME OVER"

        pygame.draw.rect(screen, EXIT_COLOR, exit_door)
        for obs in obstacles:
            pygame.draw.rect(screen, TRASH_COLOR, obs)
        for item in items:
            pygame.draw.rect(screen, ITEM_COLOR, item)
        pygame.draw.rect(screen, PLAYER_COLOR, player)
        pygame.draw.rect(screen, MONSTER_COLOR, monster)

        bar_color = RED if is_monster_awake else WHITE
        pygame.draw.rect(screen, bar_color, (20, 550, max(0, min(noise_level * 2, 200)), 20))
        lbl = "IT HEARS YOU!" if is_monster_awake else "Noise Level"
        screen.blit(font.render(lbl, True, WHITE), (20, 520))

        timer_text = font.render(f"Time Left: {int(countdown)}", True, WHITE)
        screen.blit(timer_text, (WIDTH - 200, 20))


    elif state == "GAME OVER":
        msg = "YOU ESCAPED!" if won else "YOU DIED!"
        end_text = title_font.render(msg, True, WHITE)
        restart_text = font.render("PRESS R TO RESTART", True, WHITE)

        screen.blit(end_text, end_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30)))
        screen.blit(restart_text, restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))
    
    pygame.display.flip()
    clock.tick(60) 

pygame.quit()