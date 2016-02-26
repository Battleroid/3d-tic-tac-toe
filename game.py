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

    def __init__(self, player_starts=True, player=1, ai=2):
        self.board = np.zeros(pow(3, 3), dtype=int).reshape(3, 3, 3)
        self.player_turn = player_starts  # true if AI's turn
        self.player = player  # the character for the player
        self.ai = ai
        self.done = False

    def _sample_moves(self):
        '''Bunch of sample moves to make sure stuff works'''
        # win on board 1
        self.move(0, 0, 2, 2)
        self.move(0, 1, 1, 2)
        self.move(0, 2, 0, 2)

        # win on board 3
        self.move(2, 1, 0, 1)
        self.move(2, 1, 1, 1)
        self.move(2, 1, 2, 1)

    def is_open(self, b, r, c):
        '''Check if location is free'''
        return self.board[b, r, c] == 0

    def move(self, b, r, c, player):
        '''Mark the specified location as taken by the player'''
        if self.is_open(b, r, c):
            self.board[b, r, c] = player
            # self.check_for_win()
            return True
        else:
            return False

    def ai_move(self, player):
        '''Move the AI according to minimax/alpha-beta'''
        raise NotImplementedError

    def check_for_win(self):
        '''Check if any row, col, slice, or diag has all of one player'''
        raise NotImplementedError

    def get_possible_moves(self, player):
        '''Get list of possible moves, rank accordingly'''
        raise NotImplementedError
        # 1. rows, cols, and diags for each table
        # 2. vertical cols
        # 3. for each horizontal vert slice check diags
        # 4. for each vertical slice check diags
        # 5. finally check 3D across entire array

    def display(self):
        '''Only for basic text input at the moment'''
        bl = len(self.board[0]) - 1
        for t, table in enumerate(self.board):
            print 'Board', t + 1
            for r, row in enumerate(table):
                rs = []
                for c, col in enumerate(row):
                    block = '{:>1}'.format(Board.piece[col]) if col > 0 \
                            else '-'
                    if c < bl:
                        rs.append(str(block) + ' | ')
                    else:
                        rs.append(str(block))
                print ''.join(rs)

    def play(self):
        while not self.done:

            # player's turn
            if self.player_turn:
                self.display()
                brc = raw_input('Which location? (b,r,c): ')
                b, r, c = map(int, brc.split(','))
                while not self.is_open(b, r, c):
                    brc = raw_input('Location not free (b,r,c): ')
                    b, r, c = map(int, brc.split(','))
                self.move(b, r, c, self.player)
                self.player_turn = False
            else:
                print 'AI turn'
                self.player_turn = True


if __name__ == '__main__':
    b = Board()
    b._sample_moves()
    b.play()
