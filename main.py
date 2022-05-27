import itertools
import logging
from pprint import *
import gc


logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")

# class for the chess tiles that will contain chess pieces
class Tile:
    def __init__(self):
        self.piece = None

    def __str__(self):
        try:
            print(self.piece.position)
        except:
            pass
        return self.piece.__class__.__name__

    def set_piece(self, piece):
        self.piece = piece

    def check_for_piece(self):
        if self.piece:
            return self.piece
        else:
            return False


# parent class for all pieces
class Piece:
    def __init__(self, color, position, self_grid, en_passant=False):
        self.color = color
        self.position = position
        self.en_passant = en_passant
        self.grid = self_grid
    # checks if there is a piece in the coordinates provided and returns the appropriate command
    def check_for_pieces(self, z, w, current_step, total_steps, check_if_check):
        try:
            if self.grid[z][w].check_for_piece():
                if self.grid[z][w].piece.color == self.color:
                    logging.info(f"Friendly piece in the way at {z, w, self.grid[z][w].piece}")
                    return False
                else:
                    if current_step == total_steps:
                        if check_if_check:
                            if self.__class__.__name__ == "Pawn":
                                print("HEREEE1")
                                if self.attacking:
                                    pass
                                else:
                                    return False
                            logging.info(f"{self.color} {self.__class__.__name__} at {self.position} has put enemy in check ")
                            return "Check"
                        elif self.__class__.__name__ == "Pawn":
                            print("HEREEE2")
                            if self.attacking:
                                pass
                            else:
                                return False
                        return "Attack"
                    else:
                        logging.info(f"Enemy piece in the way at {z, w}")
                        return False
            else:
                if current_step == total_steps:
                    if not check_if_check:
                        return "Move"
                    elif check_if_check:
                        if self.__class__.__name__ == "Pawn":
                            print("HEREEE3")
                            if self.attacking:
                                pass
                            else:
                                return False
                        print((z, w, self.position))
                        logging.info(f"{self.__class__.__name__, self.position} Check")
                        return "Check"
                else:
                    return "Empty"
        except IndexError:
            logging.info(f"{self.__class__.__name__} tried going off the board")
            return False

    # replaces the piece at (z, w) with the piece at (x, y)
    def attack(self, x, y, z, w):
        attacked_piece = self.grid[z][w].piece.__class__.__name__
        del self.grid[x][y].piece
        self.grid[x][y].set_piece(None)
        self.grid[z][w].set_piece(self)
        self.position = (z, w)
        logging.info(
            f"{self.color, self.__class__.__name__} moved from {x, y} and attacked {attacked_piece} at {z, w}")

    # moves the piece at (x, y) to (z, w)
    def do_move(self, x, y, z, w):
        self.grid[x][y].set_piece(None)
        self.grid[z][w].set_piece(self)
        self.position = (z, w)
        logging.info(f"{self.color, self.__class__.__name__} moved from {x, y} to {z, w}")

    # calculates the tiles a piece needs to traverse and handles commands from check_for_pieces()
    def do_move_do(self, targetx, targety, chosen_direction, check_if_check, knight=False):
        z, w = self.position
        x, y = self.position
        maxx_minx = max(x, targetx) - min(x,targetx)
        if maxx_minx == 0:
            steps = max(y, targety) - min(y, targety)
        else:
            steps = maxx_minx
        if knight:
            steps = 1

        for each in range(steps):
            each += 1
            new_position = chosen_direction(z, w)
            z, w = new_position
            command = self.check_for_pieces(z, w, each, steps, check_if_check)
            if command == "Empty":
                continue
            elif command == "Attack":
                self.attack(x, y, z, w)
            elif command == "Move":
                self.do_move(x, y, z, w)
            elif command == "Check":
                return "Check"
            elif not command:
                return False
            else:
                raise Exception(logging.critical("Not supposed to happen"))
        return True

# class for the pawn piece with rules on how it can move and which direction to move
class Pawn(Piece):
    def __init__(self, color, position, self_grid, en_passant=False):
        self.en_passant = en_passant
        self.do_en_passant = False
        super(Pawn, self).__init__(color, position, self_grid, en_passant)
    def move(self, targetx, targety, check_if_check=False):
        self.attacking = False
        en_passant = False
        one = +1 if self.color == "black" else -1
        if self.color == "black" and targetx - self.position[0] > 0:
            pass
        elif self.color == "white" and self.position[0] - targetx > 0:
            pass
        else:
            return False

        if self.position[1] != targety:
            self.attacking = True

            if (self.position[1] + 1 == targety or self.position[1] - 1 == targety) and self.position[0] + one == targetx and self.grid[targetx][targety].check_for_piece():
                pass
            elif self.grid[targetx - one][targety].check_for_piece():
                if self.grid[targetx - one][targety].piece.en_passant == True and self.position[0] == targetx - one and (self.position[1] + 1 == targety or self.position[1] - 1 == targety):
                    self.do_en_passant = True
                    logging.info("EN PASSANT")
                else:
                    if not check_if_check:
                        logging.warning(f"{self.__class__.__name__} can not move there")
                    return False
            else:
                if not check_if_check:
                    logging.warning(f"{self.__class__.__name__} can not move there")
                return False
        elif self.grid[targetx][targety].piece:
            return False

        if max(targetx, self.position[0]) - min(targetx, self.position[0]) == 1:
            pass
        elif self.color == "black":
            if self.position[0] == 1 and targetx - self.position[0] == 2:
                en_passant = True
                pass
            else:
                return False
        elif self.color == "white":
            if self.position[0] == 6 and self.position[0] - targetx == 2:
                en_passant = True
                pass
            else:
                return False
        else:
            if not check_if_check:
                logging.warning(f"{self.__class__.__name__} can not move there")
            return False



        def direction(z, w, x, y):
            one = + 1 if self.color == "black" else - 1
            if y == w:
                new_position = lambda x, y: [x + one, y]
                return new_position
            elif y + 1 == w:
                new_position = lambda x, y: [x + one, y + 1]
                return new_position
            elif y - 1 == w:
                new_position = lambda x, y: [x + one, y - 1]
                return new_position

        if self.do_en_passant:
            logging.critical("EN PASSANT")
            if check_if_check:
                return "check"
            x, y = self.position
            one = +1 if self.color == "white" else -1
            attacked_piece = self.grid[targetx + one][targety].piece.__class__.__name__
            self.grid[x][y].set_piece(None)
            self.grid[targetx][targety].set_piece(self)
            self.grid[targetx + one][targety].set_piece(None)
            self.position = (targetx, targety)
            logging.info(
                f"{self.color, self.__class__.__name__} moved from {x, y} and attacked {attacked_piece} at {targetx, targety}")
        chosen_direction = direction(targetx, targety, self.position[0], self.position[1])
        a = self.do_move_do(targetx, targety, chosen_direction, check_if_check)
        if en_passant:
            self.en_passant = True
        else:
            self.en_passant = False
        if a:
            if a == "Check":
                return "check"
            return True

# class for the rook piece with rules on how it can move and which direction to move
class Rook(Piece):
    def move(self, targetx, targety, check_if_check=False):
        if self.position[0] == targetx or self.position[1] == targety:
            pass
        else:
            if not check_if_check:
                logging.warning(f"{self.__class__.__name__} can not move there")
            return False

        def direction(z, w, x, y): # z = new vertical coordinate, w = new horizontal coordinate, x = old vertical, y = old horizontal
            if z > x:
                new_position = lambda x, y: [x + 1, y]
                return new_position
            elif w > y:
                new_position = lambda x, y: [x, y + 1]
                return new_position
            elif w == y and z == x:
                return False  # This would move it to the tile it's standing on
            elif w < y:
                new_position = lambda x, y: [x, y - 1]
                return new_position
            elif z < x:
                new_position = lambda x, y: [x - 1, y]
                return new_position


        chosen_direction = direction(targetx, targety, self.position[0], self.position[1])
        if self.do_move_do(targetx, targety, chosen_direction, check_if_check):
            return True

# class for the bishop piece with rules on how it can move and which direction to move
class Bishop(Piece):
    def move(self, targetx, targety, check_if_check=False):
        if targetx - self.position[0] == targety - self.position[1] or self.position[0] - targetx == targety - \
                self.position[1]:
            pass
        else:
            if not check_if_check:
                logging.warning(f"{self.__class__.__name__} can not move there")
            return False

        def direction(z, w, x, y):
            if w == y:
                return False  # This would move it to the tile it's standing on
            elif z > x and w > y:
                new_position = lambda x, y: [x + 1, y + 1]
                return new_position

            elif z > x and w < y:
                new_position = lambda x, y: [x + 1, y - 1]
                return new_position

            elif z < x and w > y:
                new_position = lambda x, y: [x - 1, y + 1]
                return new_position

            elif z < x and w < y:
                new_position = lambda x, y: [x - 1, y - 1]
                return new_position

        chosen_direction = direction(targetx, targety, self.position[0], self.position[1])
        if self.do_move_do(targetx, targety, chosen_direction, check_if_check):
            return True

# class for the knight piece with rules on how it can move and which direction to move
class Knight(Piece):
    def move(self, targetx, targety, check_if_check=False):
        def direction(z, w, x, y):
            if x+2 == z:
                if y+1 == w:
                    new_position = lambda x,y:[x + 2, y + 1]
                    return new_position
                elif y-1 == w:
                    new_position = lambda x, y: [x + 2, y - 1]
                    return new_position
            elif x-2 == z:
                if y + 1 == w:
                    new_position = lambda x, y: [x - 2, y + 1]
                    return new_position
                elif y - 1 == w:
                    new_position = lambda x, y: [x - 2, y - 1]
                    return new_position
            elif y - 2 == w:
                if x + 1 == z:
                    new_position = lambda x, y: [x + 1, y - 2]
                    return new_position
                elif x - 1 == z:
                    new_position = lambda x, y: [x - 1, y - 2]
                    return new_position
            elif y + 2 == w:
                if x + 1 == z:
                    new_position = lambda x, y: [x + 1, y + 2]
                    return new_position
                elif x - 1 == z:
                    new_position = lambda x, y: [x - 1, y + 2]
                    return new_position
            else:
                if not check_if_check:
                    logging.info(f"{self.__class__.__name__} can not move there")
                return False

        chosen_direction = direction(targetx, targety, self.position[0], self.position[1])
        if chosen_direction:
            if self.do_move_do(targetx, targety, chosen_direction, check_if_check, knight=True):
                return True
        else:
            return False

# class for the queen piece with rules on how it can move and which direction to move
class Queen(Piece):
    def move(self, targetx, targety, check_if_check=False):
        if self.position[0] == targetx or self.position[1] == targety:
            pass
        elif targetx - self.position[0] == targety - self.position[1] or self.position[0] - targetx == targety - self.position[1]:
            pass
        else:
            if not check_if_check:
                logging.warning(f"{self.__class__.__name__} can not move there")
            return False
        def direction(z, w, x, y):
            if z > x:
                if w > y:
                    new_position = lambda x,y:[x + 1, y + 1]
                    return new_position
                elif w == y:
                    new_position = lambda x,y:[x + 1, y]
                    return new_position
                elif w < y:
                    new_position = lambda x,y:[x + 1, y - 1]
                    return new_position
            elif z == x:
                if w > y:
                    new_position = lambda x,y:[x, y + 1]
                    return new_position
                elif w == y:
                    return False  # This would move it to the tile it's standing on
                elif w < y:
                    new_position = lambda x,y:[x, y - 1]
                    return new_position
            elif z < x:
                if w > y:
                    new_position = lambda x,y:[x - 1, y + 1]
                    return new_position
                elif w == y:
                    new_position = lambda x,y:[x - 1, y]
                    return new_position
                elif w < y:
                    new_position = lambda x,y:[x - 1, y - 1]
                    return new_position

        chosen_direction = direction(targetx, targety, self.position[0], self.position[1])
        if self.do_move_do(targetx, targety, chosen_direction, check_if_check):
            return True

# class for the king piece with rules on how it can move and which direction to move
class King(Piece):
    def move(self, targetx, targety, check_if_check=False):
        if max(targetx, self.position[0]) - min(targetx, self.position[0]) > 1 or max(targety, self.position[1]) - min(targety, self.position[1]) > 1:
            if not check_if_check:
                logging.info(f"{self.__class__.__name__} can not move there, {self.position, self.position[0] - targetx, self.position[1] - targety}")
            return False

        def direction(z, w, x, y):
            if z > x:
                if w > y:
                    new_position = lambda x, y: [x + 1, y + 1]
                    return new_position
                elif w == y:
                    new_position = lambda x, y: [x + 1, y]
                    return new_position
                elif w < y:
                    new_position = lambda x, y: [x + 1, y - 1]
                    return new_position
            elif z == x:
                if w > y:
                    new_position = lambda x, y: [x, y + 1]
                    return new_position
                elif w == y:
                    return False  # This would move it to the tile it's standing on
                elif w < y:
                    new_position = lambda x, y: [x, y - 1]
                    return new_position
            elif z < x:
                if w > y:
                    new_position = lambda x, y: [x - 1, y + 1]
                    return new_position
                elif w == y:
                    new_position = lambda x, y: [x - 1, y]
                    return new_position
                elif w < y:
                    new_position = lambda x, y: [x - 1, y - 1]
                    return new_position

        chosen_direction = direction(targetx, targety, self.position[0], self.position[1])
        if self.do_move_do(targetx, targety, chosen_direction, check_if_check):
            return True

# returns a list of pieces present on the board
def update_board():
    board_state = [[] for _ in range(8)]
    for i, row in enumerate(grid):
        for j, value in enumerate(row):
            piece = grid[i][j].piece.__class__.__name__
            board_state[i].append(piece)
    return board_state

# changes the value of cur_turn from black to white or white to black and adds 1 to the total amount of moves
def change_turn(cur_turn, turn_i):
    turn = "black" if cur_turn == "white" else "white"
    turn_i += 1
    return turn, turn_i

# takes two coordinates from GUI.py and if it is a piece, it is moved from (x1, y1) to (x2, y2). After moving, it checks
# if the enemy has been put in check or checkmate
def move_piece(stored_commands, cur_turn, turn_i):
    x1, y1, x2, y2 = stored_commands
    check_amount = 0
    if not grid[x1][y1].check_for_piece():
        logging.info(f"no piece found at {x1}, {y1}")
        return False
    color = grid[x1][y1].piece.color
    if color != cur_turn:
        logging.info(f"it is not {color}'s turn")
        return False
    copy_board()
    if testing_grid[x1][y1].piece.move(x2, y2):
        other_color = "white" if color == "black" else "black"
        if is_check(other_color, testing_grid)[0] != 0:
            logging.info(f"{color} tried putting themselves in check")
            return False
        else:
            grid[x1][y1].piece.move(x2, y2)
            cur_turn, turn_i = change_turn(cur_turn, turn_i)
            check_amount = is_check(color, grid)
            clean_board(testing_grid)
    else:
        logging.info(f"Illegal move")
        return False
    if check_amount[0] == 0:
        return [True, cur_turn, turn_i]

    elif check_amount[0]:
        if not check_mate(color, *check_amount):
            return ["check mate", cur_turn, turn_i]
        return ["check", cur_turn, turn_i]


#
def is_check(color, local_grid, king_position=None, mate_check=False, king=None):
    king_pos, black_list_of_pieces, white_list_of_pieces = get_king_position(color, local_grid)
    attacker = []
    check_amount = 0
    if king_position:
        king_pos = king_position
    logging.info(f"{king_pos} {color}")
    color_list_of_pieces = black_list_of_pieces if color == "black" else white_list_of_pieces
    #if mate_check:
    #    if king.move(king_pos[0], king_pos[1], check_if_check=True):
    #        return 0, attacker
    #        check_amount += 1
    #        attacker.append(each)
    for each in color_list_of_pieces:
        if each.move(king_pos[0], king_pos[1], check_if_check=True):
            check_amount += 1
            attacker.append(each)
    logging.info(f"check amount: {check_amount}, attacker: {attacker} ")
    return [check_amount, attacker]

# checker is the color of the piece putting the enemy in check, check_amount is the amount of pieces putting enemy in check
def check_mate(checker, check_amount, attacker):
    attacker = attacker[0]
    checkered = "black" if checker == "white" else "white"
    def move_king():
        logging.info("move_king")
        for obj in gc.get_objects():
            if isinstance(obj, Piece):
                if obj.grid == grid:
                    if isinstance(obj, King) and obj.color == checkered:
                        checked_king = obj
        checked_king_pos = checked_king.position
        for each in itertools.product((-1, 0, 1), repeat=2):
            x = checked_king_pos[0] - each[0]
            y = checked_king_pos[1] - each[1]
            if x > 7 or x < 0 or y > 7 or y < 0:
                continue
            if grid[x][y].check_for_piece():
                if grid[x][y].piece.color == checkered:
                    continue
            if not is_check(checker, grid, king_position=(x,y), mate_check=True)[0]:
                return True
            continue
        return False

    def block():
        logging.info("block")
        tile_list = []
        king = get_king_position(checker, grid)[0]
        name = attacker.__class__.__name__
        logging.info(f"{name} is attacking")
        if name == "Knight" or name == "Pawn" or name == "King":
            logging.info("cannot block knight, pawn, or king")
            return False
        maxx = max(attacker.position[0], king[0])
        minx = min(attacker.position[0], king[0])
        maxy = max(attacker.position[1], king[1])
        miny = min(attacker.position[1], king[1])
        ydiff = maxy - miny
        xdiff = maxx - minx
        if attacker.position[1] == king[1] and attacker.position[0] != king[0]:
            for each in range(xdiff - 1):
                each += 1
                tile_list.append([maxx - each, maxy])
        elif attacker.position[0] == king[0] and attacker.position[1] != king[1]:
            for each in range(ydiff - 1):
                each += 1
                tile_list.append([maxx, maxy - each])
        elif king[0] != attacker.position[0] and king[1] != attacker.position[1]:
            if (attacker.position[0] > king[0] and attacker.position[1] > king[1]) or (attacker.position[0] < king[0] and attacker.position[1] < king[1]):
                for each in range(xdiff - 1):
                    each += 1
                    tile_list.append([maxx - each, maxy - each])
            else:
                for each in range(max(xdiff, ydiff) - 1):
                    each += 1
                    tile_list.append([maxx - each, miny + each])
        logging.info(f"tile list: {tile_list} ")
        for each in tile_list:
            check_amount, local_checker = is_check(checkered, grid, king_position=each)
            for every in local_checker:
                if check_amount and every.__class__.__name__ != "King":
                    logging.critical(every.__class__.__name__)
                    return True
        return False

    def attack_attacker():
        logging.info("attack_attacker")
        is_check_result = is_check(checkered, grid, king_position=attacker.position)
        logging.info(f"{is_check_result} is_check_result")
        if is_check_result[0]:
            if isinstance(is_check_result[1][0], King):
                is_check_result[0] -=1
            if is_check_result[0]:
                return True
        else:
            return False

    if check_amount > 1:
        if move_king():
            return True
        else:
            return False
    elif check_amount == 1:
        if move_king() or block() or attack_attacker():
            logging.info(f"{move_king()}{block()}{attack_attacker()}CHECKMATE FUNCTION")
            return True
        else:
            return False
    return False



def get_king_position(color, local_grid):
    black_list_of_pieces = []
    white_list_of_pieces = []

    for obj in gc.get_objects():
        if isinstance(obj, Piece):
            if obj.grid == local_grid:
                if isinstance(obj, King):
                    if obj.color == "black":
                        if color == "white":
                            king = obj.position
                        black_list_of_pieces.append(obj)
                    elif obj.color == "white":
                        if color == "black":
                            king = obj.position
                        white_list_of_pieces.append(obj)
                else:
                    if obj.color == "black":
                        black_list_of_pieces.append(obj)
                    elif obj.color == "white":
                        white_list_of_pieces.append(obj)

    return king, black_list_of_pieces, white_list_of_pieces

# creates an 8x8 matrix containing tiles
def initialize_grid():
    grid = []
    for every in range(8):
        grid_row = []
        for each in range(8):
            grid_row.append(Tile())
        grid.append(grid_row)
    return grid

# populates an initialized grid with chess pieces
def populate_grid(grid):
    for i, each in enumerate(grid[1]):
        each.set_piece(Pawn("black", (1, i), grid))
    grid[0][0].set_piece(Rook("black", (0, 0), grid))
    grid[0][7].set_piece(Rook("black", (0, 7), grid))
    grid[0][1].set_piece(Knight("black", (0, 1), grid))
    grid[0][6].set_piece(Knight("black", (0, 6), grid))
    grid[0][2].set_piece(Bishop("black", (0, 2), grid))
    grid[0][5].set_piece(Bishop("black", (0, 5), grid))
    grid[0][3].set_piece(King("black", (0, 3), grid))
    grid[0][4].set_piece(Queen("black", (0, 4), grid))

    for i, each in enumerate(grid[6]):
        each.set_piece(Pawn("white", (6, i), grid))
    grid[7][0].set_piece(Rook("white", (7, 0), grid))
    grid[7][7].set_piece(Rook("white", (7, 7), grid))
    grid[7][1].set_piece(Knight("white", (7, 1), grid))
    grid[7][6].set_piece(Knight("white", (7, 6), grid))
    grid[7][2].set_piece(Bishop("white", (7, 2), grid))
    grid[7][5].set_piece(Bishop("white", (7, 5), grid))
    grid[7][3].set_piece(King("white", (7, 3), grid))
    grid[7][4].set_piece(Queen("white", (7, 4), grid))

def copy_board():
    for i, row in enumerate(grid):
        for j, value in enumerate(row):
            if value.check_for_piece():
                testing_grid[i][j].set_piece(value.piece.__class__(value.piece.color, value.piece.position, testing_grid, en_passant=value.piece.en_passant))

def clean_board(grid):
    for each in grid:
        for every in each:
            if every.check_for_piece():
                del every.piece
                every.set_piece(None)
grid = initialize_grid()
populate_grid(grid)
testing_grid = initialize_grid()
copy_board()



