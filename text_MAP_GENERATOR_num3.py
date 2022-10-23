from PIL import Image, ImageDraw


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
        image = Image.open('data/AirposrtDes.png')  # Открываем изображение
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

                if (r, g, b) == (107, 107, 107):
                    self.map_city[y][x] = ['floor_1', '.']
                if (r, g, b) == (255, 0, 0):
                    self.map_city[y][x] = ['floor_2', '.']
                if (r, g, b) == (255, 255, 255):
                    self.map_city[y][x] = ['floor_3', '.']
                `else:
                    self.map_city[y][x] = ['floor_4', '.']`

        print(1)
        self.write_in_txt()

    def write_in_txt(self):
        print(2)
        with open('test_data/Test_map.txt', 'w') as writing_file:
            for element in self.map_city:
                print(element, file=writing_file)


if __name__ == '__main__':
    lev = Map_generation()
    lev.write_in_txt()
