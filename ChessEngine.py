class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K':self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.piece == 'wk':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bk':
            self.blackKingLocation = (move.endRow, move.endCol)

        if move.isPawnpromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'


    def undoMove(self):
        if len(self.moveLog) !=0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.piece == 'wk':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bk':
                self.blackKingLocation = (move.startRow, move.startCol)


    def getValidMoves(self):
        moves = self.getAllPossibleMoves()
        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        return moves

    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def squareUnderAttack(self,r,c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False


    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves


    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c] == '--':
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r,c), (r-2, c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c-1), self.board))
            if c+1 <= 7:
                if self.board[r - 1][c + 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c+1), self.board))
        else:
            if self.board[r+1][c] == '--':
                moves.append(Move((r, c), (r+1,c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r,c), (r+2,c), self.board))
            if c-1 >=0:
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c-1), self.board))
            if c+1 <= 7:
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c+1), self.board))

    def getRookMoves(self, r, c, moves):
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        enemy_color = 'b' if self.whiteToMove else 'w'

        for d in directions:
            for i in range(1,8):
                end_row = r + d[0]*i
                end_col = c +d[1]*i
                if 0<=end_row < 8 and 0<= end_col <8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == '--':
                        moves.append(Move((r,c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((r,c), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        ally_color = 'w' if self.whiteToMove else 'b'
        for dr in [-2, -1, 1, 2]:
            for dc in [-2, -1, 1, 2]:
                if abs(dr) != abs(dc):
                    end_row, end_col = r + dr, c + dc
                    if 0 <= end_row < 8 and 0 <= end_col < 8:
                        end_piece = self.board[end_row][end_col]
                        if end_piece == '--' or end_piece[0] != ally_color:
                            moves.append(Move((r, c), (end_row, end_col), self.board))

    def getBishopMoves(self, r, c, moves):
        directions = [(-1,-1), (-1,1), (1,-1), (1,1)]
        enemy_color = 'b' if self.whiteToMove else 'w'

        for d in directions:
            for i in range(1,8):
                end_row = r + d[0]*i
                end_col = c +d[1]*i
                if 0<=end_row < 8 and 0<= end_col <8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == '--':
                        moves.append(Move((r,c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((r,c), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break



    def getQueenMoves(self, r, c, moves):
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # Rook-like moves (up, down, left, right)
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # Bishop-like moves (diagonals)
        ]
        enemy_color = 'b' if self.whiteToMove else 'w'

        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == '--':
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKingMoves(self, r, c, moves):
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        ally_color = 'w' if self.whiteToMove else 'b'

        for dr, dc in directions:
            end_row, end_col = r + dr, c + dc
            # Check if the move is within the board boundaries
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                # If the end square is empty or occupied by an enemy piece, add the move
                if end_piece == '--' or end_piece[0] != ally_color:
                    moves.append(Move((r, c), (end_row, end_col), self.board))



class Move():

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = False
        if (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7) :
            self.isPawnPromotion = True
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)


    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
