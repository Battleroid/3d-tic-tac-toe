import numpy as np


class Pos(object):

    def __init__(self, board, r, c, player):
        self.b = board
        self.r = r
        self.c = c
        self.player = player

    def __eq__(self, other):
        if isinstance(other, Pos):
            return self.player == other.player

    def __ne__(self, other):
        r = self.__eq__(other)
        if r is NotImplemented:
            return r
        return not r

    def __str__(self):
        return self.player


class Board(object):

    piece = {1: 'X', 2: 'O'}

    def __init__(self):
        self.board = np.zeros(pow(3, 3), dtype=int).reshape(3, 3, 3)
        self.turn = True  # true if AI's turn
        self.done = False

    def _sample_moves(self):
        # win on board 1
        self.move(0, 0, 2, 2)
        self.move(0, 1, 1, 2)
        self.move(0, 2, 0, 2)

        # win on board 3
        self.move(2, 1, 0, 1)
        self.move(2, 1, 1, 1)
        self.move(2, 1, 2, 1)

    def _open(self, b, r, c):
        return self.board[b, r, c] == 0

    def move(self, b, r, c, player):
        if self._open(b, r, c):
            self.board[b, r, c] = player
            return True
        else:
            return False

    def check_wins(self, player):
        # bl = len(self.board)

        # rows
        def rows(arr):
            pass

        # cols
        def cols(arr):
            pass

        # diagonals in 2D
        def diag(arr):
            pass

        # horizontal columns in 3D
        def hslice():
            pass

        # vertical columns in 3D
        def vslice():
            pass

        # cross diagonals in 3D (through center)
        def cross():
            pass

        # 1. rows, cols, and diags for each table
        # 2. vertical cols
        # 3. for each horizontal vert slice check diags
        # 4. for each vertical slice check diags
        # 5. finally check 3D across entire array

    def display(self):
        dummy = np.concatenate(
            [[np.arange(9, dtype=int).reshape(3, 3)] for _ in range(3)])
        bl = len(self.board[0]) - 1
        for t, table in enumerate(self.board):
            print 'Board', t + 1
            for r, row in enumerate(table):
                rs = []
                for c, col in enumerate(row):
                    block = '{:>1}'.format(Board.piece[col]) if col > 0 \
                            else '{:1d}'.format(dummy[t, r, c])
                    if c < bl:
                        rs.append(str(block) + ' | ')
                    else:
                        rs.append(str(block))
                print ''.join(rs)


if __name__ == '__main__':
    b = Board()
    b._sample_moves()
    b.display()
