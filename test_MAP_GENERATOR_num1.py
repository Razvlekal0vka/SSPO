"""Библиотеки"""
import random

"""Обозначения"""
' '  # пустота
'.'  # поле по которуму может ходить игрок
'#'  # стена
'@'  # стартовая позиция
'East'  # 1
'South'  # 2
'West'  # 3
'North'  # 4

"""Настройка"""
# Настройка стартовых направлений
directions = [[1, 2, 3, 4], ['x']]
# directions = [[1, 2, 3, 4], ['x']] максимальный фарш
# directions = ['r'] - рандомные направления, иначе необходимо передать список
# directions = [['x'], [n]], где n это количество исходных направлений
# directions = [[d1, ...], ['x']], где d1, ... это номера направлений, кодировку смотрите выше, в обозначениях

# Настройка длины коридоров
length_of_corridors = ['r', 20, 40]
# length_of_corridors = ['r', 10, 15] рандомная длина, включает написанные значения
# length_of_corridors = ['o', 10, 0] определённая длина (10)

# Настройка размеров игровой комнаты
room_sizes = ['r', 100, 200, 2]
# из игровых сооброжений не следует ставить менее чем 30*30
# room_sizes = ['r', 30, 50, 2] рандомная длина стенок, включает написанные значения
# последнюю цифру желательно не трогать, тк она обеспечивает четные значения
# room_sizes = ['o', 40, 46] определённая длина стенок, включает написанные
# не следует писать не четные значения

# Настройка размеров комнаты, желательно не трогать
starting_room_sizes = 50

# Настройка размеров комнаты, желательно не трогать
map_size = 1000

# Максимальная длина ветки
maximum_branch_length = 5

# Максимальное деление ветки, не превышает длину ветки
maximum_division_of_a_branch = 3


class Map_generation:
    def __init__(self, size_map, size_room, direc, loc, max_len_br, max_div_br, rs):
        self.WIDTH = self.HEIGHT = self.SIZE = size_map  # размеры карты
        self.generation = True
        self.MAP = []  # слайс карты
        self.SIZE_room = size_room  # размеры начальной комнаты
        self.ends, self.root_ends = [], []
        self.directions = direc  # Настройка стартовых направлений
        self.length_of_corridors = loc  # Настройка длнины коридоров
        self.max_len_br = max_len_br  # Настройка длины веток
        self.max_div_br = max_div_br  # Настройка количества веток
        self.dir = []
        self.room_size = rs
        self.room_coordinates = []  # Координаты всех комнат

        self.Filling_the_map_with_emptiness()

    def Filling_the_map_with_emptiness(self):
        """Заполнение карты пустотой"""
        for y in range(self.SIZE):
            line = []
            for x in range(self.SIZE):
                line.append([' '])
            self.MAP.append(line)
        print('Создание и заполнение списка')

        self.Setting_the_starting_location()

    def Setting_the_starting_location(self):
        """Установка стартовой локации"""
        # стартовая локация имеет размеры self.SIZE_room и находится в центре карты
        # устанавливаем координаты комнаты
        print('Генирация начальной локации')
        x1, y1 = int(self.SIZE / 2 - self.SIZE_room / 2), int(self.SIZE / 2 - self.SIZE_room / 2)
        x2, y2 = int(self.SIZE / 2 + self.SIZE_room / 2), int(self.SIZE / 2 + self.SIZE_room / 2)

        self.room_coordinates.append([x1, y1, self.SIZE_room, self.SIZE_room])

        # Проверка параметров создаваймой начальной локации
        if self.directions == ['r'] or not self.directions[0] or not self.directions[1]:
            east = random.randint(0, 1)
            south = random.randint(0, 1)
            west = random.randint(0, 1)
            north = random.randint(0, 1)
            # Если нет дорог, то идем перегенирировать пока не получим хотя бы 1 дорогу
            while east + south + west + north == 0:
                east = random.randint(0, 1)
                south = random.randint(0, 1)
                west = random.randint(0, 1)
                north = random.randint(0, 1)

        elif self.directions[0][0] == 'x':
            number_of_directions = self.directions[1][0]
            if number_of_directions == 0:
                number_of_directions = 1
            east = south = west = north = 0
            while east + south + west + north != number_of_directions:
                east = random.randint(0, 1)
                south = random.randint(0, 1)
                west = random.randint(0, 1)
                north = random.randint(0, 1)

        elif self.directions[1][0] == 'x':
            if 1 not in self.directions[0]:
                east = 0
            else:
                east = 1
            if 2 not in self.directions[0]:
                south = 0
            else:
                south = 1
            if 3 not in self.directions[0]:
                west = 0
            else:
                west = 1
            if 4 not in self.directions[0]:
                north = 0
            else:
                north = 1

        if east == 1:
            self.dir.append(1)
        if south == 1:
            self.dir.append(2)
        if west == 1:
            self.dir.append(3)
        if north == 1:
            self.dir.append(4)

        # создаем стены по данным нам координатам и пропиливаем проходы
        if True:
            pc, z = [], 0  # |
            n, n1 = 0, 0  # |
            f, f1 = 1, 1  # | отвечают за определение крайних точек прохода (нужны для генирации проходов)
            for y in range(y1, y2 + 1):  # |
                n = y
                f = 1
                if east == 1:
                    if y >= self.SIZE / 2 + self.SIZE_room * 0.1 + 1 or y < self.SIZE / 2 - self.SIZE_room * 0.1:
                        self.MAP[y - 1][x2 - 1][0], f = '#', 0
                else:
                    self.MAP[y - 1][x2 - 1][0], f = '#', 0
                if ((f == 0 and f1 == 1) or (f == 1 and f1 == 0)) and z == 0:
                    z = 1
                elif f == 0 and f1 == 1:
                    pc.append([x2 - 1, n1])
                elif f == 1 and f1 == 0:
                    pc.append([x2 - 1, n])
                f1, n1 = f, n
            self.root_ends.append(pc)

            pc, z = [], 0  # |
            n, n1 = 0, 0  # |
            f, f1 = 1, 1  # | отвечают за определение крайних точек прохода (нужны для генирации проходов)
            for x in range(x1, x2 + 1):
                n = x
                f = 1
                if south == 1:
                    if x >= self.SIZE / 2 + self.SIZE_room * 0.1 + 1 or x < self.SIZE / 2 - self.SIZE_room * 0.1:
                        self.MAP[y2 - 1][x - 1][0], f = '#', 0
                else:
                    self.MAP[y2 - 1][x - 1][0], f = '#', 0
                if ((f == 0 and f1 == 1) or (f == 1 and f1 == 0)) and z == 0:
                    z = 1
                elif f == 0 and f1 == 1:
                    pc.append([n1, y2 - 1])
                elif f == 1 and f1 == 0:
                    pc.append([n, y2 - 1])
                f1, n1 = f, n
            self.root_ends.append(pc)

            pc, z = [], 0  # |
            n, n1 = 0, 0  # |
            f, f1 = 1, 1  # | отвечают за определение крайних точек прохода (нужны для генирации проходов)
            for y in range(y1, y2 + 1):  # |
                n = y
                f = 1
                if west == 1:
                    if y >= self.SIZE / 2 + self.SIZE_room * 0.1 + 1 or y < self.SIZE / 2 - self.SIZE_room * 0.1:
                        self.MAP[y - 1][x1 - 1][0], f = '#', 0
                else:
                    self.MAP[y - 1][x1 - 1][0], f = '#', 0
                if ((f == 0 and f1 == 1) or (f == 1 and f1 == 0)) and z == 0:
                    z = 1
                elif f == 0 and f1 == 1:
                    pc.append([x1 - 1, n1])
                elif f == 1 and f1 == 0:
                    pc.append([x1 - 1, n])
                f1, n1 = f, n
            self.root_ends.append(pc)

            pc, z = [], 0  # |
            n, n1 = 0, 0  # |
            f, f1 = 1, 1  # | отвечают за определение крайних точек прохода (нужны для генирации проходов)
            for x in range(x1, x2 + 1):
                n = x
                f = 1
                if north == 1:
                    if x >= self.SIZE / 2 + self.SIZE_room * 0.1 + 1 or x < self.SIZE / 2 - self.SIZE_room * 0.1:
                        self.MAP[y1 - 1][x - 1][0], f = '#', 0
                else:
                    self.MAP[y1 - 1][x - 1][0], f = '#', 0
                if ((f == 0 and f1 == 1) or (f == 1 and f1 == 0)) and z == 0:
                    z = 1
                elif f == 0 and f1 == 1:
                    pc.append([n1, y1 - 1])
                elif f == 1 and f1 == 0:
                    pc.append([n, y1 - 1])
                f1, n1 = f, n
            self.root_ends.append(pc)

        """Теперь необходимо создавать отдельные локации в определённых направлениях, и проходы до них"""
        self.Leveled_branch_root()

    def Leveled_branch_root(self):
        """Здесь рассматривается направление ветвей"""
        d = []
        for n in range(len(self.dir)):
            dir = random.choice(self.dir)
            if dir not in d:
                d.append(dir)
                self.Creating_leveled_branches(dir)
            else:
                while dir in d:
                    dir = random.choice(self.dir)
                d.append(dir)
                self.Creating_leveled_branches(dir)

    def Creating_leveled_branches(self, direction):
        """Здесь происходит генирация ветвей"""
        print(f'Начало создания ветки {direction}')
        # сначала создае  проход к новой локации
        end_coord = self.Create_passages(direction, self.root_ends[direction - 1])
        # создаем комнату в конце коридора
        self.Creating_rooms(end_coord, direction)
        self.write_in_txt()

    def Creating_rooms(self, end_coord, direction):
        """Здесь происходит генирация комнат"""
        print('Создание комнаты')
        # определение типа генирации комнаты

        if self.room_size[0] == 'r':
            a = random.randrange(self.room_size[1], self.room_size[2], self.room_size[3])
            b = random.randrange(self.room_size[1], self.room_size[2], self.room_size[3])
        elif self.room_size[0] == 'o':
            a, b = self.room_size[1], self.room_size[2]

        # находим смещение относительно прохода
        r = abs(end_coord[0][0] - end_coord[1][0]) + abs(end_coord[0][1] - end_coord[1][1])
        r = 0.5 * (min(a, b) - r)
        r = random.randint(1, r)  # смещение относительно прохода
        s = random.randint(0, 1)  # вправо или влево

        # устанавливаем координаты комнаты
        # east, south, west, north = 0, 0, 0, 0
        # 0 Простая стена
        # 1 Будущий проход (НЕ РАБОТАЕТ)
        # 2 Вход в комнату
        if direction == 1:
            if s == 0:
                x1, y1 = end_coord[0][0] + 1, end_coord[0][1] + r - b
                x2, y2 = x1 + a + 1, y1 + b + r + 5
            else:
                x1, y1 = end_coord[0][0] + 1, end_coord[0][1] + r - b
                x2, y2 = x1 + a + 1, y1 + b + 5
            east, south, west, north = 0, 0, 2, 0

        if direction == 2:
            if s == 1:
                x1, y1 = end_coord[0][0] - r, end_coord[0][1] + 1
                x2, y2 = x1 + a, y1 + b + 1
            else:
                x1, y1 = end_coord[0][0] + r - a, end_coord[0][1] + 1
                x2, y2 = x1 + a, y1 + b + 1
            east, south, west, north = 0, 0, 0, 2

        if direction == 3:
            if s == 0:
                x1, y1 = end_coord[0][0] - a, end_coord[0][1] - r
                x2, y2 = x1 + a + 1, y1 + b
            else:
                x1, y1 = end_coord[0][0] - a, end_coord[0][1] + r - b
                x2, y2 = x1 + a + 1, y1 + b
            east, south, west, north = 2, 0, 0, 0

        if direction == 4:
            if s == 1:
                x1, y1 = end_coord[0][0] - r, end_coord[0][1] - b
                x2, y2 = x1 + a, y1 + b + 1
            else:
                x1, y1 = end_coord[0][0] + r - a, end_coord[0][1] - b
                x2, y2 = x1 + a, y1 + b + 1
            east, south, west, north = 0, 2, 0, 0
        print(f'Код генирации - {s}')

        # создаем стены по данным нам координатам и пропиливаем проходы
        if True:
            pc, z = [], 0  # |
            n, n1 = 0, 0  # |
            f, f1 = 1, 1  # | отвечают за определение крайних точек прохода (нужны для генирации проходов)
            for y in range(y1, y2 + 1):  # |
                n = y
                f = 1
                if east == 2:
                    if y > max(end_coord[0][1], end_coord[1][1]) or y < min(end_coord[0][1], end_coord[1][1]):
                        self.MAP[y - 1][x2 - 1][0], f = '#', 0
                else:
                    self.MAP[y - 1][x2 - 1][0], f = '#', 0
                if ((f == 0 and f1 == 1) or (f == 1 and f1 == 0)) and z == 0:
                    z = 1
                elif f == 0 and f1 == 1:
                    pc.append([x2 - 1, n1])
                elif f == 1 and f1 == 0:
                    pc.append([x2 - 1, n])
                f1, n1 = f, n
            self.root_ends.append(pc)

            pc, z = [], 0  # |
            n, n1 = 0, 0  # |
            f, f1 = 1, 1  # | отвечают за определение крайних точек прохода (нужны для генирации проходов)
            for x in range(x1, x2 + 1):
                n = x
                f = 1
                if south == 2:
                    if x > max(end_coord[0][0], end_coord[1][0]) or x < min(end_coord[0][0], end_coord[1][0]):
                        self.MAP[y2 - 1][x - 1][0], f = '#', 0
                else:
                    self.MAP[y2 - 1][x - 1][0], f = '#', 0
                if ((f == 0 and f1 == 1) or (f == 1 and f1 == 0)) and z == 0:
                    z = 1
                elif f == 0 and f1 == 1:
                    pc.append([n1, y2 - 1])
                elif f == 1 and f1 == 0:
                    pc.append([n, y2 - 1])
                f1, n1 = f, n
            self.root_ends.append(pc)

            pc, z = [], 0  # |
            n, n1 = 0, 0  # |
            f, f1 = 1, 1  # | отвечают за определение крайних точек прохода (нужны для генирации проходов)
            for y in range(y1, y2 + 1):  # |
                n = y
                f = 1
                if west == 2:
                    if y > max(end_coord[0][1], end_coord[1][1]) or y < min(end_coord[0][1], end_coord[1][1]):
                        self.MAP[y - 1][x1 - 1][0], f = '#', 0
                else:
                    self.MAP[y - 1][x1 - 1][0], f = '#', 0
                if ((f == 0 and f1 == 1) or (f == 1 and f1 == 0)) and z == 0:
                    z = 1
                elif f == 0 and f1 == 1:
                    pc.append([x1 - 1, n1])
                elif f == 1 and f1 == 0:
                    pc.append([x1 - 1, n])
                f1, n1 = f, n
            self.root_ends.append(pc)

            pc, z = [], 0  # |
            n, n1 = 0, 0  # |
            f, f1 = 1, 1  # | отвечают за определение крайних точек прохода (нужны для генирации проходов)
            for x in range(x1, x2 + 1):
                n = x
                f = 1
                if north == 2:
                    if x > max(end_coord[0][0], end_coord[1][0]) or x < min(end_coord[0][0], end_coord[1][0]):
                        self.MAP[y1 - 1][x - 1][0], f = '#', 0
                else:
                    self.MAP[y1 - 1][x - 1][0], f = '#', 0
                if ((f == 0 and f1 == 1) or (f == 1 and f1 == 0)) and z == 0:
                    z = 1
                elif f == 0 and f1 == 1:
                    pc.append([n1, y1 - 1])
                elif f == 1 and f1 == 0:
                    pc.append([n, y1 - 1])
                f1, n1 = f, n
            self.root_ends.append(pc)

        self.write_in_txt()

    def Create_passages(self, direction, coord):
        """Здесь создаются проходы"""
        print('Создание прохода')
        # Определяем длину коридора
        if self.length_of_corridors[0] != 'r' and self.length_of_corridors[0] != 'o':
            len_cor = random.randint(20, 40)
        elif self.length_of_corridors[0] == 'r':
            len_cor = random.randint(int(self.length_of_corridors[1]), int(self.length_of_corridors[2]) + 1)
        elif self.length_of_corridors[0] == 'o':
            len_cor = self.length_of_corridors[1]

        # устанавливаем координаты прохода, определяем создаваемые стенки
        if direction == 1:
            x1, y1 = int(coord[0][0]), int(coord[0][1])
            x2, y2 = int(coord[1][0]) + len_cor, int(coord[1][1])
            east, south, west, north = 0, 1, 0, 1
        if direction == 2:
            x1, y1 = x1, y1 = int(coord[0][0]), int(coord[0][1])
            x2, y2 = int(coord[1][0]), int(coord[1][1] + len_cor)
            east, south, west, north = 1, 0, 1, 0
        if direction == 3:
            x1, y1 = int(coord[0][0]) - len_cor, int(coord[0][1])
            x2, y2 = int(coord[1][0]), int(coord[1][1])
            east, south, west, north = 0, 1, 0, 1
        if direction == 4:
            x1, y1 = x1, y1 = int(coord[0][0]), int(coord[0][1] - len_cor)
            x2, y2 = int(coord[1][0]), int(coord[1][1])
            east, south, west, north = 1, 0, 1, 0

        # создаем стены по данным нам координатам
        if True:
            if east == 1:
                for y in range(y1, y2 + 1):  # |
                    self.MAP[y][x2 - 1][0], f = '#', 0

            if south == 1:
                for x in range(x1, x2 + 1):
                    self.MAP[y2 - 1][x][0], f = '#', 0

            if west == 1:
                for y in range(y1, y2 + 1):  # |
                    self.MAP[y][x1 - 1][0], f = '#', 0

            if north == 1:
                for x in range(x1, x2 + 1):
                    self.MAP[y1 - 1][x][0], f = '#', 0

            print(' - Проход создан')

            # Возвращаем координаты крайних точек
            if direction == 1:
                return [[x2, y1], [x2, y2]]
            if direction == 2:
                return [[x1, y2], [x2, y2]]
            if direction == 3:
                return [[x1, y1], [x1, y2]]
            if direction == 4:
                return [[x1, y1], [x2, y1]]

    def write_in_txt(self):
        with open('data/Test_map.txt', 'w') as writing_file:
            for element in self.MAP:
                print(*element, file=writing_file)

    def Map(self):
        return self.MAP


a = Map_generation(map_size, starting_room_sizes, directions, length_of_corridors, maximum_branch_length,
                   maximum_division_of_a_branch, room_sizes)
map_coords = a.Map()
print(map_coords)
