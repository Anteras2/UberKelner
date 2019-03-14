# kelner object

from scripts.dinning_table import *
from scripts.matrix import *
from scripts.furnace import *
from random import shuffle

class Waiter(pygame.sprite.Sprite):

    def __init__(self, x, y, num_tables, num_furnaces):

        # init graphics - do not touch!
        init_graphics(self, x, y, "waiter")

        # real coordinates of object
        self.x = x
        self.y = y

        # lists with data:
        # dishes lists
        self.orderedDishes = {}
        self.readyDishes = {}

        # objects have coordinates like in matrix (0..N, 0..N)
        ##################
        # init tables and furnaces
        # creates tables and furnaces based on random positions in the matrix
        positions = range(N)
        matrix_fields = [[posX, posY] for posX in positions for posY in positions]
        shuffle(matrix_fields)

        self.tables = []
        for i in range(num_tables):
            self.tables.append(Dinning_table(matrix_fields[i][0], matrix_fields[i][1]))
        for i in range(num_furnaces):
            self.furnaces.append(Furnace(matrix_fields[i + num_tables][0], matrix_fields[i + num_tables][1]))
        ##################
        # init restaurant map for waiter
        self.space = Matrix(N, N)

    # movement procedures
    def move_right(self):
        if self.x + 1 < N:
            self.x += 1
            self.next_round()

    def move_left(self):
        if self.x - 1 >= 0:
            self.x -= 1
            self.next_round()

    def move_down(self):
        if self.y + 1 < N:
            self.y += 1
            self.next_round()

    def move_up(self):
        if self.y - 1 >= 0:
            self.y -= 1
            self.next_round()

    def reset(self):
        # teleport waiter to the first kitchen
        self.x = self.furnaces[0].x
        self.y = self.furnaces[0].y
        self.next_round()

    def next_round(self):
        # change the environment:
        # update waiter sprite localization
        self.rect.x = self.x * blocksize
        self.rect.y = self.y * blocksize

        # update statuses of furnaces
        for furnace in self.furnaces:
            # update environment
            furnace.next_round()
            # change environment in space
            self.space.insert_object(furnace.time, furnace.y, furnace.x)

        # update statuses of tables
        for table in self.tables:
            # update environment
            table.next_round()
            # change environment in space
            self.space.insert_object(table.time, table.y, table.x)

        # show me status of simulation
        self.space.print_matrix()

    def restaurant(self):
        # example usage of matrix, for development purpose only
        self.space = Matrix(N, N)
        self.space.print_matrix()
        self.space.insert_object('asdasd', 2, 4, debug=True)
        self.space.insert_object(Matrix(2, 2, fill=5), 1, 1)
        self.space.print_matrix()
        print(self.space.objects_to_list('asdasd'))
        self.space.delete_object(1, 1, debug=True)
        self.space.print_matrix()
