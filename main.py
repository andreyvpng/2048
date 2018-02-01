from random import randint
import os
import sys

def make_board(n):
    mat = []

    for i in range(n):
        mat.append([0] * n)

    return mat


def add_block(mat):
    free_blocks = []

    for i in range(len(mat)):
        for j in range(len(mat)):
            if mat[i][j] == 0:
                free_blocks.append([i, j])

    if len(free_blocks) > 0:
        x, y = free_blocks[randint(0, len(free_blocks) - 1)]
        mat[x][y] = 2


def game_status(mat):
    for i in range(len(mat)):
        for j in range(len(mat)):
            if mat[i][j] == 2048:
                return "win"

            if mat[i][j] == 0:
                return "ok"

            if i + 1 <= len(mat):
                if mat[i + 1][j] == mat[i][j]:
                    return "ok"

            if j + 1 <= len(mat):
                if mat[i][j + 1] == mat[i][j]:
                    return "ok"

    return "lose"


def print_matrix(mat):
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')
    for rows in mat:
        for item in rows:
            print(item, end = " ")
        print()
    print("\n\n")


def transpose(mat):
    new = []
    for i in range(len(mat)):
        new.append([])
        for j in range(len(mat)):
            new[i].append(mat[j][i])
    return new


def reverse(mat):
    new = []
    for i in range(len(mat)):
        new.append([])
        for j in range(len(mat[0])):
            new[i].append(mat[i][len(mat[0]) - j - 1])
    return new


def merge(mat):
    for i in range(len(mat)):
        for j in range(len(mat) - 1):
            if mat[i][j] == mat[i][j + 1] and mat[i][j] != 0:
                mat[i][j] *= 2
                mat[i][j + 1] = 0

    return mat


def cover_up(mat):
    new = make_board(len(mat))

    for i in range(len(mat)):
        count = 0
        for j in range(len(mat)):
            if mat[i][j] != 0:
                new[i][count] = mat[i][j]
                count += 1
    return new


def up(mat):
    mat = transpose(mat)
    mat = cover_up(mat)
    mat = merge(mat)
    mat = cover_up(mat)
    mat = transpose(mat)
    return mat


def down(mat):
    mat = reverse(transpose(mat))
    mat = cover_up(mat)
    mat = merge(mat)
    mat = cover_up(mat)
    mat = transpose(reverse(mat))
    return mat


def left(mat):
    mat = cover_up(mat)
    mat = merge(mat)
    mat = cover_up(mat)
    return mat


def right(mat):
    mat = reverse(mat)
    mat = cover_up(mat)
    mat = merge(mat)
    mat = cover_up(mat)
    mat = reverse(mat)
    return mat


mat = make_board(4)


if __name__ == '__main__':
    while True:
        add_block(mat)
        print_matrix(mat)
        command = input()
        if command == "w":
            mat = up(mat)
        elif command == "s":
            mat = down(mat)
        elif command == "a":
            mat = left(mat)
        elif command == "d":
            mat = right(mat)

