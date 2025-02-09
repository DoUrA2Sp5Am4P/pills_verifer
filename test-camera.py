import pygame
import pygame.camera
from pyzbar.pyzbar import decode
from PIL import Image
pygame.init()
pygame.camera.init()

camera_list = pygame.camera.list_cameras()
camera = pygame.camera.Camera(camera_list[0])

window = pygame.display.set_mode(camera.get_size())
clock = pygame.time.Clock()
camera.start()
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    camera_frame = camera.get_image()
    
    
    strFormat = 'RGBA'
    raw_str = pygame.image.tostring(camera_frame, strFormat, False)
    image = Image.frombytes(strFormat, camera_frame.get_size(), raw_str)
    decoded_QR=decode(image)
    if len(decoded_QR)>0:
        print(decoded_QR[0].data.decode('ascii'))
    window.fill(0)
    window.blit(camera_frame, (0, 0))
    pygame.display.flip()

pygame.quit()
exit()
