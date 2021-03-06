import pygame, os, sys, math
from object_classes import *
from other_objects import *
from arc_missions import missions

os.environ["SDL_VIDEO_CENTERED"] = '1'


#Constants
WIN_W = 1600
WIN_H = 900

def hub(screen, clock, fps, TIMER):
    pygame.init()
    
    bg = BackgroundImage("Sprites/apartment.png")
    
    pygame.mixer.music.stop()
    try:
        pygame.mixer.music.load("Sounds/GrayAreaSong.mp3")
        pygame.mixer.music.play(-1)
    except pygame.error:
        pass

    apartment = desk = True

    platform_group = pygame.sprite.Group()
    hero_group = pygame.sprite.Group()

    hero = Hero(128, 96)
    hero_group.add(hero)

    #dummy_scroll = Scroll_Text("THIS IS DUMMY TEXT",BLACK)

    # Load apartment level
    apartment_level = [
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
        "I         I          I     I          I          I",
        "I                                                I",
        "I                                                I", #| This represents the player height in relation to the level
        "I                                          D     I", #|
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",
    ]
    #80 P wide (50 * 32) and 6 P high (6 * 32)

    #Build level
    x = y = 0
    platforms = []
    for row in apartment_level:
        for col in row:
            if col == "P":
                p = Platform("Sprites/BlackBlock.png", x, y)
                platform_group.add(p)
            if col == "D":
                desk = LaunchDesk(x, y)
                platform_group.add(desk)
            if col == "I":
                i = InvisibleWall(x, y)
                platform_group.add(i)
            x += 32
        y += 32
        x = 0

    #Set Up Camera
    total_width_app = len(apartment_level[0]) * 32
    total_height_app = len(apartment_level) * 32
    camera = Camera(total_width_app, total_height_app)

    #Apartment, mostly eye candy and mechanism for 'desk' level selector
    while apartment:
        hero.menu = False
        TIMER += 1
        clock.tick(fps)
        #Quitting the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.blit(bg.image, camera.apply(bg))
        #Update
        hero_group.update(platform_group, hub)
        camera.update(hero.rect)
        platform_group.update(hero, missions)



        #Put stuff on the screen yo
        for p in platform_group:
            screen.blit(p.image, camera.apply(p))
        for h in hero_group:
            screen.blit(h.image, camera.apply(h))
        screen.blit(desk.image, camera.apply(desk))

        pygame.display.flip()
