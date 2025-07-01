import pygame
pygame.init()
image = pygame.image.load(r'D:\HZY\VsCode\Codes\pythonhyy\images\love.png')
new_size = (100,100)
resized_image = pygame.transform.scale(image, new_size)
pygame.image.save(resized_image, r'D:\HZY\VsCode\Codes\pythonhyy\images\love.png')
