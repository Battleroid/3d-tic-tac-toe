from copy import deepcopy
from colorama import Back, Style


class Board(object):

    winning_combos = (
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
    )

    def __init__(self, player_first=True, human='X', ai='O', ply=3):
        self.board = Board.create_board()     # 3x3 grid for playing
        self.allowed_moves = range(pow(3, 3)) # 27 available positions
        self.difficulty = ply                 # 'difficulty'; game tree depth
        self.human_turn = player_first        # human moves first toggle
        self.human = human                    # character for human
        self.ai = ai                          # character for ai
        self.players = (human, ai)            # tuple of both characters

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

    @staticmethod
    def create_board():
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

    def get_moves(self, player):
        moves = []
        cnt = 0
        for i in range(3):
            for x in range(3):
                for y in range(3):
                    if self.board[i][x][y] == player:
                        moves += [cnt]
                    cnt += 1
        return moves

    def available_combos(self, player):
        return self.allowed_moves + self.get_moves(player)

    @property
    def complete(self):
        for player in self.players:
            for combo in self.winning_combos:
                combo_avail = True
                for pos in combo:
                    if not pos in self.available_combos(player):
                        combo_avail = False
                if combo_avail:
                    return self.winner is not None
        return True

    @property
    def winning_combo(self):
        if self.winner:
            positions = self.get_moves(self.winner)
            for combo in self.winning_combos:
                winner = combo
                for pos in combo:
                    if pos not in positions:
                        winner = None
                if winner:
                    return winner
        return None

    @property
    def winner(self):
        for player in self.players:
            positions = self.get_moves(player)
            for combo in self.winning_combos:
                won = True
                for pos in combo:
                    if pos not in positions:
                        won = False
                if won:
                    return player
        return None

    @property
    def ai_won(self):
        return self.winner == self.ai

    @property
    def human_won(self):
        return self.winner == self.human

    @property
    def tied(self):
        return self.complete == True and self.winner is None

    @property
    def heuristic(self):
        if self.human_won:
            return -10
        elif self.tied:
            return 0
        elif self.ai_won:
            return 10
        else:
            return 0
        # TODO: need blocking heuristic for ai to block human wins
        # TODO: need 3-in-row and 2-in-row and single cell heuristics

    def minimax(self, node, player, ply, a=-1e10000):
        if node.complete or ply == 0:
            return node.heuristic
        for move in node.allowed_moves:
            child = deepcopy(node)
            child.move(move, player)
            o = -self.minimax(child, self.get_enemy(player), ply - 1, a)
            a = max(a, o)
        return a

    def think(self, ply):
        raise NotImplementedError

    def move(self, position, player):
        self.allowed_moves.remove(position)
        i, x, y = self.find(self.board, position)
        self.board[i][x][y] = player

    def get_enemy(self, player):
        if player == self.human:
            return self.ai
        else:
            return self.human

    def display(self):
        cnt = 0
        for i, bd in enumerate(self.board):
            print 'Board {:>2}'.format(i + 1)
            for line in bd:
                larr = []
                for cell in line:
                    bg = Back.RED
                    if self.winner and cnt in self.winning_combo:
                        bg = Back.BLUE
                    if cell in self.players:
                        s = '{}{:>2}{}'.format(bg, cell * 2, Style.RESET_ALL)
                    else:
                        s = '{:>2}'.format(cell)
                    larr += [s]
                    cnt += 1
                print ' '.join(larr)


if __name__ == '__main__':
    b = Board()
    b.move(0, b.human)
    b.move(26, b.human)
    b.move(20, b.ai)
    if b.complete:
        print b.winner, b.winning_combo
    print b.minimax(b, b.ai, 3)
