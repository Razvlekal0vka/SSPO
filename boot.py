import pygame
import sys
import os

pygame.init()
width, height = size = 960, 540
screen = pygame.display.set_mode(size)
pygame.display.set_caption('[INSERT ANY NAME]')
screen.fill("black")
clock = pygame.time.Clock()
FPS = 60


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def terminate():
    pygame.quit()
    sys.exit()


class Boot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)

        self.fon_image = pygame.transform.scale(load_image('dispet.jpg'), (width, height))
        self.name_image = pygame.transform.scale(load_image('RBWOF.png'), (width, height))
        self.click_image = pygame.transform.scale(load_image('CIYWETG2.png'), (width, height))
        self.click_image_alf = self.name_image_alf = 255

    def start_screen_fon(self):
        screen.blit(self.fon_image, (0, 0))

    def start_screen_click(self):
        # self.click_image.set_alpha(255)
        self.click_image.set_alpha(self.click_image_alf)
        screen.blit(self.click_image, (0, 0))

    def start_screen_name(self):
        # self.name_image.set_alpha(255)
        self.name_image.set_alpha(self.name_image_alf)
        screen.blit(self.name_image, (0, 0))


all_sprites = pygame.sprite.Group()
boot = Boot()

if __name__ == '__main__':

    boot.start_screen_fon()
    boot.start_screen_name()

    '''boot.start_screen_click()'''

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)
