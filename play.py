import pygame
import time
def music_mlay(src):
    pygame.init()
    pygame.mixer.init()
    my_sound = pygame.mixer.Sound(src)
    my_sound.play()
music_mlay('main\hello.wav')
time.sleep(1)