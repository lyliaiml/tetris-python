import random
from figure import Figure
from config import colors


class Tetris:

    def __init__(self, height, width):

        self.height = height
        self.width = width

        self.field = []

        self.score = 0
        self.state = "start"

        self.x = 100
        self.y = 60

        self.zoom = 20

        self.figure = None

        # système 7-bag
        self.bag = []

        # création grille vide
        for i in range(height):
            self.field.append([0 for _ in range(width)])

    # 7-BAG

    def get_new_piece(self):

        if len(self.bag) == 0:

            self.bag = [0, 1, 2, 3, 4, 5, 6]

            random.shuffle(self.bag)

        return self.bag.pop()

    #NOUVELLE PIÈCE

    def new_figure(self):

        piece_type = self.get_new_piece()

        self.figure = Figure(3, 0, piece_type)

    #  COLLISIONS 

    def intersects(self):

        for i in range(4):

            for j in range(4):

                if i * 4 + j in self.figure.image():

                    # limites grille
                    if (
                        i + self.figure.y >= self.height
                        or j + self.figure.x >= self.width
                        or j + self.figure.x < 0
                        or i + self.figure.y < 0
                    ):
                        return True

                    # collision blocs
                    if self.field[i + self.figure.y][j + self.figure.x] > 0:
                        return True

        return False

    # SUPPRESSION LIGNES

    def break_lines(self):

        lines = 0

        for i in range(1, self.height):

            if 0 not in self.field[i]:

                lines += 1

                for k in range(i, 1, -1):

                    self.field[k] = self.field[k - 1][:]

        # score amélioré
        self.score += (lines ** 2) * 10

    # FIXER PIÈCE

    def freeze(self):

        for i in range(4):

            for j in range(4):

                if i * 4 + j in self.figure.image():

                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color

        self.break_lines()

        self.new_figure()

        if self.intersects():

            self.state = "gameover"

    #  DROP INSTANTANÉ

    def go_space(self):

        while not self.intersects():

            self.figure.y += 1

        self.figure.y -= 1

        self.freeze()

    #  DESCENTE 

    def go_down(self):

        self.figure.y += 1

        if self.intersects():

            self.figure.y -= 1

            self.freeze()

    

    def go_side(self, dx):

        old_x = self.figure.x

        self.figure.x += dx

        if self.intersects():

            self.figure.x = old_x

    

    def rotate(self):

        old_rotation = self.figure.rotation

        self.figure.rotate()

        if self.intersects():

            self.figure.rotation = old_rotation
