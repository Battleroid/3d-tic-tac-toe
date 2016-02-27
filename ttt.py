from copy import deepcopy
from colorama import Back, Style, Fore


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
        self.board = Board.create_board()      # 3x3 grid for playing
        self.allowed_moves = set(range(pow(3, 3)))  # 27 available positions
        self.difficulty = ply                  # 'difficulty'; game tree depth
        self.human_turn = player_first         # human moves first toggle
        self.human = human                     # character for human
        self.ai = ai                           # character for ai
        self.players = (human, ai)             # tuple of both characters

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

    def get_moves_by_combination(self, player):
        moves = []
        for combo in self.winning_combos:
            move = []
            for cell in combo:
                b, r, c = self.find(self.board, cell)
                if self.board[b][r][c] == player:
                    move += [cell]
            moves += [move]
        return moves

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
        return list(self.allowed_moves) + self.get_moves(player)

    @property
    def complete(self):
        for player in self.players:
            for combo in self.winning_combos:
                combo_avail = True
                for pos in combo:
                    if pos not in self.available_combos(player):
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
        return self.complete and self.winner is None

    # @property
    # def heuristic(self):
    #     # TODO: need blocking heuristic for ai to block human wins
    #     if self.human_won:
    #         return -100
    #     elif self.tied:
    #         return 0
    #     elif self.ai_won:
    #         return 100
    #     else:
    #         return self.simple_heuristic

    @property
    def simple_heuristic(self):
        return self.check_available(self.ai) - self.check_available(self.human)

    def check_available(self, player):
        wins = 0
        table = [0 for x in range(27)]
        cnt = 0

        # create table of winning combinations
        for i in range(3):
            for x in range(3):
                for y in range(3):
                    if self.board[i][x][y] == player or \
                            self.board[i][x][y] != self.get_enemy(player):
                        table[cnt] = 1
                    cnt += 1

        # get total winning spots for given player
        for i in range(len(self.winning_combos)):
            cnt = 0
            for j in range(3):
                if table[self.winning_combos[i][j]] == 1:
                    cnt += 1
                    if cnt == 3:
                        wins += 1
        return wins

    # def minimax(self, node, player, ply):
    #     '''Minimax for node evaluation'''
    #     if node.complete or ply == 0:
    #         return node.heuristic
    #     a = -1e10000
    #     for move in node.allowed_moves:
    #         child = deepcopy(node)
    #         child.move(move, player)
    #         a = max([a, -self.minimax(child, self.get_enemy(player), ply - 1)])
    #     return a

    # def think(self, ply):
    #     '''Uses minimax to establish the best move with the given ply'''
    #     best_move = None
    #     best_score = -1e10000

    #     # find the best move of the available moves on the board using the 
    #     # minimax method for each child node of the move
    #     for move in self.allowed_moves:
    #         score = self.minimax(self, self.ai, ply)
    #         if score > best_score:
    #             best_move = move
    #             best_score = score

    #     print 'I think we\'ll go to', best_move
    #     self.move(best_move, self.ai)

    # def computers_turn(self):
    #     best_score = -1000
    #     best_move = -1
    #     hval = 0

    #     for move in self.allowed_moves:
    #         # first check if the move results in a win for the AI
    #         dummy = deepcopy(self)
    #         dummy.move(move, self.ai)
    #         if dummy.complete and dummy.winner == self.ai:
    #             self.move(move, self.ai)
    #             print 'Game over!'
    #             break
    #         else:
    #             # first move was not a win, generate game tree for this cell
    #             dummy = deepcopy(self)
    #             hval = self.think_ahead(dummy, self.human, -1000, 1000)
    #         if hval >= best_score:
    #             best_score = hval
    #             best_move = move

    #     # did not reach win condition, instead use best move
    #     self.move(best_move, self.ai)
    #     # TODO: toggle human turn for play

    # TODO: do I really need to make copies of copies? probably really stupid
    # def think_ahead(self, node, player, alpha, beta, ply=None):
    #     if not ply:
    #         ply = self.difficulty  # use default ply (3) if no ply specified
    #     if ply == -1:
    #         return self.simple_heuristic  # reached depth
    #     if player == self.ai:
    #         hval = 0
    #         for move in node.allowed_moves:
    #             dummy = deepcopy(node)
    #             dummy.move(move, dummy.ai)
    #             if dummy.complete and dummy.winner == self.ai:
    #                 return 1000
    #             else:
    #                 dummy = deepcopy(node)
    #                 hval = self.think_ahead(dummy, self.human, alpha, beta, ply - 1)
    #                 if hval > alpha:
    #                     alpha = hval
    #             if alpha >= beta:
    #                 break
    #         return alpha
    #     else:
    #         hval = 0
    #         for move in node.allowed_moves:
    #             dummy = deepcopy(node)
    #             dummy.move(move, dummy.human)
    #             if dummy.complete and dummy.winner == self.human:
    #                 return -1000
    #             else:
    #                 dummy = deepcopy(node)
    #                 hval = self.think_ahead(dummy, self.ai, alpha, beta, ply - 1)
    #                 if hval < beta:
    #                     beta = hval
    #             if alpha >= beta:
    #                 break
    #         return beta
    
    def computers_turn(self):
        best_score = -1000
        best_move = -1
        hval = 0

        for move in self.allowed_moves:
            self.move(move, self.ai)
            self.display()
            print 'Moving to', move
            print 'hval is', hval
            print 'best_score', best_score
            print 'best_move is', best_move
            if self.complete and self.winner == self.ai:
                print 'Done'
                break
            else:
                print 'Move', move, 'was not a winner'
                hval = self.think_ahead(self.human, -1000, 1000, self.difficulty)
                if hval >= best_score:
                    best_score = hval
                    best_move = move
                self.undo_move(move)

        print 'Next best move is', best_move
        self.move(best_move, self.ai)

    def think_ahead(self, player, alpha, beta, ply=None):
        if not ply:
            ply = self.difficulty
        # if ply == -1:
        #     print 'Reached depth, returning', self.simple_heuristic
        #     return self.simple_heuristic
        print 'Simple heuristic is:', self.simple_heuristic
        ply -= 1
        print 'PLY IS', ply
        if ply > 0:
            if player == self.ai:
                # alpha portion
                print 'Alpha for AI'
                hval = 0
                for move in self.allowed_moves:
                    self.move(move, self.ai)
                    if self.complete and self.winner == self.ai:
                        print 'Winning move for AI', move
                        self.undo_move(move)
                        return 1000
                    else:
                        hval = self.think_ahead(self.human, alpha, beta, ply)
                        if hval > alpha:
                            alpha = hval
                        self.undo_move(move)
                    if alpha >= beta:
                        break
                return alpha
            else:
                # beta portion
                print 'Beta for Human'
                hval = 0
                for move in self.allowed_moves:
                    self.move(move, self.human)
                    if self.complete and self.winner == self.human:
                        print 'Winning move for Human', move
                        self.undo_move(move)
                        return -1000
                    else:
                        hval = self.think_ahead(self.ai, alpha, beta, ply)
                        if hval < beta:
                            beta = hval
                        self.undo_move(move)
                    if alpha >= beta:
                        break
                return beta
        else:
            return self.simple_heuristic

    def undo_move(self, position):
        self.allowed_moves.add(position)
        i, x, y = self.find(self.board, position)
        self.board[i][x][y] = position

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
            print '{}{}Board #{}{}'.format(Back.WHITE, Fore.BLACK, i + 1, \
                    Style.RESET_ALL)
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
    b.move(0, b.ai)
    b.move(2, b.human)
    b.move(26, b.ai)
    b.display()
    b.computers_turn()
