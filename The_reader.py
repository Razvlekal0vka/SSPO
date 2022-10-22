with open('test_data/Test_map.txt', encoding='utf8') as f:
    level = [line.strip() for line in f.readlines()]
    for y in range(len(level)):
        line_of_cells = level[y][2:-2].split('], [')
        for x in range(len(line_of_cells)):
            cell = line_of_cells[x][1:-1].split("', '")
            if cell[1] == '@':
                print(cell)
