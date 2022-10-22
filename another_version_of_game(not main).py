import sys
import pygame
import os

pygame.init()
width, height = size = 900, 900
screen = pygame.display.set_mode(size)
screen.fill("black")
clock = pygame.time.Clock()
FPS = 60
vek_x, vek_y = 0, 0
flag_vek_x, flag_vek_y = False, False
V_MAX, A_ACCEL, A_DECELER = 50, 5, 5


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


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_m = [line.strip() for line in mapFile]
    max_width = max(map(len, level_m))
    return list(map(lambda x: x.ljust(max_width, '.'), level_m))


tile_images = {'wall': load_image('background_mountain.png'),
               'empty': load_image('background.png')}

player_image = load_image('pers_wof.png')

tile_width = tile_height = 100


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.pos_x, self.pos_y = tile_width * pos_x, tile_height * pos_y
        self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)

    def go(self, vx, vy, lm, plcrd, hw):
        movement = True
        place_rd = plcrd
        """Тут есть баг, надеюсь, что он будет исправлен"""
        """-----"""
        bag1 = 0.5 * hw  # самое оптимальное значение
        bag2 = hw  # самое оптимальное значение
        """-----"""
        pos_x, pos_y = self.pos_x + vx + bag1, self.pos_y + vy + bag1  # тут задействован баг-1
        x11, y11, a1, b1 = pos_x, pos_y, hw, hw
        for crd in lm:
            """Алгоритм столкновения"""
            x21, y21, a2, b2 = crd[1], crd[2], hw, hw
            x12, y12 = x11 + a1 - bag2, y11 + b1 - bag2  # тут задействован баг-2
            x22, y22 = x21 + a2, y21 + b2
            ys1, xs1 = (y11 + y12) * 0.5, (x11 + x12) * 0.5
            ys2, xs2 = (y21 + y22) * 0.5, (x21 + x22) * 0.5
            rx1, ry1 = x12 - xs1, y11 - ys1
            rx2, ry2 = x22 - xs2, y21 - ys2
            delx = abs(xs1 - xs2)
            dely = abs(ys1 - ys2)
            r1 = (delx ** 2 + dely ** 2) ** 0.5
            r2 = (abs(rx1 + rx2) ** 2 + abs(ry1 + ry2) ** 2) ** 0.5

            if r2 >= r1:
                movement = False
                # Основные значения для нахождения столкновения
                # x11;y11;x12;y12 - координаты движущегося тела
                # x21;y21;x22;y22 - координаты рассматриваемогок тела
                # r1;r2 - вычисление расстояний между объектами
                # print('----------------------------------')
                # print(x11, y11, x12, y12, r1)
                # print(x21, y21, x22, y22, r2)
                # print(pos_x, pos_y)
                # print('----------------------------------')

        if movement:
            self.pos_x, self.pos_y = self.pos_x + vx, self.pos_y + vy
            self.rect.x += vx
            self.rect.y += vy


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


def generate_level_mam(level, hw):
    lm = []
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                pass
            elif level[y][x] == '#':
                lm.append(['st', x * hw, y * hw, x * hw + hw, y * hw + hw])
            elif level[y][x] == '@':
                pass
    return lm


def player_crd(level, hw):
    crd = []
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '@':
                crd.append(['st', x * hw, y * hw, x * hw + hw, y * hw + hw])
    return crd


player, level_x, level_y = generate_level(load_level('map.txt'))
level_map = generate_level_mam(load_level('map.txt'), tile_height)
player_coord = player_crd(load_level('map.txt'), tile_height)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


if __name__ == '__main__':
    camera = Camera()
    running = True

    while running:
        keys = pygame.key.get_pressed()
        flag_vek_x, flag_vek_y = True, True

        if keys[pygame.K_UP] and abs(vek_y) < V_MAX:
            vek_y, flag_vek_y = vek_y - A_ACCEL, False
        elif keys[pygame.K_DOWN] and abs(vek_y) < V_MAX:
            vek_y, flag_vek_y = vek_y + A_ACCEL, False
        if keys[pygame.K_RIGHT] and abs(vek_x) < V_MAX:
            vek_x, flag_vek_x = vek_x + A_ACCEL, False
        elif keys[pygame.K_LEFT] and abs(vek_x) < V_MAX:
            vek_x, flag_vek_x = vek_x - A_ACCEL, False

        if flag_vek_y and vek_y < 0:
            vek_y, flag_vek_y = vek_y + A_DECELER, True
        elif flag_vek_y and vek_y > 0:
            vek_y, flag_vek_y = vek_y - A_DECELER, True
        if flag_vek_x and vek_x > 0:
            vek_x, flag_vek_x = vek_x - A_DECELER, True
        elif flag_vek_x and vek_x < 0:
            vek_x, flag_vek_x = vek_x + A_DECELER, True

        player.go(vek_x, vek_y, level_map, player_coord, tile_height)
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            camera.update(player)
            for sprite in all_sprites:
                camera.apply(sprite)
            screen.fill(pygame.Color(0, 0, 0))
            tiles_group.draw(screen)
            player_group.draw(screen)
            clock.tick(FPS)
            pygame.display.flip()

        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)

        screen.fill(pygame.Color(0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
