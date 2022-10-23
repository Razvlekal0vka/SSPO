import os
import random
import sys
from enum import Enum
from random import randint
from tkinter import Image
import pygame
from PIL import Image, ImageDraw
import random

pygame.init()
size = WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode(size)
FPS = 60
clock = pygame.time.Clock()


class MAP_ENTRY_TYPE(Enum):
    """Необходим для генирации лабиринтов"""
    MAP_EMPTY = 0,
    MAP_BLOCK = 1,


class WALL_DIRECTION(Enum):
    """Необходим для генирации лабиринтов"""
    WALL_LEFT = 0,
    WALL_UP = 1,
    WALL_RIGHT = 2,
    WALL_DOWN = 3,


class Map:
    def __init__(self):

        self.width = 25
        self.height = 25
        self.map = [[0 for x in range(self.width)] for y in range(self.height)]

    def setMap(self, x, y, value):

        if value == MAP_ENTRY_TYPE.MAP_EMPTY:
            self.map[y][x] = 0
        elif value == MAP_ENTRY_TYPE.MAP_BLOCK:
            self.map[y][x] = 1

    def isMovable(self, x, y):

        return self.map[y][x] != 1

    def isValid(self, x, y):

        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return True

    def showMap(self):

        map = []
        for row in self.map:
            s = ''
            for entry in row:
                if entry == 0:
                    s += ' '
                elif entry == 1:
                    s += '#'
                else:
                    s += ' X'
            map.append(s)
        maze_map = []
        for i in map:
            line = []
            for j in range(len(i)):
                line.append(i[j])
            maze_map.append(line)
        return maze_map


def recursiveDivision(map, x, y, width, height, wall_value):
    def getWallIndex(start, length):

        assert length >= 3
        wall_index = randint(start + 1, start + length - 2)
        if wall_index % 2 == 1:
            wall_index -= 1
        return wall_index

    def generateHoles(map, x, y, width, height, wall_x, wall_y):

        holes = []

        hole_entrys = [(randint(x, wall_x - 1), wall_y), (randint(wall_x + 1, x + width - 1), wall_y),
                       (wall_x, randint(y, wall_y - 1)), (wall_x, randint(wall_y + 1, y + height - 1))]
        margin_entrys = [(x, wall_y), (x + width - 1, wall_y), (wall_x, y), (wall_x, y + height - 1)]
        adjacent_entrys = [(x - 1, wall_y), (x + width, wall_y), (wall_x, y - 1), (wall_x, y + height)]
        for i in range(4):
            adj_x, adj_y = (adjacent_entrys[i][0], adjacent_entrys[i][1])
            if map.isValid(adj_x, adj_y) and map.isMovable(adj_x, adj_y):
                map.setMap(margin_entrys[i][0], margin_entrys[i][1], MAP_ENTRY_TYPE.MAP_EMPTY)
            else:
                holes.append(hole_entrys[i])

        ignore_hole = randint(0, len(holes) - 1)
        for i in range(0, len(holes)):
            if i != ignore_hole:
                map.setMap(holes[i][0], holes[i][1], MAP_ENTRY_TYPE.MAP_EMPTY)

    if width <= 1 or height <= 1:
        return

    wall_x, wall_y = (getWallIndex(x, width), getWallIndex(y, height))

    for i in range(x, x + width):
        map.setMap(i, wall_y, wall_value)
    for i in range(y, y + height):
        map.setMap(wall_x, i, wall_value)

    generateHoles(map, x, y, width, height, wall_x, wall_y)

    recursiveDivision(map, x, y, wall_x - x, wall_y - y, wall_value)
    recursiveDivision(map, x, wall_y + 1, wall_x - x, y + height - wall_y - 1, wall_value)
    recursiveDivision(map, wall_x + 1, y, x + width - wall_x - 1, wall_y - y, wall_value)
    recursiveDivision(map, wall_x + 1, wall_y + 1, x + width - wall_x - 1, y + height - wall_y - 1, wall_value)


def doRecursiveDivision(map):
    for x in range(0, map.width):
        map.setMap(x, 0, MAP_ENTRY_TYPE.MAP_BLOCK)
        map.setMap(x, map.height - 1, MAP_ENTRY_TYPE.MAP_BLOCK)

    for y in range(0, map.height):
        map.setMap(0, y, MAP_ENTRY_TYPE.MAP_BLOCK)
        map.setMap(map.width - 1, y, MAP_ENTRY_TYPE.MAP_BLOCK)

    recursiveDivision(map, 1, 1, map.width - 2, map.height - 2, MAP_ENTRY_TYPE.MAP_BLOCK)


def Error_of_creating_maze():
    map_m = Map()
    doRecursiveDivision(map_m)
    maze = map_m.showMap()
    return maze


class Map_generation:
    def __init__(self):

        print('Инициализация')
        self.number_of_buildings = 3
        self.number_of_streets = self.number_of_buildings + 1
        self.house = 50
        self.street = 5
        self.border = 1
        self.size_of_the_city = self.number_of_streets * self.street + self.number_of_buildings * self.house + 2 * self.border
        self.map_city = []

        self.map_brown_house = []
        self.map_purple_house = []
        self.map_green_house = []
        self.map_yellow_house = []
        self.map_street = []
        self.crossroads = []
        self.map_border = []

        self.filling_out_the_city_list()

    def filling_out_the_city_list(self):

        k = 0
        image = Image.open('data/111.png')  # Открываем изображение
        draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования
        width = image.size[0]  # Определяем ширину
        height = image.size[1]  # Определяем высоту
        pix = image.load()  # Выгружаем значения пикселей

        for y in range(height):
            line = []
            for x in range(width):
                line.append(['.'])
            self.map_city.append(line)

        for y in range(height):
            for x in range(width):
                r = pix[x, y][0]  # узнаём значение красного цвета пикселя
                g = pix[x, y][1]  # зелёного
                b = pix[x, y][2]  # синего


                if randint(1, 100) > 90:
                    hh = 's'
                else:
                    hh = '.'

                if (r, g, b) == (255, 255, 255):
                    self.map_city[y][x] = ['wall_2', '#']
                elif (r, g, b) == (237, 28, 36):
                    print(600)
                    self.map_city[y][x] = ['wall_1', '#']
                elif (r, g, b) == (163, 73, 164):
                    print(600)
                    self.map_city[y][x] = ['f', hh]
                elif (r, g, b) == (34, 177, 76):
                    print(600)
                    self.map_city[y][x] = ['g', hh]
                elif (r, g, b) == (0, 0, 0):
                    print(600)
                    self.map_city[y][x] = ['b', hh]
                elif (r, g, b) == (255, 127, 39):
                    print(600)
                    self.map_city[y][x] = ['or', hh]
                elif (r, g, b) == (255, 242, 0):
                    print(600)
                    self.map_city[y][x] = ['y', hh]
                elif (r, g, b) == (63, 72, 204):
                    print(600)
                    self.map_city[y][x] = ['blue', hh]
                elif (r, g, b) == (195, 195, 195):
                    print(600)
                    self.map_city[y][x] = ['lg', hh]
                elif (r, g, b) == (127, 127, 127):
                    print(600)
                    self.map_city[y][x] = ['g', hh]
                else:
                    self.map_city[y][x] = ['wall_2', hh]

        self.map_city[40][50] = ['g', '@']

        print(1)
        self.write_in_txt()

    def write_in_txt(self):
        print(2)

        with open('test_data/Test_map.txt', 'w') as writing_file:
            for element in self.map_city:
                print(element, file=writing_file)

    def map_level(self):

        return self.map_city


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    text = ['']
    fon = pygame.transform.scale(load_image('start/aeroport-samolety-vid-sverkhu.jpg'), (WIDTH, HEIGHT))
    name = pygame.transform.scale(load_image('start/name.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    screen.blit(name, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 550
    t = 0


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if t != 1:
                    for line in text:
                        string_rendered = font.render(line, True, pygame.Color('orange'))
                        intro_rect = string_rendered.get_rect()
                        text_coord += 10
                        intro_rect.top = text_coord
                        intro_rect.x = 10
                        text_coord += intro_rect.height
                        screen.blit(string_rendered, intro_rect)
                        pygame.display.flip()
                        t = 1
                elif t == 1:
                    return
        pygame.display.flip()
        clock.tick(FPS * 2)


def load_image(name, color_key=None):
    fullname = os.path.join('test_data/', name)
    if not os.path.isfile(fullname):
        print(f'Файл с изображением \'{fullname}\' не найден')
        sys.exit()
    image = pygame.image.load(fullname)
    if color_key:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "test_data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, enemies, x, y = None, [], None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x][1] == '@':
                print(x, y)
                Tile(level[y][x][0], x, y)
                new_player = Player(x, y)
            elif level[y][x][1] == 'd':
                Tile(level[y][x][0], x, y)
                n = random.randint(1, 5)
                if n == 5:
                    Tile(str(level[y][x][1]) + str(1), x, y)
                elif 2 <= n <= 4:
                    Tile(str(level[y][x][1]) + str(2), x, y)
                else:
                    Tile(str(level[y][x][1]) + str(2), x, y)
            elif level[y][x][1] == 'e':
                Tile(level[y][x][0], x, y)
                Emerald('emerald', x, y)
            elif level[y][x][1] == 'f1':
                Tile(level[y][x][0], x, y)
                Object('fountain', x, y)
            else:
                Tile(level[y][x][0], x, y)
    return new_player, enemies, len(level[0]), len(level)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Object(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(object_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image_lr
        self.rect = self.image.get_rect().move(tile_width * pos_x + 5, tile_height * pos_y)
        self.pos = pos_x, pos_y


class Emerald(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(emeralds_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
object_group = pygame.sprite.Group()
emeralds_group = pygame.sprite.Group()

tile_images = {'wall_1': load_image('world/wall_1.png'),
               'wall_2': load_image('world/wall_2.png'),
               'g': load_image('world/асфальт - зеленый.bmp'),
               'f': load_image('world/верхняя  т - фиолетовый.png'),
               'b': load_image('world/впп - черный.png'),
               'or': load_image('world/впп верт - оранжевый.png'),
               'y': load_image('world/нижняя т - желтые.png'),
               'blue': load_image('world/перекресток синий.png'),
               'lg': load_image('world/разметка верт - светло-серый.png'),
               'gr': load_image('world/серый.png'),
               }

player_image_lr = load_image('pers/stand_1.png')
standing_player = {'stand_1': load_image('pers/stand_1.png'),
                   'stand_2': load_image('pers/stand_2.png'),
                   'stand_3': load_image('pers/stand_3.png'),
                   'stand_4': load_image('pers/stand_4.png'),
                   'stand_5': load_image('pers/stand_5.png'),
                   'stand_6': load_image('pers/stand_6.png')}

running_player = {'run_1': load_image('pers/run_1.png'),
                  'run_2': load_image('pers/run_2.png'),
                  'run_3': load_image('pers/run_3.png'),
                  'run_4': load_image('pers/run_4.png'),
                  'run_5': load_image('pers/run_5.png'),
                  'run_6': load_image('pers/run_6.png'),
                  'run_7': load_image('pers/run_7.png'),
                  'run_8': load_image('pers/run_8.png'),
                  'run_9': load_image('pers/run_9.png')}

tile_width = tile_height = STEP = 50

if __name__ == '__main__':

    def upd_camera():
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)


    def draw():
        screen.fill(pygame.Color(0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        object_group.draw(screen)
        emeralds_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS * 4)


    def change_running_pose(lr):
        global running_flag, running_list
        running_flag %= 8
        if lr == 1:
            player.image = pygame.transform.flip(running_player[running_list[running_flag]], True, False)
        else:
            player.image = pygame.transform.flip(running_player[running_list[running_flag]], False, False)
        running_flag += 1


    lev = Map_generation()
    #   lev.rendering()  # Сохраняем изображение карты
    lev.write_in_txt()  # Сохраняем список в текстовый файл
    level = lev.map_level()  # Считываем карту
    start_screen()
    camera = Camera()
    running = True
    player, enemies, level_x, level_y = generate_level(level)
    standing_flag, running_flag, lr = 0, 0, 2
    standing_list = ['stand_1', 'stand_2', 'stand_3', 'stand_4', 'stand_5', 'stand_6']
    running_list = ['run_1', 'run_2', 'run_3', 'run_4', 'run_5', 'run_6', 'run_7', 'run_8', 'run_9']
    y, x = player.pos[1], player.pos[0]
    upd_camera()
    while running:

        keys = pygame.key.get_pressed()
        allowed_cells = ['.', 'e', '@', 'f1']

        if keys[pygame.K_ESCAPE]:
            terminate()

        '''ДВИЖЕНИЕ ИГРОКА'''

        if keys[pygame.K_d] and keys[pygame.K_w]:
            if level[y][x + 1][1] not in allowed_cells and level[y - 1][x][1] in allowed_cells:
                y -= 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.y -= step
                    change_running_pose(2)
                    lr = 2
                    upd_camera()
                    draw()

            elif level[y - 1][x][1] not in allowed_cells and level[y][x + 1][1] in allowed_cells:
                x += 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.x += step
                    change_running_pose(2)
                    lr = 2
                    upd_camera()
                    draw()

            elif level[y - 1][x + 1][1] in allowed_cells:
                x += 1
                y -= 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.x += step
                    player.rect.y -= step
                    change_running_pose(2)
                    lr = 2
                    upd_camera()
                    draw()

        elif keys[pygame.K_d] and keys[pygame.K_s]:
            if level[y][x + 1][1] not in allowed_cells and level[y + 1][x][1] in allowed_cells:
                y += 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.y += step
                    change_running_pose(2)
                    lr = 2
                    upd_camera()
                    draw()

            elif level[y + 1][x][1] not in allowed_cells and level[y][x + 1][1] in allowed_cells:
                x += 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.x += step
                    change_running_pose(2)
                    lr = 2
                    upd_camera()
                    draw()

            elif level[y + 1][x + 1][1] in allowed_cells:
                x += 1
                y += 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.x += step
                    player.rect.y += step
                    change_running_pose(2)
                    lr = 2
                    upd_camera()
                    draw()

        elif keys[pygame.K_a] and keys[pygame.K_s]:
            if level[y + 1][x][1] not in allowed_cells and level[y][x - 1][1] in allowed_cells:
                x -= 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.x -= step
                    change_running_pose(1)
                    lr = 1
                    upd_camera()
                    draw()

            elif level[y][x - 1][1] not in allowed_cells and level[y + 1][x][1] in allowed_cells:
                y += 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.y += step
                    change_running_pose(1)
                    lr = 1
                    upd_camera()
                    draw()

            elif level[y + 1][x - 1][1] in allowed_cells:
                x -= 1
                y += 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.x -= step
                    player.rect.y += step
                    change_running_pose(1)
                    lr = 1
                    upd_camera()
                    draw()

        elif keys[pygame.K_a] and keys[pygame.K_w]:
            if level[y - 1][x][1] not in allowed_cells and level[y][x - 1][1] in allowed_cells:
                x -= 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.x -= step
                    change_running_pose(1)
                    lr = 1
                    upd_camera()
                    draw()

            elif level[y][x - 1][1] not in allowed_cells and level[y - 1][x][1] in allowed_cells:
                y -= 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.y -= step
                    change_running_pose(1)
                    lr = 1
                    upd_camera()
                    draw()

            elif level[y - 1][x - 1][1] in allowed_cells:
                x -= 1
                y -= 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.x -= step
                    player.rect.y -= step
                    change_running_pose(1)
                    lr = 1
                    upd_camera()
                    draw()

        elif keys[pygame.K_d]:
            if level[y][x + 1][1] in allowed_cells:
                x += 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.x += step
                    change_running_pose(2)
                    lr = 2
                    upd_camera()
                    draw()

        elif keys[pygame.K_a]:
            if level[y][x - 1][1] in allowed_cells:
                x -= 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.x -= step
                    change_running_pose(1)
                    lr = 1
                    upd_camera()
                    draw()

        elif keys[pygame.K_w]:
            if level[y - 1][x][1] in allowed_cells:
                y -= 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.y -= step
                    if lr == 2:
                        change_running_pose(2)
                    else:
                        change_running_pose(1)
                    upd_camera()
                    draw()

        elif keys[pygame.K_s]:
            if level[y + 1][x][1] in allowed_cells:
                y += 1
                for step in [5, 5, 6, 6, 6, 6, 6, 5, 5]:
                    player.rect.y += step
                    if lr == 2:
                        change_running_pose(2)
                    else:
                        change_running_pose(1)
                    upd_camera()
                    draw()

        elif keys[pygame.K_s] == False and keys[pygame.K_w] == False \
                and keys[pygame.K_a] == False and keys[pygame.K_d] == False:
            standing_flag %= 5
            if lr == 2:
                player.image = pygame.transform.flip(standing_player[standing_list[standing_flag]], False, False)
            else:
                player.image = pygame.transform.flip(standing_player[standing_list[standing_flag]], True, False)
            standing_flag += 1
            clock.tick(FPS // 8)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            upd_camera()
        draw()
    terminate()
