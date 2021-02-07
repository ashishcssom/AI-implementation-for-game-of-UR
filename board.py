""" 
Board design
------------

                                                  Player 1
                                            ⦶,⦶,⦶,⦶,⦶,⦶,⦶

                                    [[✪],[ ],[ ],[ ],[⬜],[⬜],[ ],[✪]]
                                    [[ ],[ ],[ ],[✪],[  ] ,[  ],[ ],[ ]]
                                    [[✪],[ ],[ ],[ ],[⬜],[⬜],[ ],[✪]]

                                            ⦵,⦵,⦵,⦵,⦵,⦵,⦵
                                                  Player 2

Co-ordinate information
-----------------------
[[(0,2)],[(1,2)],[(2,2)],[(3,2)],[( , )],[( , )],[(6,2)],[(7,2)]] # Player 1
[[(0,1)],[(1,1)],[(2,1)],[(3,1)],[(4,1)],[(5,1)],[(6,1)],[(7,1)]] # Common path
[[(0,0)],[(1,0)],[(2,0)],[(3,0)],[( , )],[( , )],[(6,0)],[(7,0)]] # Player 2

"""

class Board(object):
    """docstring for Board"""
    MAX_PIECES = 7
    DUAL_CHANCE = [[0, 0],[0, 2],[3, 1],[7, 0],[7, 2]] 
    COMMON_PATH = [[0, 1], [1, 1], [2, 1],[3, 1],[4, 1],[5, 1], [6, 1], [ 7, 1]] 
    PATHS = [[[3, 0], [2, 0], [1, 0], [0, 0]] +COMMON_PATH + [[7, 0], [6, 0]],[[3, 2], [2, 2], [1, 2], [0, 2]] +COMMON_PATH + [[7, 2], [6, 2]]] 

    def __init__(self):
        self.setBoard()
        self.setPlayers()

    def setBoard(self):
        self.board = [
            [['xx'], ['--'], ['xx']],
            [['--'], ['--'], ['--']],
            [['--'], ['--'], ['--']],
            [['s1'], ['xx'], ['s2']],
            [None, ['--'], None],
            [None, ['--'], None],
            [['--'], ['--'], ['--']],
            [['xx'], ['--'], ['xx']],
        ]

    def setPlayers(self):
        self.p1 = 'A'
        self.p2 = 'B'
        self.p1Pieces = ['A' + str(x) for x in range(0, self.MAX_PIECES)] # ['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6']
        self.p2Pieces = ['B' + str(x) for x in range(0, self.MAX_PIECES)] # ['B0', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6']
        self.p1Path = self.PATHS[0] # [[3, 0],[2, 0],[1, 0],[0, 0],[0, 1],[1, 1],[2, 1],[3, 1],[4, 1],[5, 1],[6, 1],[7, 1],[7, 0],[6, 0]]
        self.p2Path = self.PATHS[1] # [[3, 2],[2, 2],[1, 2],[0, 2],[0, 1],[1, 1],[2, 1],[3, 1],[4, 1],[5, 1],[6, 1],[7, 1],[7, 2],[6, 2]]
        self.piecesPosition = dict((el, -1) for el in self.p1Pieces + self.p2Pieces) # {'A0': -1,'A1': -1,'A2': -1,'A3': -1,'A4': -1,'A5': -1,'A6': -1,'B0': -1,'B1': -1,'B2': -1,'B3': -1,'B4': -1,'B5': -1,'B6': -1}

    def isCellEmpty(self, coord):
        """ To check whether the position is empy or not """
        return len(self.board[coord[0]][coord[1]]) == 0

    def isOccupied(self, position):
        """ To check whether the position is occupied or not """
        for pidO, positionO in self.piecesPosition.items():
            if positionO != position:
                continue
            (playerO, piece, pieces, path) = self.idByPiece(pidO)
            return (True, pidO, playerO)
        return (False, None, None)

    def fillBoard(self):
        """ Fill the board with proper token """
        self.setBoard()
        for pid, position in self.piecesPosition.items():
            if position < 0:
                continue
            (player, piece, pieces, path) = self.idByPiece(pid) # pid-->'B6' ,player-->B, piece-->6, pieces-->p2Pieces,path-->p2Path
            if position >= len(path):
                continue
            coords = path[position]
            self.board[coords[0]][coords[1]] = [pid] # To put players token in the cell

    def idByPiece(self, pid):
        """ To return player, token number, piece and the path """
        pl = pid[0]
        pi = pid[1]
        if pl == self.p1:
            return (pl, pi, self.p1Pieces, self.p1Path)
        if pl == self.p2:
            return (pl, pi, self.p2Pieces, self.p2Path)
        return (None, None, None, None)

    def movePiece(self, pid, step):
        """ Piece moving algorithm """
        (player, piece, pieces, path) = self.idByPiece(pid)
        curPosition = self.piecesPosition[pid]
        kill = ''
        completed = ''
        if curPosition + step < len(path):
            (occupied, pidO, playerO) = self.isOccupied(curPosition + step)
            if occupied and (playerO == player):
                return (curPosition, curPosition, kill, completed)
            elif occupied and (path[curPosition + step] in self.DUAL_CHANCE):
                if (path[curPosition + step] in self.COMMON_PATH):
                    return (curPosition, curPosition, kill, completed)
                self.piecesPosition[pid] = curPosition + step
            elif occupied and (path[curPosition + step] in self.COMMON_PATH):
                self.removePiece(pidO, curPosition + step)
                kill = pidO
                self.piecesPosition[pid] = curPosition + step
            else:
                self.piecesPosition[pid] = curPosition + step
            self.fillBoard()
            return (curPosition, curPosition + step, kill, completed)
        elif curPosition + step == len(path):
            self.piecesPosition[pid] = curPosition + step
            completed = pid
            self.fillBoard()
            return (curPosition, curPosition + step, kill, completed)
        else:
            return (curPosition, curPosition, kill, completed)

    def removePiece(self, pidO, position):
        """ To remove the piece frm board """
        self.piecesPosition[pidO] = -1

    def printer(self):
        """ To print the board """
        pstr = ""
        for row in self.board:
            for ele in row:
                if ele is None:
                    pstr += '       '
                else:
                    pstr += '|-' + str(ele[0]) + '-| '
            pstr += "   \r\n"
        print(pstr)

    def isCompleted(self):
        """ To check player finshed or not """
        p1Movables = self.MAX_PIECES
        p2Movables = self.MAX_PIECES
        for pid, position in self.piecesPosition.items():
            if position < len(self.PATHS[0]):
                continue
            (player, piece, pieces, path) = self.idByPiece(pid)
            if player == self.p1:
                p1Movables -= 1
            if player == self.p2:
                p2Movables -= 1
        if p1Movables == 0:
            return (True, self.p1)
        if p2Movables == 0:
            return (True, self.p2)
        return (False, None)

    def isPieceFinished(self, piece, path):
        """ To check piece is finished or not """
        return self.piecesPosition[piece] == len(path)

    def isPieceDualChance(self, piece, path):
        """ To check the whether the piece deserve dual chance for rolling dice or not """
        return path[self.piecesPosition[piece]] in self.DUAL_CHANCE

    def movablePieces(self, iplayer, step):
        """ method to deside the movable piece of each player"""
        p1Movables = list(self.p1Pieces)
        p2Movables = list(self.p2Pieces)
        # print(p1Movables, "\r\n", p2Movables)
        teamPos = []
        for pid, position in self.piecesPosition.items():
            (player, piece, pieces, path) = self.idByPiece(pid)
            # print(iplayer, position, player, piece, pieces, path)
            if (position + step < 1 + len(self.PATHS[0])):
                if player == iplayer:
                    teamPiece = dict()
                    teamPiece['pid'] = pid
                    teamPiece['position'] = position
                    teamPos += [teamPiece]
                continue
            if (player == self.p1) and pid in p1Movables:
                p1Movables.remove(pid)
            if (player == self.p2) and pid in p2Movables:
                p2Movables.remove(pid)
        teamPosSorted = sorted(teamPos, key=lambda k: k['position'])
        # print(teamPosSorted)
        for key in range(0, len(teamPosSorted) - 1):
            for nkey in range(key + 1, len(teamPosSorted)):
                diff = teamPosSorted[nkey]['position'] - \
                    teamPosSorted[key]['position']
                # print(key, nkey, diff)
                if diff == step:
                    pid = teamPosSorted[key]['pid']
                    if pid in p1Movables:
                        p1Movables.remove(pid)
                    if pid in p2Movables:
                        p2Movables.remove(pid)
        if self.p1 == iplayer:
            return p1Movables
        if self.p2 == iplayer:
            return p2Movables
        return []