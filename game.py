import numpy as np


class Move(object):

    def __init__(self, board, r, c, player):
        self.b = board
        self.r = r
        self.c = c
        self.player = player

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.player == other.player

    def __ne__(self, other):
        r = self.__eq__(other)
        if r is NotImplemented:
            return r
        return not r

    def __repr__(self):
        return r'<Move {},{},{}>'.format(self.b, self.r, self.c)

    def __str__(self):
        return str(self.player)


class PossibleMove(object):

    WINNING = 100  # three in a row; a win, we want this
    CLOSE = 50  # two in a row; contiguous
    LONE = 1  # single lone cell
    EMPTY = 0  # nothing

    def __init__(self, rank=0, **kwargs):
        super(PossibleMove, self).__init__(**kwargs)
        self.rank = rank

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.rank == other.rank

    def __ne__(self, other):
        r = self.__eq__(other)
        if r is NotImplemented:
            return r
        return not r

    def __lt__(self, other):
        return self.rank > other.rank

    def __gt__(self, other):
        return self.rank < other.rank


class Board(object):

    piece = {1: 'X', 2: 'O'}

<<<<<<< HEAD
    def __init__(self, player_first=True, player=1, ai=2, difficulty=3):
        self.board = self.__create_board()
        self.player_turn = True  # true if AI's turn
        self.player = player
=======
    def __init__(self, player_starts=True, player=1, ai=2):
        self.board = np.zeros(pow(3, 3), dtype=int).reshape(3, 3, 3)
        self.player_turn = player_starts  # true if AI's turn
        self.player = player  # the character for the player
>>>>>>> 76b9519bc56070bb91f1d0e2113175f4fefcbcc1
        self.ai = ai
        self.done = False

    def __create_board(self):
        '''Create board of Move objects'''
        tb = []
        for b in range(3):
            table = []
            for r in range(3):
                row = []
                for c in range(3):
                    row.append(Move(b, r, c, 0))
                table.append(row)
            tb.append(table)
        tb = np.array(tb, dtype=object)
        return tb

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
<<<<<<< HEAD
        '''Check if spot on board is open'''
        return self.board[b, r, c].player == 0

    def computer_move(self):
        '''Move based on minimax/ab check if win after'''
        raise NotImplementedError

    def move(self, b, r, c, player):
        '''Check if spot is open, after move check for wins'''
        if self.is_open(b, r, c):
            self.board[b][r][c].player = player
            # self.check_wins(player)
=======
        '''Check if location is free'''
        return self.board[b, r, c] == 0

    def move(self, b, r, c, player):
        '''Mark the specified location as taken by the player'''
        if self.is_open(b, r, c):
            self.board[b, r, c] = player
            # self.check_for_win()
>>>>>>> 76b9519bc56070bb91f1d0e2113175f4fefcbcc1
            return True
        else:
            return False

<<<<<<< HEAD
    def get_moves(self, player):
        '''Get possible moves for player and rank accordingly'''
        raise NotImplementedError

    def check_wins_for_all(self):
        '''Check wins for all players'''
        for p in Board.piece.values():
            self.check_wins(p)

    def check_wins(self, player):
        '''Check if there are any wins for the given player'''
=======
    def ai_move(self, player):
        '''Move the AI according to minimax/alpha-beta'''
        raise NotImplementedError

    def check_for_win(self):
        '''Check if any row, col, slice, or diag has all of one player'''
        raise NotImplementedError

    def get_possible_moves(self, player):
        '''Get list of possible moves, rank accordingly'''
>>>>>>> 76b9519bc56070bb91f1d0e2113175f4fefcbcc1
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
<<<<<<< HEAD
                    block = '{:>1}'.format(Board.piece[col.player]) \
                            if col.player > 0 else '-'
=======
                    block = '{:>1}'.format(Board.piece[col]) if col > 0 \
                            else '-'
>>>>>>> 76b9519bc56070bb91f1d0e2113175f4fefcbcc1
                    if c < bl:
                        rs.append(str(block) + ' | ')
                    else:
                        rs.append(str(block))
                print ''.join(rs)

    def play(self):
<<<<<<< HEAD
        '''Play the text based version'''
=======
>>>>>>> 76b9519bc56070bb91f1d0e2113175f4fefcbcc1
        while not self.done:

            # player's turn
            if self.player_turn:
                self.display()
<<<<<<< HEAD
                brc = raw_input('Your turn (b,r,c): ')
                b, r, c = map(int, brc.split(','))
                while not self.is_open(b, r, c):
                    brc = raw_input('Spot taken (b,r,c): ')
=======
                brc = raw_input('Which location? (b,r,c): ')
                b, r, c = map(int, brc.split(','))
                while not self.is_open(b, r, c):
                    brc = raw_input('Location not free (b,r,c): ')
>>>>>>> 76b9519bc56070bb91f1d0e2113175f4fefcbcc1
                    b, r, c = map(int, brc.split(','))
                self.move(b, r, c, self.player)
                self.player_turn = False
            else:
                print 'AI turn'
<<<<<<< HEAD
                # self.computer_move()
=======
>>>>>>> 76b9519bc56070bb91f1d0e2113175f4fefcbcc1
                self.player_turn = True


if __name__ == '__main__':
    b = Board()
    b._sample_moves()
    b.play()
