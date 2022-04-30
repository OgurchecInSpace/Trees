# Деревья
import random as rm
import pygame
import pprint as pp

# Импорт всего нужного

count = 0
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SIZE = 10
WIDTH = 1200  # ширина игрового окна
HEIGHT = 700  # высота игрового окна
FPS = 30  # частота кадров в секунду
ENERGY_ON_CELL = 13
FLOOR = HEIGHT * 0.9

cells_woods = set()
all_sprites = pygame.sprite.Group()


class Cell_to_tree(pygame.sprite.Sprite):  # Клетки, которые станут деревьями (читай - семена)
    def __init__(self, num, x, y, genome=None):
        pygame.sprite.Sprite.__init__(self)
        cells_to_trees_sprites.add(self)
        cells_to_trees.add(self)

        self.num = num

        self.image = pygame.Surface((SIZE, SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y  # Настраиваем спрайты Pygame
        cells_woods.add((self.rect.x, self.rect.y))

        self.genome = genome
    def fall(self):  # Метод падения
        global count
        global trees
        if self.rect.y + SIZE <= FLOOR and (self.rect.x, self.rect.y + SIZE) not in cells_woods:
            if (self.rect.x, self.rect.y) in cells_woods:
                cells_woods.remove((self.rect.x, self.rect.y))
            self.rect.y += SIZE
            cells_woods.add((self.rect.x, self.rect.y))
        if (self.rect.x, self.rect.y + SIZE) in cells_woods or (self.rect.x, self.rect.y + SIZE) == FLOOR:
            cells_to_trees.remove(self)
            self.kill()
            trees.add(Tree(count, len(trees), self.rect.x, self.rect.y, genome=self.genome))
            count += 1

class Cell(pygame.sprite.Sprite):  # Клетка дерева
    def __init__(self, num, x, y, parent, gene=0):  # Инициализируем часть дерева (клетку размножения)
        self.gene = gene
        pygame.sprite.Sprite.__init__(self)
        all_sprites.add(self)
        parent.cells_sprites.add(self)  # Добавляем себя во все массивы спрайтов
        self.num = num
        self.parent = parent  # Проставляем обычные значения

        self.image = pygame.Surface((SIZE, SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y  # Настраиваем спрайты Pygame
        cells_woods.add((self.rect.x, self.rect.y))

    def __repr__(self):
        return f'Клетка размножения {self.num}. X = {self.rect.x}, Y = {self.rect.y}'


class Wood(pygame.sprite.Sprite):  # Часть дерева (древесина)
    def __init__(self, num, x, y, parent):  # Инициализируем часть дерева (древесину (её клетку))
        pygame.sprite.Sprite.__init__(self)
        all_sprites.add(self)
        parent.woods_sprites.add(self)  # Добавляем себя во все массивы спрайтов
        self.num = num
        self.parent = parent  # Проставляем обычные значения

        self.image = pygame.Surface((SIZE, SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y  # Настраиваем спрайты Pygame
        cells_woods.add((self.rect.x, self.rect.y))

    def __repr__(self):
        return f'Древесина {self.num}. X = {self.rect.x}, Y = {self.rect.y}'

    def get_energy(self):  # получение энергии из клетки
        if len(cells_woods) > 3:
            num = 3
        else:
            num = len(cells_woods) + 1
        top = sorted(cells_woods, key=lambda coords: coords[1], reverse=True)[0:num]
        if (self.rect.x, self.rect.y) in top:
            position = top.index((self.rect.x, self.rect.y)) + 1
            energy = HEIGHT - (self.rect.y / SIZE) * position
            return energy
        return 0


class Tree:  # Дерево
    def __init__(self, name, num, x, y, genome=None):  # Инициализируем класс деревца
        self.cells_sprites = pygame.sprite.Group()
        self.woods_sprites = pygame.sprite.Group()
        self.name = name
        self.num = len(trees)
        self.x = x
        self.y = y  # Проставляем все нужные значения

        if genome is None:  # Если геном не задан, то генерируем свой
            self.genome = [
                {'left': int(rm.randrange(0, 31)),
                 'up': int(rm.randrange(0, 31)),
                 'right': int(rm.randrange(0, 31)),
                 'down': int(rm.randrange(0, 31))} for _ in range(16)
            ]  # Я надеюсь, что не забуду ещё лет 5, как работают списочные выражения, так что не буду комментировать этот момент
        else:
            self.genome = genome  # Иначе берём заданный

        if not rm.randrange(0, 4):  # И вносим случайные изменения (мы ж тут эволюцией занимаемся)
            direction = rm.choice(('left', 'up', 'right', 'down'))
            self.genome[rm.randrange(0, 16)][direction] = rm.randrange(0, 31)

        self.cells = set()
        self.cells.add(Cell(0, x, y, self))
        self.woods = set()
        self.woods.add(Wood(0, x, y, self))

    def __repr__(self):
        return f'Дерево {self.name} под номер {self.num}. X {self.x}, Y {self.y}'

    def end(self):  # Метод конца дерева (грустнявка :(((((( )
        energy = 0
        print('end')
        for wood in self.woods:
            energy += wood.get_energy()
            wood_key = (wood.rect.x, wood.rect.y)
            if wood_key in cells_woods:
                cells_woods.remove(wood_key)

        for cell in self.cells:
            cell_key = (cell.rect.x, cell.rect.y)
            if cell_key in cells_woods:
                cells_woods.remove(cell_key)
            new_cell_to_tree = Cell_to_tree(len(cells_to_trees), cell.rect.x, cell.rect.y, genome=self.genome)
            cells_to_trees.add(new_cell_to_tree)

        self.cells = set()
        self.woods = set()
        self.woods_sprites = pygame.sprite.Group()
        self.cells_sprites = pygame.sprite.Group()
        trees.remove(self)

    def update(self):  # рост дерева (хз почему апдейт)
        new_cells = set()
        energy = 0
        for wood in self.woods:  # Сбор энергии с клеток
            cells_woods.add((wood.rect.x, wood.rect.y))
            energy += wood.get_energy()
        if energy / (len(self.cells) + len(
                self.woods)) >= ENERGY_ON_CELL:  # Если энергии на каждую клетку приходится достаточно, то фигачим
            print(f'Энергия дерева на клетку = {energy / (len(self.cells) + len(self.woods))}')
            for cell in self.cells:  # Проходимся по всем клеткам
                cells_woods.add((cell.rect.x, cell.rect.y))

                if cell.gene <= 15:  # Сложный момент кода, который отвечает за, собственно, сам рост дерева. Мне лень объяснять
                    # Лучше посмотрите видео, откуда я брал идеи, реализуемые мной:
                    # https://www.youtube.com/watch?v=WTh-gNZxTM8
                    for direction, gene in self.genome[cell.gene].items():
                        if direction == 'left' and \
                                (cell.rect.x - SIZE, cell.rect.y) not in cells_woods\
                                and cell.rect.x - SIZE > SIZE:
                            new_cells.add(Cell(len(self.cells), cell.rect.x - SIZE, cell.rect.y, self, gene=gene))  # Влево

                        elif direction == 'up' and \
                                (cell.rect.x, cell.rect.y - SIZE) not in cells_woods\
                                and cell.rect.y - SIZE > SIZE:
                            new_cells.add(Cell(len(self.cells), cell.rect.x, cell.rect.y - SIZE, self, gene=gene))  # Вверх

                        elif direction == 'right' and \
                                (cell.rect.x + SIZE, cell.rect.y) not in cells_woods\
                                and cell.rect.x + SIZE < WIDTH - SIZE:
                            new_cells.add(Cell(len(self.cells), cell.rect.x - SIZE, cell.rect.y, self, gene=gene))  # Вправо

                        elif direction == 'down' and \
                                (cell.rect.x, cell.rect.y + SIZE) not in cells_woods \
                                and cell.rect.y + SIZE < HEIGHT - SIZE and cell.rect.y + SIZE <= FLOOR:
                            new_cells.add(Cell(len(self.cells), cell.rect.x, cell.rect.y + SIZE, self, gene=gene))  # Вниз

                    cell.kill()
                    cells_woods.remove((cell.rect.x, cell.rect.y))  # Удаляем клетку отовсюду

                    self.woods.add(Wood(len(self.woods), cell.rect.x, cell.rect.y, self))  # добавляем вместо клетки древесину

            self.cells = new_cells
            if len(self.cells) == 0:  # Если клетки размножения кончились
                print(f'Клетки размножения кончились у дерева {self}')
                self.end()
                print('----')
        else:  # И если энергия кончилась
            print(f'Энергия кончилась у дерева {self}')
            self.end()
            print('----')


pygame.init()  # инициализация всего интерфейса
pygame.mixer.init()  # для звука
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # pygame.RESIZABLE)  # окно
pygame.display.set_caption("Trees")  # имя окна
clock = pygame.time.Clock()  # Время
running = True

trees = set()  # Множество деревьев
cells_to_trees = set()  # множество клеток, которые упадут и станут деревьями
cells_to_trees_sprites = pygame.sprite.Group()
count += 1
trees.add(Tree('fsdkdskfsd', count, WIDTH / 2, FLOOR, genome=
[{'down': 12, 'left': 20, 'right': 6, 'up': 13},
 {'down': 0, 'left': 10, 'right': 10, 'up': 18},
 {'down': 4, 'left': 14, 'right': 11, 'up': 18},
 {'down': 20, 'left': 15, 'right': 16, 'up': 24},
 {'down': 16, 'left': 14, 'right': 8, 'up': 25},
 {'down': 16, 'left': 20, 'right': 24, 'up': 0},
 {'down': 10, 'left': 1, 'right': 0, 'up': 17},
 {'down': 5, 'left': 19, 'right': 18, 'up': 26},
 {'down': 25, 'left': 11, 'right': 30, 'up': 25},
 {'down': 28, 'left': 27, 'right': 17, 'up': 9},
 {'down': 12, 'left': 13, 'right': 22, 'up': 5},
 {'down': 1, 'left': 9, 'right': 26, 'up': 22},
 {'down': 2, 'left': 23, 'right': 23, 'up': 6},
 {'down': 1, 'left': 25, 'right': 25, 'up': 13},
 {'down': 19, 'left': 28, 'right': 16, 'up': 23},
 {'down': 10, 'left': 13, 'right': 23, 'up': 15}]
               ))  # Добавляем первое дерево

while running:  # ОСНОВНОЙ ЦИКЛ
    clock.tick(FPS)  # Стабилизируем фпс
    for event in pygame.event.get():  # Проходимся по событиям (нажатиям кнопок и т.д.)
        if event.type == pygame.QUIT:  # проверить закрытие окна
            running = False  # Закрываемся

    screen.fill(BLUE)  # Заливаем всё синим цветом настроения
    print(f'Кол-во деревьев - {len(trees)}')
    for tree in trees.copy():  # Проходимся по деревьям
        tree.update()  # Обновляем каждое из них
        tree.woods_sprites.draw(screen)  # Отрисовываем древесину
        tree.cells_sprites.draw(screen)  # И клетки размножения
    for cells_to_tree in cells_to_trees.copy():  # Проходимся по будущим деревьям (падающим клеткам ныне мёртвых деревьев)
        cells_to_tree.fall()  # Вниз их сводим
    cells_to_trees_sprites.draw(screen)  # Отрисовываем клетки, которые станут растениями

    #  all_sprites.draw(screen)
    pygame.display.flip()  # Конец отрисовки
print('The end of life')  # Конец
