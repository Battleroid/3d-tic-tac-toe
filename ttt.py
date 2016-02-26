from copy import deepcopy
from colorama import Back, Style


class Cell(object):
    def __init__(self, player=None):
        self.player = player

    @property
    def empty(self):
        return self.player is None


class Board(object):

    winning_combos = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14],
        [15, 16, 17], [18, 19, 20], [21, 22, 23], [24, 25, 26],

        [0, 3, 6], [1, 4, 7], [2, 5, 8], [9, 12, 15], [10, 13, 16],
        [11, 14, 17], [18, 21, 24], [19, 22, 25], [20, 23, 26],

        [0, 4, 8], [2, 4, 6], [9, 13, 17], [11, 13, 15], [18, 22, 26],
        [20, 22, 24],

        [0, 9, 18], [1, 10, 19], [2, 11, 20], [3, 12, 21], [4, 13, 22],
        [5, 14, 23], [6, 15, 24], [7, 16, 25], [8, 17, 26],

        [0, 12, 24], [1, 13, 25], [2, 14, 26], [6, 12, 18], [7, 13, 19],
        [8, 14, 20], [0, 10, 20], [3, 13, 23], [6, 16, 26], [2, 10, 18],
        [5, 13, 21], [8, 16, 24], [0, 13, 26], [2, 13, 24], [6, 13, 20],
        [8, 13, 18]
    ]

    def __init__(self, player_first=True, human='X', ai='O', ply=3):
        self.board = self.__create_board()  # 3x3 grid for playing
        self.allowed_moves = range(pow(3, 3))  # 27 available positions
        self.human_turn = player_first
        self.human = human
        self.ai = ai
        self.players = (human, ai)
        self.difficulty = ply

    def find(self, arr, key):
        cnt = 0
        for i in range(3):
            for x in range(3):
                for y in range(3):
                    if cnt == key:
                        return (i, x, y)
                    cnt += 1

    def find_combo(self, combo):
        s, m, e = combo
        s = self.find(self.board, s)
        m = self.find(self.board, m)
        e = self.find(self.board, e)
        return s, m, e

    def __create_board(self):
        cnt = 0
        board = []
        for i in range(3):
            bt = []
            for x in range(3):
                rt = []
                for y in range(3):
                    rt.append(cnt)
                    cnt += 1
                bt.append(rt)
            board.append(bt)
        return board

    def check_wins(self):
        for combo in self.winning_combos:
            s, m, e = self.find_combo(combo)
            b, r, c = s, m, e
            s = self.board[s[0]][s[1]][s[2]]
            m = self.board[m[0]][m[1]][m[2]]
            e = self.board[e[0]][e[1]][e[2]]
            if all(i == s for i in (s, m, e)):
                return b, r, c  # return coords of winning combination
        return False  # no winning combinations found

    def move(self, position, player, board=None, allowed_moves=None):
        if not board:
            board = self.board
        if not allowed_moves:
            allowed_moves = self.allowed_moves
        if position in allowed_moves:
            allowed_moves.remove(position)
            i, x, y = self.find(board, position)
            board[i][x][y] = player
            return True
        return False  # no positions left

    def think(self, ply, player):
        dummy_moves = deepcopy(self.allowed_moves)  # copy of current allowed moves
        dummy = deepcopy(self.board)  # copy of board for use in finding best move

        def minimax(ply=ply, player=player, board=dummy):
            pass

        # eventually return best possible move for AI
        self.move(5, self.ai, dummy, dummy_moves)
        self.display(dummy)

    def human_move(self, board):
        raise NotImplementedError

    def computer_move(self, board):
        raise NotImplementedError

    def display(self, board=None):
        if not board:
            board = self.board
        for i, bd in enumerate(board):
            print 'Board {:>2}'.format(i + 1)
            for line in bd:
                print ' '.join('{}'.format('{}{:>2}{}'.format(Back.RED, x, Style.RESET_ALL)) if x in self.players else '{:>2}'.format(x) for x in map(str, line))  # basically a red bg if a player has moved there


if __name__ == '__main__':
    b = Board()
    b.move(0, b.human)
    b.move(13, b.human)
    b.think(3, b.human)
    b.display()
