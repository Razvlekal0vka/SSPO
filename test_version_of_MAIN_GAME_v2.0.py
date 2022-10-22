import os
import sys
import pygame

pygame.init()
size = WIDTH, HEIGHT = 1000, 640
screen = pygame.display.set_mode(size)
FPS = 50
clock = pygame.time.Clock()

import random
from enum import Enum
from PIL import Image


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
        wall_index = random.randint(start + 1, start + length - 2)
        if wall_index % 2 == 1:
            wall_index -= 1
        return wall_index

    def generateHoles(map, x, y, width, height, wall_x, wall_y):
        holes = []

        hole_entrys = [(random.randint(x, wall_x - 1), wall_y), (random.randint(wall_x + 1, x + width - 1), wall_y),
                       (wall_x, random.randint(y, wall_y - 1)), (wall_x, random.randint(wall_y + 1, y + height - 1))]
        margin_entrys = [(x, wall_y), (x + width - 1, wall_y), (wall_x, y), (wall_x, y + height - 1)]
        adjacent_entrys = [(x - 1, wall_y), (x + width, wall_y), (wall_x, y - 1), (wall_x, y + height)]
        for i in range(4):
            adj_x, adj_y = (adjacent_entrys[i][0], adjacent_entrys[i][1])
            if map.isValid(adj_x, adj_y) and map.isMovable(adj_x, adj_y):
                map.setMap(margin_entrys[i][0], margin_entrys[i][1], MAP_ENTRY_TYPE.MAP_EMPTY)
            else:
                holes.append(hole_entrys[i])

        ignore_hole = random.randint(0, len(holes) - 1)
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


class Map_generation:
    """Здесь происходит генирация карты"""

    def __init__(self):
        print('Инициализация')
        self.number_of_buildings = 21
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
        print('Заполнение города пустотой')
        for y in range(self.size_of_the_city):
            line = []
            for x in range(self.size_of_the_city):
                line.append(['.'])
            self.map_city.append(line)

        self.filling()

    def filling(self):
        print('Генерация границ карты')
        for x in range(self.size_of_the_city):
            self.map_city[0][x], self.map_city[self.size_of_the_city - 1][x] = ['b'], ['b']
        for y in range(self.size_of_the_city):
            self.map_city[y][0], self.map_city[y][self.size_of_the_city - 1] = ['b'], ['b']

        print('Создание ген. плана застройки и его согласование')
        facades = []
        start_house = 0
        colors = ['brown', 'purple', 'green', 'yellow']
        for _ in range(21):
            street = []
            for __ in range(21):
                color = random.randint(0, 12)
                if 0 <= color <= 3:
                    color = 3
                elif 4 <= color <= 7:
                    color = 2
                elif 8 <= color <= 11:
                    color = 1
                elif color == 12:
                    color = 0
                street.append(colors[color])
            facades.append(street)
            street = []

        x = random.randint(5, 15)
        y = random.randint(5, 15)
        facades[y][x] = 'grey'

        print('Возведение улиц')
        x, y = 6, 1  # горизонтальные
        for _ in range(22):
            for __ in range(21):
                for yy in range(5):
                    for xx in range(50):
                        if yy == 0:
                            self.map_city[y + yy][x + xx] = ['border12', '.']
                        elif yy == 4:
                            self.map_city[y + yy][x + xx] = ['border6', '.']
                        elif (0 < yy < 4 and 0 <= xx <= 2) or (0 < yy < 4 and 47 <= xx <= 49):
                            self.map_city[y + yy][x + xx] = ['transition_g', '.']
                        else:
                            self.map_city[y + yy][x + xx] = ['road_g', '.']
                x += 55
            y += 55
            x = 6

        x, y = 6, 1  # вертикальные
        for _ in range(22):
            for __ in range(21):
                for yy in range(5):
                    for xx in range(50):
                        if yy == 0:
                            self.map_city[x + xx][y + yy] = ['border9', '.']
                        elif yy == 4:
                            self.map_city[x + xx][y + yy] = ['border3', '.']
                        elif (0 < yy < 4 and 0 <= xx <= 2) or (0 < yy < 4 and 47 <= xx <= 49):
                            self.map_city[x + xx][y + yy] = ['transition_v', '.']
                        else:
                            self.map_city[x + xx][y + yy] = ['road_v', '.']
                x += 55
            y += 55
            x = 6

        print('Создание перекрёстков')
        x, y = 1, 1
        for _ in range(22):
            for __ in range(22):
                for yy in range(5):
                    for xx in range(5):
                        if yy == 0 and xx == 0:
                            self.map_city[y + yy][x + xx] = ['c1011', '.']
                        elif yy == 0 and xx == 4:
                            self.map_city[y + yy][x + xx] = ['c12', '.']
                        elif yy == 4 and xx == 4:
                            self.map_city[y + yy][x + xx] = ['c45', '.']
                        elif yy == 4 and xx == 0:
                            self.map_city[y + yy][x + xx] = ['c78', '.']
                        else:
                            self.map_city[y + yy][x + xx] = ['c', '.']
                x += 55
            y += 55
            x = 1

        print('Строительство зданий')
        x, y = 6, 6
        for _ in range(21):
            for __ in range(21):
                for yy in range(50):
                    for xx in range(50):
                        if facades[_][__] == 'purple':
                            if yy == 0 or xx == 0 or yy == 49 or xx == 49:
                                self.map_city[y + yy][x + xx] = ['purple_house', '#']
                            else:
                                self.map_city[y + yy][x + xx] = ['purple_house_floor', '.']
                        elif facades[_][__] == 'green':
                            if yy == 0 or xx == 0 or yy == 49 or xx == 49:
                                self.map_city[y + yy][x + xx] = ['green_house', '#']
                            else:
                                self.map_city[y + yy][x + xx] = ['green_house_floor', '.']
                        elif facades[_][__] == 'yellow':
                            if yy == 0 or xx == 0 or yy == 49 or xx == 49:
                                self.map_city[y + yy][x + xx] = ['yellow_house', '#']
                            else:
                                self.map_city[y + yy][x + xx] = ['yellow_house_floor', '.']
                        elif facades[_][__] == 'grey':
                            if yy == 0 and (xx < 24 or xx > 27):
                                self.map_city[y + yy][x + xx] = ['sh', '#']
                            elif yy == 49 and (xx < 24 or xx > 27):
                                self.map_city[y + yy][x + xx] = ['sh', '#']
                            elif xx == 0 and (yy < 24 or yy > 27):
                                self.map_city[y + yy][x + xx] = ['sh', '#']
                            elif xx == 49 and (yy < 24 or yy > 27):
                                self.map_city[y + yy][x + xx] = ['sh', '#']
                            elif (yy == 0 and (24 <= xx <= 27)) or (yy == 49 and (24 <= xx <= 27)) or (
                                    xx == 0 and (24 <= yy <= 27)) or (xx == 49 and (24 <= yy <= 27)):
                                self.map_city[y + yy][x + xx] = ['start_passage', '.']
                            else:
                                self.map_city[y + yy][x + xx] = ['start_floor', '.']
                x += 55
            y += 55
            x = 6

        print('Строительство зданий c лабиринтом')
        x, y = 6, 6
        for _ in range(21):
            for __ in range(21):
                map_m = Map()
                doRecursiveDivision(map_m)
                maze = map_m.showMap()
                for yy in range(50):
                    for xx in range(50):
                        if facades[_][__] == 'brown':
                            if yy <= 1 and xx <= 1:
                                self.map_city[y + yy][x + xx] = ['brown_house', '#']
                            else:
                                if xx <= 49 and yy <= 49:
                                    if maze[yy // 2][xx // 2] == '#':
                                        self.map_city[y + yy][x + xx] = ['brown_house', '#']
                                    else:
                                        self.map_city[y + yy][x + xx] = ['brown_house_floor', '.']
                if facades[_][__] != 'grey':
                    if facades[_][__] == 'brown':
                        np = random.randint(1, 4)
                        rp = random.randint(2, 43)
                        if np == 1:
                            for i in range(4):
                                self.map_city[y + rp][x + 46 + i] = ['passage', '.']
                                self.map_city[y + rp + 1][x + 46 + i] = ['passage', '.']
                                self.map_city[y + rp + 2][x + 46 + i] = ['passage', '.']
                                self.map_city[y + rp + 3][x + 46 + i] = ['passage', '.']
                        elif np == 2:
                            for i in range(4):
                                self.map_city[y + 46 + i][x + rp] = ['passage', '.']
                                self.map_city[y + 46 + i][x + rp + 1] = ['passage', '.']
                                self.map_city[y + 46 + i][x + rp + 2] = ['passage', '.']
                                self.map_city[y + 46 + i][x + rp + 3] = ['passage', '.']
                        elif np == 3:
                            for i in range(4):
                                self.map_city[y + rp][x + 0 + i] = ['passage', '.']
                                self.map_city[y + rp + 1][x + 0 + i] = ['passage', '.']
                                self.map_city[y + rp + 2][x + 0 + i] = ['passage', '.']
                                self.map_city[y + rp + 3][x + 0 + i] = ['passage', '.']
                        elif np == 4:
                            for i in range(4):
                                self.map_city[y + 0 + i][x + rp] = ['passage', '.']
                                self.map_city[y + 0 + i][x + rp + 1] = ['passage', '.']
                                self.map_city[y + 0 + i][x + rp + 2] = ['passage', '.']
                                self.map_city[y + 0 + i][x + rp + 3] = ['passage', '.']
                    else:
                        np = random.randint(1, 4)
                        rp = random.randint(2, 43)
                        if np == 1:
                            self.map_city[y + rp][x + 49] = ['passage', '.']
                            self.map_city[y + rp + 1][x + 49] = ['passage', '.']
                            self.map_city[y + rp + 2][x + 49] = ['passage', '.']
                            self.map_city[y + rp + 3][x + 49] = ['passage', '.']
                        elif np == 2:
                            self.map_city[y + 49][x + rp] = ['passage', '.']
                            self.map_city[y + 49][x + rp + 1] = ['passage', '.']
                            self.map_city[y + 49][x + rp + 2] = ['passage', '.']
                            self.map_city[y + 49][x + rp + 3] = ['passage', '.']
                        elif np == 3:
                            self.map_city[y + rp][x + 0] = ['passage', '.']
                            self.map_city[y + rp + 1][x + 0] = ['passage', '.']
                            self.map_city[y + rp + 2][x + 0] = ['passage', '.']
                            self.map_city[y + rp + 3][x + 0] = ['passage', '.']
                        elif np == 4:
                            self.map_city[y + 0][x + rp] = ['passage', '.']
                            self.map_city[y + 0][x + rp + 1] = ['passage', '.']
                            self.map_city[y + 0][x + rp + 2] = ['passage', '.']
                            self.map_city[y + 0][x + rp + 3] = ['passage', '.']
                x += 55
            x = 6
            y += 55

    def rendering(self):
        print('Создание изображения карты')
        image = Image.new("RGB", (self.size_of_the_city, self.size_of_the_city), (0, 0, 0))
        for y in range(self.size_of_the_city):
            for x in range(self.size_of_the_city):
                coords = (x, y)
                if self.map_city[y][x][0] == 'b':
                    r, g, b = 190, 65, 0
                elif self.map_city[y][x][0] == 'c':
                    r, g, b = 63, 89, 141
                elif self.map_city[y][x][0] == 'c12':
                    r, g, b = 63, 89, 191
                elif self.map_city[y][x][0] == 'c45':
                    r, g, b = 63, 89, 191
                elif self.map_city[y][x][0] == 'c78':
                    r, g, b = 63, 89, 191
                elif self.map_city[y][x][0] == 'c1011':
                    r, g, b = 63, 89, 191
                elif self.map_city[y][x][0] == 'road_v':
                    r, g, b = 43, 88, 101
                elif self.map_city[y][x][0] == 'road_g':
                    r, g, b = 43, 88, 101
                elif self.map_city[y][x][0] == 'border12':
                    r, g, b = 93, 108, 141
                elif self.map_city[y][x][0] == 'border6':
                    r, g, b = 93, 108, 141
                elif self.map_city[y][x][0] == 'border9':
                    r, g, b = 93, 108, 141
                elif self.map_city[y][x][0] == 'border3':
                    r, g, b = 93, 108, 141
                elif self.map_city[y][x][0] == 'transition_g':
                    r, g, b = 63, 138, 141
                elif self.map_city[y][x][0] == 'transition_v':
                    r, g, b = 63, 138, 141
                elif self.map_city[y][x][0] == 'yellow_house':
                    r, g, b = 141, 76, 63
                elif self.map_city[y][x][0] == 'yellow_house_floor':
                    r, g, b = 201, 136, 123
                elif self.map_city[y][x][0] == 'green_house':
                    r, g, b = 115, 141, 63
                elif self.map_city[y][x][0] == 'green_house_floor':
                    r, g, b = 175, 201, 123
                elif self.map_city[y][x][0] == 'purple_house':
                    r, g, b = 138, 81, 117
                elif self.map_city[y][x][0] == 'purple_house_floor':
                    r, g, b = 198, 141, 177
                elif self.map_city[y][x][0] == 'brown_house':
                    r, g, b = 141, 99, 63
                elif self.map_city[y][x][0] == 'brown_house_floor':
                    r, g, b = 201, 159, 123
                elif self.map_city[y][x][0] == 'sh':
                    r, g, b = 79, 79, 79
                elif self.map_city[y][x][0] == 'passage':
                    r, g, b = 120, 120, 120
                elif self.map_city[y][x][0] == 'start_floor':
                    r, g, b = 200, 200, 200
                else:
                    r, g, b = 0, 0, 0
                image.putpixel(coords, (r, g, b))
        image.save('test_data/' + 'map.png')

    def write_in_txt(self):
        print('Сохранение карты')
        with open('test_data/Test_map.txt', 'w') as writing_file:
            for element in self.map_city:
                print(*element, file=writing_file)

    def map_level(self):
        return self.map_city


level = Map_generation()
level.rendering()  # Сохраняем изображение карты
level.write_in_txt()  # Сохраняем список в текстовый файл
map_lev = level.map_level()  # Считываем список


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    # intro_text = []
    fon = pygame.transform.scale(load_image('boot.png'), (WIDTH, HEIGHT))
    name_of_the_game = pygame.transform.scale(load_image('RBWOF.png'), (WIDTH, HEIGHT))
    start_text = pygame.transform.scale(load_image('CIYWETG2.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    screen.blit(name_of_the_game, (0, 0))
    screen.blit(start_text, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    '''for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)'''

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def load_image(name, color_key=None):
    fullname = os.path.join('test_data', name)
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


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = pos_x, pos_y


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
tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('mario.png')
tile_width = tile_height = STEP = 50

if __name__ == '__main__':
    start_screen()
    camera = Camera()
    running = True
    level = load_level('level1.txt')
    player, level_x, level_y = generate_level(level)
    y, x = player.pos[0] - 1, player.pos[1] + 1
    while running:

        keys = pygame.key.get_pressed()
        print(y, x)

        if keys[pygame.K_d]:
            if x < level_x - 1 and level[y][x + 1] == '.':
                x += 1
                player.rect.x += STEP
        elif keys[pygame.K_a]:
            if x > 0 and level[y][x - 1] == '.':
                x -= 1
                player.rect.x -= STEP
        clock.tick(FPS // 3)

        if keys[pygame.K_w]:
            if y > 0 and level[y - 1][x] == '.':
                y -= 1
                player.rect.y -= STEP
        elif keys[pygame.K_s]:
            if y < level_y - 1 and level[y + 1][x] == '.':
                y += 1
                player.rect.y += STEP
        clock.tick(FPS // 3)

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
        pygame.display.flip()
        clock.tick(FPS)

    terminate()
