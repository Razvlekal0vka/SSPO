import os
import random
import sys
from enum import Enum
from random import randint
from tkinter import Image

import pygame
from PIL import Image

pygame.init()
size = WIDTH, HEIGHT = 1000, 640
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
    """Здесь происходит генирация карты"""

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
            n = random.randint(1, 2)
            if n == 1:
                self.map_city[0][x] = ['wall_1', '#']
            elif n == 2:
                self.map_city[0][x] = ['wall_2', '#']

            n = random.randint(1, 2)
            if n == 1:
                self.map_city[self.size_of_the_city - 1][x] = ['wall_1', '#']
            elif n == 2:
                self.map_city[self.size_of_the_city - 1][x] = ['wall_2', '#']

        for y in range(self.size_of_the_city):
            n = random.randint(1, 2)
            if n == 1:
                self.map_city[y][0] = ['wall_1', '#']
            elif n == 2:
                self.map_city[y][0] = ['wall_2', '#']

            n = random.randint(1, 2)
            if n == 1:
                self.map_city[y][self.size_of_the_city - 1] = ['wall_1', '#']
            if n == 2:
                self.map_city[y][self.size_of_the_city - 1] = ['wall_2', '#']

        print('Создание ген. плана застройки и его согласование')
        facades = []
        start_house = 0
        colors = ['brown_maze', 'purple_maze', 'green', 'yellow']
        for _ in range(self.number_of_buildings):
            street = []
            for __ in range(self.number_of_buildings):
                color = random.randint(0, 15)
                if 0 <= color <= 3:
                    color = 3
                elif 4 <= color <= 7:
                    color = 2
                elif 8 <= color <= 11:
                    color = 1
                elif color >= 12:
                    color = 0
                street.append(colors[color])
            facades.append(street)
            street = []

        x = random.randint(self.number_of_buildings // 2 - 1, self.number_of_buildings // 2 + 1)
        y = random.randint(self.number_of_buildings // 2 - 1, self.number_of_buildings // 2 + 1)
        facades[y][x] = 'grey'

        print('Возведение улиц')
        x, y = 6, 1  # горизонтальные
        for _ in range(self.number_of_streets):
            for __ in range(self.number_of_buildings):
                for yy in range(5):
                    for xx in range(50):
                        if yy == 0:
                            self.summer_floor_genesis(x, xx, y, yy, 1)
                        elif yy == 4:
                            self.summer_floor_genesis(x, xx, y, yy, 1)
                        elif (0 < yy < 4 and 0 <= xx <= 2) or (0 < yy < 4 and 47 <= xx <= 49):
                            self.summer_floor_genesis(x, xx, y, yy, 1)
                        else:
                            self.summer_floor_genesis(x, xx, y, yy, 1)
                x += 55
            y += 55
            x = 6

        x, y = 6, 1  # вертикальные
        for _ in range(self.number_of_streets):
            for __ in range(self.number_of_buildings):
                for yy in range(5):
                    for xx in range(50):
                        if yy == 0:
                            self.summer_floor_genesis(y, yy, x, xx, 1)
                        elif yy == 4:
                            self.summer_floor_genesis(y, yy, x, xx, 1)
                        elif (0 < yy < 4 and 0 <= xx <= 2) or (0 < yy < 4 and 47 <= xx <= 49):
                            self.summer_floor_genesis(y, yy, x, xx, 1)
                        else:
                            self.summer_floor_genesis(y, yy, x, xx, 1)
                x += 55
            y += 55
            x = 6

        print('Создание перекрёстков')
        x, y = 1, 1
        for _ in range(self.number_of_streets):
            for __ in range(self.number_of_streets):
                for yy in range(5):
                    for xx in range(5):
                        if yy == 0 and xx == 0:
                            self.summer_floor_genesis(x, xx, y, yy, 1)
                        elif yy == 0 and xx == 4:
                            self.summer_floor_genesis(x, xx, y, yy, 1)
                        elif yy == 4 and xx == 4:
                            self.summer_floor_genesis(x, xx, y, yy, 1)
                        elif yy == 4 and xx == 0:
                            self.summer_floor_genesis(x, xx, y, yy, 1)
                        else:
                            self.summer_floor_genesis(x, xx, y, yy, 1)
                x += 55
            y += 55
            x = 1

        print('Строительство зданий')
        x, y = 6, 6
        for _ in range(self.number_of_buildings):
            for __ in range(self.number_of_buildings):
                for yy in range(50):
                    for xx in range(50):
                        if facades[_][__] == 'green':
                            if yy == 7 or xx == 7 or yy == 42 or xx == 42:
                                n = random.randint(1, 8)
                                if n == 8:
                                    n = random.randint(1, 2)
                                    if n == 1:
                                        self.map_city[y + yy][x + xx] = ['wall_1', '#']
                                    elif n == 2:
                                        self.map_city[y + yy][x + xx] = ['wall_2', '#']
                                else:
                                    self.summer_floor_genesis(x, xx, y, yy, 0)
                            elif 23 <= yy <= 25 and 23 <= xx <= 25:
                                n = random.randint(1, 8)
                                if n == 1 or n == 2:
                                    self.map_city[y + yy][x + xx] = ['floor_1', '#']
                                elif n == 3 or n == 4:
                                    self.map_city[y + yy][x + xx] = ['floor_2', '#']
                                elif n == 5 or n == 6:
                                    self.map_city[y + yy][x + xx] = ['floor_3', '#']
                                elif n == 7 or n == 8:
                                    self.map_city[y + yy][x + xx] = ['floor_4', '#']
                            elif yy == 22 and xx == 23 :
                                n = random.randint(1, 8)
                                if n == 1 or n == 2:
                                    self.map_city[y + yy][x + xx] = ['floor_1', 'f1']
                                elif n == 3 or n == 4:
                                    self.map_city[y + yy][x + xx] = ['floor_2', 'f1']
                                elif n == 5 or n == 6:
                                    self.map_city[y + yy][x + xx] = ['floor_3', 'f1']
                                elif n == 7 or n == 8:
                                    self.map_city[y + yy][x + xx] = ['floor_4', 'f1']
                            else:
                                n = random.randint(1, 5)
                                if n == 1:
                                    self.summer_floor_genesis_2(x, xx, y, yy)
                                else:
                                    self.summer_floor_genesis(x, xx, y, yy, 0)
                        elif facades[_][__] == 'yellow':
                            if yy == 0 or xx == 0 or yy == 49 or xx == 49:
                                self.map_city[y + yy][x + xx] = ['yellow_house', '#']
                            else:
                                self.map_city[y + yy][x + xx] = ['yellow_house_floor', '.']
                        elif facades[_][__] == 'grey':
                            if yy == 0 and (xx < 24 or xx > 27):
                                self.map_city[y + yy][x + xx] = ['sh', '#']
                            elif (xx == 4 and yy == 4) or (xx == 4 and yy == 44) or (xx == 44 and yy == 4) or (xx == 44 and yy == 44):
                                self.map_city[y + yy][x + xx] = ['start_floor', 'e']
                            elif yy == 25 and xx == 25:
                                self.map_city[y + yy][x + xx] = ['start_floor', '@']
                            elif yy == 49 and (xx < 24 or xx > 27):
                                self.map_city[y + yy][x + xx] = ['sh', '#']
                            elif xx == 0 and (yy < 24 or yy > 27):
                                self.map_city[y + yy][x + xx] = ['sh', '#']
                            elif xx == 49 and (yy < 24 or yy > 27):
                                self.map_city[y + yy][x + xx] = ['sh', '#']
                            elif (yy == 0 and (24 <= xx <= 27)) or (yy == 49 and (24 <= xx <= 27)) or (
                                    xx == 0 and (24 <= yy <= 27)) or (xx == 49 and (24 <= yy <= 27)):
                                self.map_city[y + yy][x + xx] = ['passage', '.']
                            else:
                                self.map_city[y + yy][x + xx] = ['start_floor', '.']
                x += 55
            y += 55
            x = 6

        print('Строительство зданий c лабиринтом')
        x, y = 6, 6
        for _ in range(self.number_of_buildings):
            for __ in range(self.number_of_buildings):
                try:
                    map_m = Map()
                    doRecursiveDivision(map_m)
                    maze = map_m.showMap()
                except Exception:
                    print('<ERROR>')
                    Error_of_creating_maze()
                for yy in range(50):
                    for xx in range(50):
                        if facades[_][__] == 'brown_maze':
                            if True:
                                if yy == 0 or xx == 0 or yy == 49 or xx == 49:
                                    n = random.randint(1, 2)
                                    if n == 1:
                                        self.map_city[y + yy][x + xx] = ['wall_1', '#']
                                    elif n == 2:
                                        self.map_city[y + yy][x + xx] = ['wall_2', '#']
                                else:
                                    if xx <= 49 and yy <= 49:
                                        if maze[yy // 2][xx // 2] == '#':
                                            self.map_city[y + yy][x + xx] = ['maze_house', '#']
                                        else:
                                            n = random.randint(1, 4)
                                            if n == 1:
                                                self.map_city[y + yy][x + xx] = ['maze_floor_1', '.']
                                            elif n == 2:
                                                self.map_city[y + yy][x + xx] = ['maze_floor_2', '.']
                                            elif n == 3:
                                                self.map_city[y + yy][x + xx] = ['maze_floor_3', '.']
                                            elif n == 4:
                                                self.map_city[y + yy][x + xx] = ['maze_floor_4', '.']
                        if facades[_][__] == 'purple_maze':
                            if True:
                                if yy == 0 or xx == 0 or yy == 49 or xx == 49:
                                    n = random.randint(1, 2)
                                    if n == 1:
                                        self.map_city[y + yy][x + xx] = ['wall_1', '#']
                                    elif n == 2:
                                        self.map_city[y + yy][x + xx] = ['wall_2', '#']
                                else:
                                    if xx <= 49 and yy <= 49:
                                        if maze[yy // 2][xx // 2] == '#':
                                            ___ = random.randint(1, 2)
                                            if ___ == 1:
                                                self.map_city[y + yy][x + xx] = ['dark_maze_house_1', '#']
                                            elif ___ == 2:
                                                self.map_city[y + yy][x + xx] = ['dark_maze_house_2', '#']
                                        else:
                                            n = random.randint(1, 4)
                                            if n == 1:
                                                self.map_city[y + yy][x + xx] = ['dark_maze_floor_1', '.']
                                            elif n == 2:
                                                self.map_city[y + yy][x + xx] = ['dark_maze_floor_2', '.']
                                            elif n == 3:
                                                self.map_city[y + yy][x + xx] = ['dark_maze_floor_3', '.']
                                            elif n == 4:
                                                self.map_city[y + yy][x + xx] = ['dark_maze_floor_4', '.']
                if facades[_][__] != 'grey' and facades[_][__] != 'green':
                    if facades[_][__] == 'brown_maze' or facades[_][__] == 'purple_maze':
                        np = random.randint(1, 4)
                        rp = random.randint(2, 43)
                        if np == 1:
                            for i in range(4):
                                for j in range(4):
                                    if facades[_][__] == 'brown_maze':
                                        n = random.randint(1, 4)
                                        if n == 1:
                                            self.map_city[y + rp + j][x + 46 + i] = ['maze_floor_1', '.']
                                        elif n == 2:
                                            self.map_city[y + rp + j][x + 46 + i] = ['maze_floor_2', '.']
                                        elif n == 3:
                                            self.map_city[y + rp + j][x + 46 + i] = ['maze_floor_3', '.']
                                        elif n == 4:
                                            self.map_city[y + rp + j][x + 46 + i] = ['maze_floor_4', '.']
                                    elif facades[_][__] == 'purple_maze':
                                        n = random.randint(1, 4)
                                        if n == 1:
                                            self.map_city[y + rp + j][x + 46 + i] = ['dark_maze_floor_1', '.']
                                        elif n == 2:
                                            self.map_city[y + rp + j][x + 46 + i] = ['dark_maze_floor_2', '.']
                                        elif n == 3:
                                            self.map_city[y + rp + j][x + 46 + i] = ['dark_maze_floor_3', '.']
                                        elif n == 4:
                                            self.map_city[y + rp + j][x + 46 + i] = ['dark_maze_floor_4', '.']
                        elif np == 2:
                            for i in range(4):
                                for j in range(4):
                                    if facades[_][__] == 'brown_maze':
                                        n = random.randint(1, 4)
                                        if n == 1:
                                            self.map_city[y + 46 + j][x + rp + i] = ['maze_floor_1', '.']
                                        elif n == 2:
                                            self.map_city[y + 46 + j][x + rp + i] = ['maze_floor_2', '.']
                                        elif n == 3:
                                            self.map_city[y + 46 + j][x + rp + i] = ['maze_floor_3', '.']
                                        elif n == 4:
                                            self.map_city[y + 46 + j][x + rp + i] = ['maze_floor_4', '.']
                                    elif facades[_][__] == 'purple_maze':
                                        n = random.randint(1, 4)
                                        if n == 1:
                                            self.map_city[y + 46 + j][x + rp + i] = ['dark_maze_floor_1', '.']
                                        elif n == 2:
                                            self.map_city[y + 46 + j][x + rp + i] = ['dark_maze_floor_2', '.']
                                        elif n == 3:
                                            self.map_city[y + 46 + j][x + rp + i] = ['dark_maze_floor_3', '.']
                                        elif n == 4:
                                            self.map_city[y + 46 + j][x + rp + i] = ['dark_maze_floor_4', '.']
                        elif np == 3:
                            for i in range(4):
                                for j in range(4):
                                    if facades[_][__] == 'brown_maze':
                                        n = random.randint(1, 4)
                                        if n == 1:
                                            self.map_city[y + rp + j][x + 0 + i] = ['maze_floor_1', '.']
                                        elif n == 2:
                                            self.map_city[y + rp + j][x + 0 + i] = ['maze_floor_2', '.']
                                        elif n == 3:
                                            self.map_city[y + rp + j][x + 0 + i] = ['maze_floor_3', '.']
                                        elif n == 4:
                                            self.map_city[y + rp + j][x + 0 + i] = ['maze_floor_4', '.']
                                    elif facades[_][__] == 'purple_maze':
                                        n = random.randint(1, 4)
                                        if n == 1:
                                            self.map_city[y + rp + j][x + 0 + i] = ['dark_maze_floor_1', '.']
                                        elif n == 2:
                                            self.map_city[y + rp + j][x + 0 + i] = ['dark_maze_floor_2', '.']
                                        elif n == 3:
                                            self.map_city[y + rp + j][x + 0 + i] = ['dark_maze_floor_3', '.']
                                        elif n == 4:
                                            self.map_city[y + rp + j][x + 0 + i] = ['dark_maze_floor_4', '.']
                        elif np == 4:
                            for i in range(4):
                                for j in range(4):
                                    if facades[_][__] == 'brown_maze':
                                        n = random.randint(1, 4)
                                        if n == 1:
                                            self.map_city[y + 0 + j][x + rp + i] = ['maze_floor_1', '.']
                                        elif n == 2:
                                            self.map_city[y + 0 + j][x + rp + i] = ['maze_floor_2', '.']
                                        elif n == 3:
                                            self.map_city[y + 0 + j][x + rp + i] = ['maze_floor_3', '.']
                                        elif n == 4:
                                            self.map_city[y + 0 + j][x + rp + i] = ['maze_floor_4', '.']
                                    elif facades[_][__] == 'purple_maze':
                                        n = random.randint(1, 4)
                                        if n == 1:
                                            self.map_city[y + 0 + j][x + rp + i] = ['dark_maze_floor_1', '.']
                                        elif n == 2:
                                            self.map_city[y + 0 + j][x + rp + i] = ['dark_maze_floor_2', '.']
                                        elif n == 3:
                                            self.map_city[y + 0 + j][x + rp + i] = ['dark_maze_floor_3', '.']
                                        elif n == 4:
                                            self.map_city[y + 0 + j][x + rp + i] = ['dark_maze_floor_4', '.']
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
                if self.map_city[y][x][0] == 'wall_1':
                    r, g, b = 0, 55, 190
                elif self.map_city[y][x][0] == 'wall_2':
                    r, g, b = 0, 75, 190
                elif self.map_city[y][x][0] == 'floor_1':
                    if self.map_city[y][x][1] == 'd':
                        r, g, b = 46, 130, 40
                    elif self.map_city[y][x][1] == 'f1':
                        r, g, b = 46, 170, 240
                    elif self.map_city[y][x][1] == '#':
                        r, g, b = 46, 240, 240
                    else:
                        r, g, b = 96, 130, 90
                elif self.map_city[y][x][0] == 'floor_2':
                    if self.map_city[y][x][1] == 'd':
                        r, g, b = 46, 130, 40
                    elif self.map_city[y][x][1] == 'f1':
                        r, g, b = 46, 170, 240
                    elif self.map_city[y][x][1] == '#':
                        r, g, b = 46, 240, 240
                    else:
                        r, g, b = 96, 130, 90
                elif self.map_city[y][x][0] == 'floor_3':
                    if self.map_city[y][x][1] == 'd':
                        r, g, b = 46, 130, 40
                    elif self.map_city[y][x][1] == 'f1':
                        r, g, b = 46, 170, 240
                    elif self.map_city[y][x][1] == '#':
                        r, g, b = 46, 240, 240
                    else:
                        r, g, b = 96, 130, 90
                elif self.map_city[y][x][0] == 'floor_4':
                    if self.map_city[y][x][1] == 'd':
                        r, g, b = 46, 130, 40
                    elif self.map_city[y][x][1] == 'f1':
                        r, g, b = 46, 170, 240
                    elif self.map_city[y][x][1] == '#':
                        r, g, b = 46, 240, 240
                    else:
                        r, g, b = 96, 130, 90
                elif self.map_city[y][x][0] == 'yellow_house':
                    r, g, b = 141, 76, 63
                elif self.map_city[y][x][0] == 'yellow_house_floor':
                    r, g, b = 201, 136, 123
                elif self.map_city[y][x][0] == 'green_house':
                    r, g, b = 115, 141, 63
                elif self.map_city[y][x][0] == 'maze_house':
                    r, g, b = 141, 99, 63
                elif self.map_city[y][x][0] == 'maze_floor_1' or self.map_city[y][x][0] == 'maze_floor_2' or \
                        self.map_city[y][x][0] == 'maze_floor_3' or self.map_city[y][x][0] == 'maze_floor_4':
                    r, g, b = 201, 159, 123
                elif self.map_city[y][x][0] == 'dark_maze_house_1' or self.map_city[y][x][0] == 'dark_maze_house_2':
                    r, g, b = 84, 0, 138
                elif self.map_city[y][x][0] == 'dark_maze_floor_1' or self.map_city[y][x][0] == 'dark_maze_floor_2' or \
                        self.map_city[y][x][0] == 'dark_maze_floor_3' or self.map_city[y][x][0] == 'dark_maze_floor_4':
                    r, g, b = 155, 0, 255
                elif self.map_city[y][x][0] == 'sh':
                    r, g, b = 79, 79, 79
                elif self.map_city[y][x][0] == 'passage':
                    r, g, b = 120, 120, 120
                elif self.map_city[y][x][0] == 'start_floor':
                    if self.map_city[y][x][1] == '@':
                        r, g, b = 250, 150, 150
                    elif self.map_city[y][x][1] == 'e':
                        r, g, b = 250, 50, 50
                    else:
                        r, g, b = 200, 200, 200
                elif self.map_city[y][x][0] == 'player':
                    r, g, b = 255, 0, 0
                else:
                    r, g, b = 0, 0, 0
                image.putpixel(coords, (r, g, b))
        image.save('test_data/' + 'map.png')

    def summer_floor_genesis(self, x, xx, y, yy, k):
        n = random.randint(1, 17)
        if 1 <= n <= 4:
            self.map_city[y + yy][x + xx] = ['floor_1', '.']
        elif 5 <= n <= 8:
            self.map_city[y + yy][x + xx] = ['floor_2', '.']
        elif 9 <= n <= 12:
            self.map_city[y + yy][x + xx] = ['floor_3', '.']
        elif 13 <= n <= 16:
            self.map_city[y + yy][x + xx] = ['floor_4', '.']
        elif n == 17:
            if self.map_city[y + yy - 1][x + xx - 1] != ['floor_3', '.'] or self.map_city[y + yy - 1][x + xx] != ['floor_3', '.'] or self.map_city[y + yy - 1][x + xx + 1] != ['floor_3', '.'] or self.map_city[y + yy][x + xx + 1] != ['floor_3', '.'] or self.map_city[y + yy + 1][x + xx + 1] != ['floor_3', '.'] or self.map_city[y + yy + 1][x + xx] != ['floor_3', '.'] or self.map_city[y + yy + 1][x + xx - 1] != ['floor_3', '.'] or self.map_city[y + yy][x + xx - 1] != ['floor_3', '.']:
                self.summer_floor_genesis_2(x, xx, y, yy)
            else:
                n = random.randint(1, 8)
                if n == 1 or n == 2:
                    self.map_city[y + yy][x + xx] = ['floor_1', '.']
                elif n == 3 or n == 4:
                    self.map_city[y + yy][x + xx] = ['floor_2', '.']
                elif n == 5 or n == 6:
                    self.map_city[y + yy][x + xx] = ['floor_3', '.']
                elif n == 7 or n == 8:
                    self.map_city[y + yy][x + xx] = ['floor_4', '.']
        else:
            n = random.randint(1, 8)
            if n == 1 or n == 2:
                self.map_city[y + yy][x + xx] = ['floor_1', '.']
            elif n == 3 or n == 4:
                self.map_city[y + yy][x + xx] = ['floor_2', '.']
            elif n == 5 or n == 6:
                self.map_city[y + yy][x + xx] = ['floor_3', '.']
            elif n == 7 or n == 8:
                self.map_city[y + yy][x + xx] = ['floor_4', '.']

    def summer_floor_genesis_2(self, x, xx, y, yy):
        n = random.randint(1, 4)
        if n == 1:
            self.map_city[y + yy][x + xx] = ['floor_1', 'd']
        elif n == 2:
            self.map_city[y + yy][x + xx] = ['floor_2', 'd']
        elif n == 3:
            self.map_city[y + yy][x + xx] = ['floor_3', 'd']
        elif n == 4:
            self.map_city[y + yy][x + xx] = ['floor_4', 'd']

    def write_in_txt(self):
        print('Сохранение карты')
        with open('test_data/Test_map.txt', 'w') as writing_file:
            for element in self.map_city:
                print(element, file=writing_file)

    def map_level(self):
        return self.map_city


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    # intro_text = []
    fon = pygame.transform.scale(load_image('else/boot.png'), (WIDTH, HEIGHT))
    name_of_the_game = pygame.transform.scale(load_image('else/RBWOF.png'), (WIDTH, HEIGHT))
    start_text = pygame.transform.scale(load_image('else/CIYWETG2.png'), (WIDTH, HEIGHT))
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

    text = ['Незнакомец: Нет времени обьяснять, найди фонтаны.',
            'Следующие указания поступят позже, возможно',
            'Вы: Ну, ок.']

    for line in text:
        string_rendered = font.render(line, True, pygame.Color('yellow'))
        rect = string_rendered.get_rect()
        text_coord += 10
        rect.top = text_coord
        rect.x = 10
        text_coord += rect.height
        screen.blit(string_rendered, intro_rect)
        pygame.display.flip()

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
                Tile(level[y][x][0], x, y)
                new_player = Player(x, y)
            elif level[y][x][1] == 'd':
                Tile(level[y][x][0], x, y)
                n = random.randint(1, 5)
                if n == 5:
                    Tile(str(level[y][x][1]) + str(1), x, y)
                elif 2 <= n <= 4:
                    Object(str(level[y][x][1]) + str(3), x, y - 1)
                else:
                    Tile(str(level[y][x][1]) + str(2), x, y)
            elif level[y][x][1] == 'e':
                Tile(level[y][x][0], x, y)
                enemies.append(Enemy(x, y))
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


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(enemies_group, all_sprites)
        self.image = enemy_image
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
enemies_group = pygame.sprite.Group()

tile_images = {'wall_1': load_image('world/wall_1.png'),
               'wall_2': load_image('world/wall_2.png'),
               'floor_1': load_image('world/floor_1.png'),
               'floor_2': load_image('world/floor_2.png'),
               'floor_3': load_image('world/floor_3.png'),
               'floor_4': load_image('world/floor_4.png'),
               'yellow_house': load_image('houses/yellow_house/yellow_house.png'),
               'yellow_house_floor': load_image('houses/yellow_house/yellow_house_floor.png'),
               'maze_house': load_image('houses/fire_maze/maze_house.png'),
               'maze_floor_1': load_image('houses/fire_maze/maze_floor_1.png'),
               'maze_floor_2': load_image('houses/fire_maze/maze_floor_2.png'),
               'maze_floor_3': load_image('houses/fire_maze/maze_floor_3.png'),
               'maze_floor_4': load_image('houses/fire_maze/maze_floor_4.png'),
               'dark_maze_house_1': load_image('houses/dark_maze/dark_maze_house_1.png'),
               'dark_maze_house_2': load_image('houses/dark_maze/dark_maze_house_2.png'),
               'dark_maze_floor_1': load_image('houses/dark_maze/dark_maze_floor_1.png'),
               'dark_maze_floor_2': load_image('houses/dark_maze/dark_maze_floor_2.png'),
               'dark_maze_floor_3': load_image('houses/dark_maze/dark_maze_floor_3.png'),
               'dark_maze_floor_4': load_image('houses/dark_maze/dark_maze_floor_4.png'),
               'sh': load_image('houses/start_house/sh.png'),
               'passage': load_image('houses/else/passage.png'),
               'start_passage': load_image('houses/else/passage.png'),
               'start_floor': load_image('houses/start_house/start_floor.png'),
               'd1': load_image('world/d1.png'),
               'd2': load_image('world/d2.png'),
               'd3': load_image('world/d3.png')}

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

enemy_image = load_image('enemies/base_enemy.png')
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
        enemies_group.draw(screen)
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
    lev.rendering()  # Сохраняем изображение карты
    lev.write_in_txt()
    level = lev.map_level()  # Считываем список
    start_screen()
    camera = Camera()
    running = True
    player, enemies, level_x, level_y = generate_level(level)
    standing_flag, running_flag, lr = 0, 0, 2
    standing_list = ['stand_1', 'stand_2', 'stand_3', 'stand_4', 'stand_5', 'stand_6']
    running_list = ['run_1', 'run_2', 'run_3', 'run_4', 'run_5', 'run_6', 'run_7', 'run_8', 'run_9']
    y, x = player.pos[1], player.pos[0]
    upd_camera()
    draw()
    while running:

        keys = pygame.key.get_pressed()
        allowed_cells = ['.', 'e', '@', 'f1']

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

        '''ДВИЖЕНИЕ БОТОВ'''

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            upd_camera()
        draw()
    terminate()
