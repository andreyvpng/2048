from random import randint
import os
import sys


class Matrix:

    
    def __init__(self, n = 4):
        self.mat = []
        self.new_board(n)


    def new_board(self, n):
        self.mat = []

        for i in range(n):
            self.mat.append([0] * n)


    def add_block(self):
        free_blocks = []

        for i in range(len(self.mat)):
            for j in range(len(self.mat)):
                if self.mat[i][j] == 0:
                    free_blocks.append([i, j])

        if len(free_blocks) > 0:
            x, y = free_blocks[randint(0, len(free_blocks) - 1)]
            self.mat[x][y] = 2


    def game_status(self):
        for i in range(len(self.mat)):
            for j in range(len(self.mat)):
                if self.mat[i][j] == 2048:
                    return "win"

                if self.mat[i][j] == 0:
                    return "ok"

                if i + 1 <= len(self.mat):
                    if self.mat[i + 1][j] == self.mat[i][j]:
                        return "ok"

                if j + 1 <= len(self.mat):
                    if self.mat[i][j + 1] == self.mat[i][j]:
                        return "ok"

        return "lose"


    def print(self):
        if sys.platform == 'win32':
            os.system('cls')
        else:
            os.system('clear')
        for rows in self.mat:
            for item in rows:
                print(item, end = " ")
            print()
        print("\n\n")


    def transpose(self):
        new = []
        for i in range(len(self.mat)):
            new.append([])
            for j in range(len(self.mat)):
                new[i].append(self.mat[j][i])
        self.mat = new


    def reverse(self):
        new = []
        for i in range(len(self.mat)):
            new.append([])
            for j in range(len(self.mat)):
                new[i].append(self.mat[i][len(self.mat[0]) - j - 1])
        self.mat = new

    
    def merge(self):
        for i in range(len(self.mat)):
            for j in range(len(self.mat) - 1):
                if self.mat[i][j] == self.mat[i][j + 1] and self.mat[i][j] != 0:
                    self.mat[i][j] *= 2
                    self.mat[i][j + 1] = 0


    def cover_up(self):
        new = Matrix(len(self.mat))

        for i in range(len(self.mat)):
            count = 0
            for j in range(len(self.mat)):
                if self.mat[i][j] != 0:
                    new.mat[i][count] = self.mat[i][j]
                    count += 1
        self.mat = new.mat


    def up(self):
        self.transpose()
        self.cover_up()
        self.merge()
        self.cover_up()
        self.transpose()


    def down(self):
        self.transpose()
        self.reverse()
        self.cover_up()
        self.merge()
        self.cover_up()
        self.reverse()
        self.transpose()
    

    def left(self):
        self.cover_up()
        self.merge()
        self.cover_up()


    def right(self):
        self.reverse()
        self.cover_up()
        self.merge()
        self.cover_up()
        self.reverse()


mat = Matrix(5)


if __name__ == '__main__':
    while True:
        mat.add_block()
        mat.print()
        command = input()
        if command == "w":
            mat.up()
        elif command == "s":
            mat.down()
        elif command == "a":
            mat.left()
        elif command == "d":
            mat.right()

