from tkinter import *
from random import randint
import os
import sys

SIZE = 500
GRID_LEN = 4
GRID_PADDING = 10

FONT = ("Verdana", 40, "bold")

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"

BACKGROUND_COLOR_DICT = {2: "#eee4da",
                         4: "#ede0c8",
                         8: "#f2b179",
                         16: "#f59563",
                         32: "#f67c5f",
                         64: "#f65e3b",
                         128: "#edcf72",
                         256: "#edcc61",
                         512: "#edc850",
                         1024: "#edc53f",
                         2048: "#edc22e"}

CELL_COLOR_DICT = {2: "#776e65",
                   4: "#776e65",
                   8: "#f9f6f2",
                   16: "#f9f6f2",
                   32: "#f9f6f2",
                   64: "#f9f6f2",
                   128: "#f9f6f2",
                   256: "#f9f6f2",
                   512: "#f9f6f2",
                   1024: "#f9f6f2",
                   2048: "#f9f6f2"}


class Matrix:

    def __init__(self, n=4):
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
            chance_of_4 = randint(1, 100)
            self.mat[x][y] = 2 + 2 * (chance_of_4 >= 90)

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
                print(item, end=" ")
            print()
        print("\n\n")

    def len(self):
        return len(self.mat)

    def get_num(self, i, j):
        return self.mat[i][j]

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
        done = False
        for i in range(len(self.mat)):
            for j in range(len(self.mat) - 1):
                if self.mat[i][j] == self.mat[i][j + 1] and self.mat[i][j] != 0:
                    self.mat[i][j] *= 2
                    self.mat[i][j + 1] = 0
                    done = True
        return done

    def cover_up(self):
        new = Matrix(len(self.mat))
        done = False

        for i in range(len(self.mat)):
            count = 0
            for j in range(len(self.mat)):
                if self.mat[i][j] != 0:
                    new.mat[i][count] = self.mat[i][j]
                    count += 1
                    done = True
        self.mat = new.mat
        return done

    def up(self):
        self.transpose()
        done = self.cover_up() | self.merge() | self.cover_up()
        self.transpose()
        return done

    def down(self):
        self.transpose()
        self.reverse()
        done = self.cover_up() | self.merge() | self.cover_up()
        self.reverse()
        self.transpose()
        return done

    def left(self):
        done = self.cover_up() | self.merge() | self.cover_up()
        return done

    def right(self):
        self.reverse()
        done = self.cover_up() | self.merge() | self.cover_up()
        self.reverse()
        return done


class App:

    def __init__(self, n):
        self.N = int(n)

        self.root = Tk()
        self.root.resizable(width=False, height=False)
        self.root.title('2048')
        self.root.bind('<Key>', self.key_down)
        self.commands = {'w': Matrix.up,
                         's': Matrix.down,
                         'a': Matrix.left,
                         'd': Matrix.right}

        self.mat = []
        self.grid = []
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()
        self.root.mainloop()

    def init_grid(self):
        background = Frame(bg=BACKGROUND_COLOR_GAME, width=SIZE / GRID_LEN, height=SIZE / GRID_LEN)
        background.grid()
        self.grid = []
        for i in range(self.N):
            grid_row = []
            for j in range(self.N):
                block = Frame(bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE / GRID_LEN, height=SIZE / GRID_LEN)
                block.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                label = Label(master=block, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=4,
                              height=2)
                label.grid()
                grid_row.append(label)
            self.grid.append(grid_row)

    def init_matrix(self):
        self.mat = Matrix(self.N)
        self.mat.add_block()
        self.mat.add_block()

    def update_grid_cells(self):
        for i in range(self.N):
            for j in range(self.N):
                new_number = self.mat.get_num(i, j)
                if new_number == 0:
                    self.grid[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid[i][j].configure(text=str(new_number), bg=BACKGROUND_COLOR_DICT[new_number],
                                              fg=CELL_COLOR_DICT[new_number])

    def key_down(self, event):
        if event.char in self.commands:
            if self.commands[event.char](self.mat):
                self.mat.add_block()
            self.update_grid_cells()


if __name__ == '__main__':
    App(4)
