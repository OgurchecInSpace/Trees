# Деревья
import random as rm
import pygame
import pprint as pp

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

cells_woods = set()
all_sprites = pygame.sprite.Group()


class Cell(pygame.sprite.Sprite):
    def __init__(self, num, x, y, parent, gene=0):
        self.gene = gene
        pygame.sprite.Sprite.__init__(self)
        all_sprites.add(self)
        parent.cells_sprites.add(self)

        self.num = num
        self.x = x
        self.y = y
        self.parent = parent

        self.image = pygame.Surface((SIZE, SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        cells_woods.add((self.x, self.y))

    def __repr__(self):
        return f'Клекта размножения {self.num}. X = {self.x}, Y = {self.y}'


class Wood(pygame.sprite.Sprite):  # Часть дерева (древесина)
    def __init__(self, num, x, y, parent):
        pygame.sprite.Sprite.__init__(self)
        all_sprites.add(self)
        parent.woods_sprites.add(self)
        self.num = num
        self.x = x
        self.y = y
        self.parent = parent

        self.image = pygame.Surface((SIZE, SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        cells_woods.add((self.x, self.y))

    def __repr__(self):
        return f'Древесина {self.num}. X = {self.x}, Y = {self.y}'
    def get_energy(self):  #  получение энергии из клетки
        if len(cells_woods) > 3:
            num = 3
        else:
            num = len(cells_woods) + 1
        top = sorted(cells_woods, key=lambda coords: coords[1], reverse=True)[0:num]
        if (self.x, self.y) in top:
            position = top.index((self.x, self.y)) + 1
            energy = HEIGHT - (self.y / SIZE) * position
            return energy
        return 0

class Tree:  # Дерево
    def __init__(self, name, x, y, genome=None):
        self.cells_sprites = pygame.sprite.Group()
        self.woods_sprites = pygame.sprite.Group()
        self.name = name
        self.num = 0
        self.x = x
        self.y = y
        if genome is None:
            self.genome = [
                {'left': int(rm.randrange(0, 31)),
                 'up': int(rm.randrange(0, 31)),
                 'right': int(rm.randrange(0, 31)),
                 'down': int(rm.randrange(0, 31))} for _ in range(16)
            ]
        else:
            self.genome = genome
        if not rm.randrange(0, 4):
            direction = rm.choice(('left', 'up', 'right', 'down'))
            self.genome[rm.randrange(0, 16)][direction] = rm.randrange(0, 31)
        self.cells = {Cell(0, x, y, self)}
        self.woods = {Wood(0, x, y, self)}

    def __repr__(self):
        return f'Дерево {self.name}. X {self.x}, Y {self.y}'

    def end(self):
        print('end')
        self.woods = set()
        for cell in self.cells:
            cell.parent = None
        self.woods_sprites = pygame.sprite.Group()
        self.cells_sprites = pygame.sprite.Group()
        trees.remove(self)


    def update(self):
        new_cells = set()
        energy = 0
        for wood in self.woods:
            cells_woods.add((wood.x, wood.y))
            energy += wood.get_energy()
        if energy / (len(self.cells) + len(self.woods)) >= ENERGY_ON_CELL:
            print(f'Энергия - {energy / (len(self.cells) + len(self.woods))}')
            for cell in self.cells:
                cells_woods.add((cell.x, cell.y))

                if cell.gene <= 15:
                    for direction, gene in self.genome[cell.gene].items():
                        if direction == 'left' and (cell.x - SIZE, cell.y) not in cells_woods and cell.x - SIZE > SIZE:
                            new_cells.add(Cell(len(self.cells), cell.x - SIZE, cell.y, self, gene=gene))

                        elif direction == 'up' and (cell.x, cell.y - SIZE) not in cells_woods and cell.y - SIZE > SIZE:
                            new_cells.add(Cell(len(self.cells), cell.x, cell.y - SIZE, self, gene=gene))

                        elif direction == 'right' and (cell.x + SIZE, cell.y) not in cells_woods and cell.x + SIZE < WIDTH - SIZE:
                            new_cells.add(Cell(len(self.cells), cell.x - SIZE, cell.y, self, gene=gene))

                        elif direction == 'down' and (cell.x, cell.y + SIZE) not in cells_woods and cell.y + SIZE < HEIGHT - SIZE:
                            new_cells.add(Cell(len(self.cells), cell.x, cell.y + SIZE, self, gene=gene))
                cell.kill()
                cells_woods.remove((cell.x, cell.y))

                self.woods.add(Wood(len(self.woods), cell.x, cell.y, self))
            self.cells = new_cells
            if len(self.cells) == 0:
                print('Клетки размножения кончились')
                self.end()
                print('----')
        else:
            print('Энергия кончилась')
            self.end()
            print('----')



pygame.init()  # инициализация всего интерфейса
pygame.mixer.init()  # для звука
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # pygame.RESIZABLE)  # окно
pygame.display.set_caption("Trees")  # имя окна
clock = pygame.time.Clock()  # Время
running = True

trees = set()
trees.add(Tree('fsdkdskfsd', WIDTH / 2, HEIGHT * 0.9))
trees.add(Tree('первое', 0, 0))
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # проверить закрытие окна
            running = False

    screen.fill(BLUE)
    for tree in trees.copy():
        if not tree.name == 'первое':
            tree.update()
            tree.woods_sprites.draw(screen)
            tree.cells_sprites.draw(screen)
    #all_sprites.draw(screen)
    pygame.display.flip()
print('The end of life')