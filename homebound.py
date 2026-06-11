# required dependencies
import pygame
from pygame import mixer

# initialise pygame
pygame.init()
mixer.init()

# configuration
screen = pygame.display.set_mode() 
pygame.display.set_caption('Homebound') 

# load images
bg = pygame.image.load('./assets/images/bg.png')
room = pygame.image.load('./assets/images/room.png')
room2 = pygame.image.load('./assets/images/room2.png')
agent = pygame.image.load('./assets/images/agent.png')
agent2 = pygame.image.load('./assets/images/agent2.png')
dinner = pygame.image.load('./assets/images/dinner.png')
bedroom = pygame.image.load('./assets/images/bedroom.png')
day_bg = pygame.image.load('./assets/images/day.png')
shop_icon = pygame.image.load('./assets/icons/shop_icon.png')
shop = pygame.image.load('./assets/images/shop.png')
coin_icon = pygame.image.load('./assets/icons/coins.png')
close_icon = pygame.image.load('./assets/icons/cross.png')

# load audios
mixer.music.load("./assets/audio/bg.mp3")
knock = mixer.Sound("./assets/audio/knock.mp3")

# play bg music infinitely
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# icons
# get width and height of screen
x, y = screen.get_size()

shop_icon_rect = shop_icon.get_rect()
shop_icon_rect.topright = (x - 100, 10)

coin_rect = coin_icon.get_rect()
coin_rect.midright = (
    shop_icon_rect.left - 120, 
    shop_icon_rect.centery
)

close_rect = close_icon.get_rect(topright=(x - 15, 10))

# initialise variables
font_colour = (0, 0, 0)
font = pygame.font.SysFont('Arial', 50)
text = font.render('Play', True, font_colour)
show_button = True
day = 1
coins = 0
knock_played = False
show_day_text = False
day_text_timer = 0
DAY_TEXT_DURATION = 5
clock = pygame.time.Clock()
current_bg = bg
previous_bg = room
play = False
game_minutes = 17 * 60
REAL_SECONDS_PER_TICK = 5
GAME_MINUTES_PER_TICK = 15
time_passed = 0

# game loop
running = True
while running:
    # update clock 
    dt = clock.tick() / 1000

    # scale and set bg image
    scaled_bg = pygame.transform.scale(current_bg, (x, y))
    screen.blit(scaled_bg, (0, 0))

    # display close button
    screen.blit(close_icon, close_rect)

    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # user clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            # user clicked on play button
            if (x / 2 + 200) <= mouse[0] <= (x / 2 + 200 + 140) and (y/2 - 150) <= mouse[1] <= (y / 2 - 150 + 60):
                current_bg = room
                show_button = False
                play = True
            
            # left click
            elif event.button == 1: 
                # user clicked on shop icon
                if shop_icon_rect.collidepoint(event.pos):
                    previous_bg = current_bg
                    current_bg = shop
                elif close_rect.collidepoint(event.pos):
                    running = False
                    pygame.quit()
                
        # user pressed the escape key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and current_bg == shop:
                current_bg = previous_bg
            
    if play:
        time_passed += dt

        # update in-game time every 15 mins
        if time_passed >= REAL_SECONDS_PER_TICK:
            game_minutes += GAME_MINUTES_PER_TICK
            time_passed = 0
        
        if show_day_text:
            day_text_timer += dt

        # display coin and time in light or dark mode
        if game_minutes < 23 * 60 and current_bg != shop:
            if (current_bg != agent and current_bg != agent2): 
                time_surface = font.render(time_text, True, (255, 255, 255))
                coin_text_surface = font.render(str(coins), True, (255, 255, 255))
                coin_text_rect = coin_text_surface.get_rect(
                    midleft=(coin_rect.right + 15, coin_rect.centery)
                )
            else:
                time_surface = font.render(time_text, True, (0, 0, 0))
                coin_text_surface = font.render(str(coins), True, (0, 0, 0))
                coin_text_rect = coin_text_surface.get_rect(
                    midleft=(coin_rect.right + 15, coin_rect.centery)
                )
        
            screen.blit(time_surface, (10, 10))

        # background logic
        if current_bg != shop and current_bg != day_bg:
            # draw icons on screen
            screen.blit(shop_icon, shop_icon_rect)
            screen.blit(coin_icon, coin_rect)
            screen.blit(coin_text_surface, coin_text_rect)

            if (game_minutes == (17 * 60 + 30) and game_minutes <= (17 * 60 + 45)):
                current_bg = room2
            elif (game_minutes > (17 * 60 + 45) and game_minutes < (18 * 60)):
                current_bg = room
            elif (game_minutes == (18 * 60)):
                if not knock_played:
                    # play knock sound
                    knock.play()
                    knock_played = True
                
                current_bg = agent
            elif (game_minutes >= (18 * 60 + 15) and game_minutes < (19 * 60)):
                knock_played = False
                current_bg = agent2
            elif (game_minutes == (19 * 60)):
                current_bg = dinner
            elif ((game_minutes >= (19 * 60 + 15)) and (game_minutes < (21 * 60))):
                # rice drop game goes here 
                # rmb to remove print statement
                print("rice drop placeholder")
            elif ((game_minutes >= (21 * 60)) and (game_minutes < (23 * 60))):
                current_bg = bedroom 
        
        # handle new day
        if game_minutes >= 23*60 and not show_day_text:
            day += 1
            show_day_text = True
            day_text_timer = 0
            current_bg = day_bg
        
        # reset variables for the new day
        if show_day_text and day_text_timer >= DAY_TEXT_DURATION:
            show_day_text = False
            day_text_timer = 0

            game_minutes = 17 * 60
            time_passed = 0
            current_bg = room

        # text on day_bg
        day_surface = font.render(f"Day {day}", True, (0, 0, 0))
        day_rect = day_surface.get_rect(center=(x // 2, y // 2))

        # display day text on day_bg
        if current_bg == day_bg and show_day_text:
            screen.blit(day_surface, day_rect)

    # calculate in-game hours and mins
    hours = int(game_minutes // 60) % 24
    minutes = int(game_minutes % 60)

    # format in-game time
    display_hour = hours % 12 or 12
    ampm = "PM" if hours >= 12 else "AM"
    time_text = f"{display_hour}:{minutes:02d} {ampm}"
    
    # get mouse position
    mouse = pygame.mouse.get_pos()

    # show play button
    if (show_button == True):
        pygame.draw.rect(screen, (255, 255, 255), [x/2 + 200, y/2 - 150, 140, 60])
        screen.blit(text, (x/2 + 230, y/2 - 150))

    # update screen
    pygame.display.update()

pygame.quit()