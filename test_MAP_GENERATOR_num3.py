import random

from PIL import Image


class Map_generation:
    def __init__(self):
        print('Инициализация')
        self.SIZE = 75
        self.wall_len = 5
        self.sea_len = 10
        self.d_len = self.SIZE + self.SIZE + self.wall_len + self.wall_len + self.sea_len + self.sea_len
        self.map_list = []
        self.min_coord = self.max_coord = self.d_len / 2

        self.filling_the_world()

    def filling_the_world(self):
        print('Заполнение мира')
        for y in range(self.d_len):
            line = []
            for x in range(self.d_len):
                line.append(['elem', 'code'])
            self.map_list.append(line)

        self.border_marking()

    def border_marking(self):
        print('Генерируем границы мира')
        xy_wall = []
        xy_floor = []
        xy_sea = []
        r = self.SIZE

        for y in range(self.d_len):
            for x in range(self.d_len):
                if 159999 * self.d_len <= int(
                        ((x - self.d_len / 2) ** 2 + (y - self.d_len / 2) ** 2) ** 2) <= self.d_len * 199999:
                    xy_wall.append([x, y])
                elif int(((x - self.d_len / 2) ** 2 + (y - self.d_len / 2) ** 2) ** 2) >= self.d_len * 199999:
                    xy_sea.append([x, y])

                elif int(((x - self.d_len / 2) ** 2 + (y - self.d_len / 2) ** 2) ** 2) <= 159999 * self.d_len:
                    xy_floor.append([x, y])
                    if x > self.max_coord:
                        self.max_coord = x
                    if x < self.min_coord:
                        self.min_coord = x

        for elem in xy_sea:
            self.map_list[elem[0]][elem[1]][0] = 'sea'
            self.map_list[elem[0]][elem[1]][1] = '.'

        for elem in xy_floor:
            self.map_list[elem[0]][elem[1]][0] = 'floor'
            self.map_list[elem[0]][elem[1]][1] = '.'

        for elem in xy_wall:
            self.map_list[elem[0]][elem[1]][0] = 'wall'
            self.map_list[elem[0]][elem[1]][1] = '#'

        self.creating_a_summer_biome()

    def creating_a_summer_biome(self):
        print('Выращивание летнего биома')
        for y in range(self.d_len):
            for x in range(self.d_len):
                if x == self.d_len / 2 and y == self.d_len / 2:
                    self.lawn_planting(x, y, '@')
                else:
                    if self.map_list[y][x] == ['floor', '.']:
                        n = random.randint(1, 20)
                        if n == 1:
                            self.lawn_planting(x, y, 'd')
                        else:
                            self.lawn_planting(x, y, '.')

        self.fence_reassembly()

    def lawn_planting(self, x, y, code):
        n = random.randint(1, 4)
        if n == 1:
            self.map_list[y][x] = ['floor_1', code]
        elif n == 2:
            self.map_list[y][x] = ['floor_2', code]
        elif n == 3:
            self.map_list[y][x] = ['floor_3', code]
        elif n == 4:
            self.map_list[y][x] = ['floor_4', code]

    def fence_reassembly(self):
        print('Перекраска вашего забора')
        for y in range(self.d_len):
            for x in range(self.d_len):
                if self.map_list[y][x][0] == 'wall':
                    self.fence_repainting(x, y, '#')

        self.evaporation_of_the_sea_and_its_planting()

    def fence_repainting(self, x, y, code):
        n = random.randint(1, 2)
        if n == 1:
            self.map_list[y][x] = ['wall_1', code]
        elif n == 2:
            self.map_list[y][x] = ['wall_2', code]

    def evaporation_of_the_sea_and_its_planting(self):
        print('Испарение моря и его засадка')
        for y in range(self.d_len):
            for x in range(self.d_len):
                if self.map_list[y][x][0] == 'sea':
                    n = random.randint(1, 20)
                    if n == 1:
                        self.lawn_planting(x, y, 'd')
                    else:
                        self.lawn_planting(x, y, '.')

        self.territory_marking()

    def territory_marking(self):
        print('Разметка территории')
        n1 = random.randint(1, 4)
        n2 = random.randint(1, 4)
        while n2 == n1:
            n2 = random.randint(1, 4)
        n3 = random.randint(1, 4)
        while n3 == n2 or n3 == n1:
            n3 = random.randint(1, 4)
        n4 = random.randint(1, 4)
        while n4 == n3 or n4 == n2 or n4 == n1:
            n4 = random.randint(1, 4)

        self.burning_flora_and_fauna(n2)
        self.overlay_corruption_on_the_landscape(n3)

    def burning_flora_and_fauna(self, n):
        print('Выжигание флоры и фауны')

        xx = yy = 0
        xy_fire = []

        if n == 1:
            xx, yy = self.d_len / 4, self.d_len / 4
        elif n == 2:
            xx, yy = self.d_len / 4 * 3, self.d_len / 4
        elif n == 3:
            xx, yy = self.d_len / 4 * 3, self.d_len / 4 * 3
        elif n == 4:
            xx, yy = self.d_len / 4, self.d_len / 4 * 3

        for y in range(self.d_len):
            for x in range(self.d_len):
                if int(((x - xx) ** 2 + (y - yy) ** 2) ** 2) <= self.d_len * 159999 / 20:
                    xy_fire.append([x, y])

        for elem in xy_fire:
            x, y = elem[0], elem[1]
            if self.map_list[y][x][0] != 'wall_1' and self.map_list[y][x][0] != 'wall_2':
                n = random.randint(1, 40)
                if n == 1:
                    self.fiery_landscape(x, y, 'd', n)
                elif n == 2:
                    n = 3
                    self.fiery_landscape(x, y, '#', n)
                else:
                    self.fiery_landscape(x, y, '.', n)

    def fiery_landscape(self, x, y, code, n):
        if n == 1:
            self.map_list[y][x] = ['maze_floor_5', code]
        elif n == 2:
            pass
        else:
            n = random.randint(1, 4)
            if n == 1:
                self.map_list[y][x] = ['maze_floor_1', code]
            elif n == 2:
                self.map_list[y][x] = ['maze_floor_2', code]
            elif n == 3:
                self.map_list[y][x] = ['maze_floor_3', code]
            elif n == 4:
                self.map_list[y][x] = ['maze_floor_4', code]

    def overlay_corruption_on_the_landscape(self, n):
        print('Наложение порчи на ландшафт')

        xx = yy = 0
        xy_fire = []

        if n == 1:
            xx, yy = self.d_len / 4, self.d_len / 4
        elif n == 2:
            xx, yy = self.d_len / 4 * 3, self.d_len / 4
        elif n == 3:
            xx, yy = self.d_len / 4 * 3, self.d_len / 4 * 3
        elif n == 4:
            xx, yy = self.d_len / 4, self.d_len / 4 * 3

        for y in range(self.d_len):
            for x in range(self.d_len):
                if int(((x - xx) ** 2 + (y - yy) ** 2) ** 2) <= self.d_len * 159999 / 20:
                    xy_fire.append([x, y])

        for elem in xy_fire:
            x, y = elem[0], elem[1]
            if self.map_list[y][x][0] != 'wall_1' and self.map_list[y][x][0] != 'wall_2':
                n = random.randint(1, 40)
                if n == 1:
                    n = 3
                    self.dark_brick_laying(x, y, 'd', n)
                elif n == 2:
                    n = 3
                    self.dark_brick_laying(x, y, '#', n)
                else:
                    self.dark_brick_laying(x, y, '.', n)

    def dark_brick_laying(self, x, y, code, n):
        if n == 1:
            pass
        elif n == 2:
            n = random.randint(1, 2)
            if n == 1:
                self.map_list[y][x] = ['dark_maze_house_1', '.']
            elif n == 2:
                self.map_list[y][x] = ['dark_maze_house_2', '.']
        else:
            n = random.randint(1, 4)
            if n == 1:
                self.map_list[y][x] = ['dark_maze_floor_1', '.']
            elif n == 2:
                self.map_list[y][x] = ['dark_maze_floor_2', '.']
            elif n == 3:
                self.map_list[y][x] = ['dark_maze_floor_3', '.']
            elif n == 4:
                self.map_list[y][x] = ['dark_maze_floor_4', '.']

    def rendering(self):
        print('Создание изображения первоначальной карты')
        image = Image.new("RGB", (self.d_len, self.d_len), (0, 0, 0))
        for y in range(self.d_len):
            for x in range(self.d_len):
                coords = (x, y)
                if self.map_list[y][x][0] == 'wall_1':
                    r, g, b = 71, 31, 0
                elif self.map_list[y][x][0] == 'wall_2':
                    r, g, b = 81, 41, 0
                elif self.map_list[y][x][0] == 'floor_1':
                    if self.map_list[y][x][1] == 'd':
                        r, g, b = 10, 109, 37
                    else:
                        r, g, b = 10, 149, 67
                elif self.map_list[y][x][0] == 'floor_2':
                    if self.map_list[y][x][1] == 'd':

                        r, g, b = 10, 109, 37
                    else:
                        r, g, b = 20, 159, 87
                elif self.map_list[y][x][0] == 'floor_3':
                    if self.map_list[y][x][1] == 'd':
                        r, g, b = 10, 109, 37
                    else:
                        r, g, b = 30, 169, 97
                elif self.map_list[y][x][0] == 'floor_4':
                    if self.map_list[y][x][1] == 'd':
                        r, g, b = 10, 109, 37
                    else:
                        r, g, b = 40, 179, 107
                elif self.map_list[y][x][0] == 'sea':
                    r, g, b = 0, 134, 179
                elif self.map_list[y][x][0] == 'maze_floor_1':
                    r, g, b = 168, 118, 72
                elif self.map_list[y][x][0] == 'maze_floor_2':
                    r, g, b = 178, 108, 62
                elif self.map_list[y][x][0] == 'maze_floor_3':
                    r, g, b = 188, 98, 52
                elif self.map_list[y][x][0] == 'maze_floor_4':
                    r, g, b = 198, 88, 42
                elif self.map_list[y][x][0] == 'maze_floor_5':
                    r, g, b = 208, 78, 32
                elif self.map_list[y][x][0] == 'dark_maze_floor_1':
                    r, g, b = 114, 102, 108
                elif self.map_list[y][x][0] == 'dark_maze_floor_2':
                    r, g, b = 124, 92, 108
                elif self.map_list[y][x][0] == 'dark_maze_floor_3':
                    r, g, b = 134, 82, 108
                elif self.map_list[y][x][0] == 'dark_maze_floor_4':
                    r, g, b = 144, 72, 108
                elif self.map_list[y][x][0] == 'dark_maze_house_1':
                    r, g, b = 84, 52, 88
                elif self.map_list[y][x][0] == 'dark_maze_house_2':
                    r, g, b = 84, 52, 88
                else:
                    r, g, b = 0, 0, 0

                if self.map_list[y][x][1] == '@':
                    r, g, b = 250, 0, 250
                image.putpixel(coords, (r, g, b))
        image.save('test_data/' + 'map.png')

    def write_in_txt(self):
        print('Сохранение карты')
        with open('test_data/Test_map.txt', 'w') as writing_file:
            for element in self.map_list:
                print(element, file=writing_file)

    def map_level(self):
        return self.map_list


level = Map_generation()
level.rendering()  # Сохраняем изображение карты
level.write_in_txt()  # Сохраняем список в текстовый файл
map_lev = level.map_level()  # Считываем карту
