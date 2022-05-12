import itertools
import logging
from pprint import *
import gc


logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")


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


class Piece:
    def __init__(self, color, position):
        self.color = color
        self.position = position

    def check_for_pieces(self, z, w, current_step, total_steps, check_if_check):
        try:
            if grid[z][w].check_for_piece():
                if grid[z][w].piece.color == self.color:
                    logging.info(f"Friendly piece in the way at {z, w, grid[z][w].piece}")
                    return False
                else:
                    if current_step == total_steps:
                        if check_if_check:
                            #if grid[z][w].piece.__class__.__name__ == "King":
                            #    logging.info(f"{self.color} {self.__class__.__name__} at {self.position} has put enemy in check ")
                            #    return "Check"
                            logging.info(f"{self.color} {self.__class__.__name__} at {self.position} has put enemy in check ")
                            return "Check"
                        return "Attack"
                    else:
                        logging.info(f"Enemy piece in the way at {z, w}")
                        return False
            else:
                if current_step == total_steps:
                    if not check_if_check:
                        return "Move"
                    elif check_if_check:
                        logging.info(f"{self.__class__.__name__, self.position} Check")
                        return "Check"
                else:
                    logging.info(f"{self.__class__.__name__} empty")
                    return "Empty"
        except IndexError:
            logging.info(f"{self.__class__.__name__} tried going off the board")
            return False

    def attack(self, x, y, z, w):
        attacked_piece = grid[z][w].piece.__class__.__name__
        grid[x][y].set_piece(None)
        grid[z][w].set_piece(self)
        self.position = (z, w)
        logging.info(
            f"{self.color, self.__class__.__name__} moved from {x, y} and attacked {attacked_piece} at {z, w}")

    def do_move(self, x, y, z, w):
        grid[x][y].set_piece(None)
        grid[z][w].set_piece(self)
        self.position = (z, w)
        logging.info(f"{self.color, self.__class__.__name__} moved from {x, y} to {z, w}")

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


class Pawn(Piece):
    def move(self, targetx, targety, check_if_check=False):
        if self.color == "black":
            if self.position[1] != targety:
                if (self.position[1] + 1 == targety or self.position[1] - 1 == targety) and self.position[0] + 1 == targetx:
                    logging.info(f"pawn info {self.position, targetx, targety}")
                    pass
                else:
                    logging.warning(f"{self.__class__.__name__} can not move there")
                    return False
            elif grid[targetx][targety].piece:
                return False
            if targetx - self.position[0] == 1:
                pass
            elif self.position[0] == 1 and targetx - self.position[0] == 2:
                pass
            else:
                logging.warning(f"{self.__class__.__name__} can not move there")
                return False
        elif self.color == "white":
            if self.position[1] != targety:
                if (self.position[1] + 1 == targety or self.position[1] - 1 == targety) and self.position[0] - 1 == targetx:
                    pass
                else:
                    logging.warning(f"{self.__class__.__name__} can not move there")
                    return False
            elif grid[targetx][targety].piece:
                return False
            if self.position[0] - targetx <= 1:
                pass
            elif self.position[0] == 6 and self.position[0] - targetx == 2:
                pass
            else:
                logging.warning(f"{self.__class__.__name__} can not move there")
                return False
        else:
            logging.warning(f"{self.__class__.__name__} can not move there")
            return False


        def direction(z, w, x, y):
            if self.color == "black":
                if y == w:
                    new_position = lambda x, y: [x + 1, y]
                    return new_position
                elif y + 1 == w:
                    new_position = lambda x, y: [x + 1, y + 1]
                    return new_position
                elif y - 1 == w:
                    new_position = lambda x, y: [x + 1, y - 1]
                    return new_position
            elif self.color == "white":
                if y == w:
                    new_position = lambda x, y: [x - 1, y]
                    return new_position
                elif y + 1 == w:
                    new_position = lambda x, y: [x - 1, y + 1]
                    return new_position
                elif y - 1 == w:
                    new_position = lambda x, y: [x - 1, y - 1]
                    return new_position

        chosen_direction = direction(targetx, targety, self.position[0], self.position[1])
        a = self.do_move_do(targetx, targety, chosen_direction, check_if_check)
        if a:
            if a == "Check":
                return "check"
            return True


class Rook(Piece):
    def move(self, targetx, targety, check_if_check=False):
        if self.position[0] == targetx or self.position[1] == targety:
            pass
        else:
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


class Bishop(Piece):
    def move(self, targetx, targety, check_if_check=False):
        if targetx - self.position[0] == targety - self.position[1] or self.position[0] - targetx == targety - \
                self.position[1]:
            pass
        else:
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
            elif x-2 == w:
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
                logging.info(f"{self.__class__.__name__} can not move there")
                return False

        chosen_direction = direction(targetx, targety, self.position[0], self.position[1])
        if chosen_direction:
            if self.do_move_do(targetx, targety, chosen_direction, check_if_check, knight=True):
                return True
        else:
            return False


class Queen(Piece):
    def move(self, targetx, targety, check_if_check=False):
        if self.position[0] == targetx or self.position[1] == targety:
            pass
        elif targetx - self.position[0] == targety - self.position[1] or self.position[0] - targetx == targety - self.position[1]:
            pass
        else:
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


class King(Piece):
    def move(self, targetx, targety, check_if_check=False):
        # 0 3  3 3
        if max(targetx, self.position[0]) - min(targetx, self.position[0]) > 1 or max(targety, self.position[1]) - min(targety, self.position[1]) > 1:
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


def initialize_grid():
    grid = []
    for every in range(8):
        grid_row = []
        for each in range(8):
            grid_row.append(Tile())
        grid.append(grid_row)
    return grid

def update_board():
    board_state = [[] for _ in range(8)]
    for i, row in enumerate(grid):
        for j, value in enumerate(row):
            piece = grid[i][j].piece.__class__.__name__
            board_state[i].append(piece)
    return board_state

def move_piece(stored_commands):
    x1, y1, x2, y2 = stored_commands
    check_amount = 0
    if not grid[x1][y1].check_for_piece():
        return False
    color = grid[x1][y1].piece.color
    if grid[x1][y1].piece.move(x2, y2):
        check_amount = is_check(check_amount, color)
    if check_amount == 0:
        return False
    elif check_amount[0]:
        if not check_mate(color, *check_amount):
            return "check mate"
        return "check"

def is_check(check_amount, color, king_position=None):
    king_pos, black_list_of_pieces, white_list_of_pieces = get_king_position(color)
    attacker = []
    if king_position:

        king_pos = king_position
    logging.info(f"{king_pos} {color}")
    color_list_of_pieces = black_list_of_pieces if color == "black" else white_list_of_pieces
    for each in color_list_of_pieces:
        logging.info(f"is_check {each, each.color}")
        if each.move(king_pos[0], king_pos[1], check_if_check=True):
            check_amount += 1
            attacker.append(each)
    logging.info(f"check amount: {check_amount}, attacker: {attacker} ")
    if attacker:
        print("attacker position, ", attacker[0].position)
    return check_amount, attacker

# checker is the color of the piece putting the enemy in check, check_amount is the amount of pieces putting enemy in check
def check_mate(checker, check_amount, attacker):
    attacker = attacker[0]
    checkered = "black" if checker == "white" else "white"
    def move_king():
        logging.info("move_king")
        for obj in gc.get_objects():
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
            if not is_check(0, checkered, king_position=(x,y))[0]:
                return True
            continue
        return False

    def block():
        logging.info("block")
        tile_list = []
        king = get_king_position(checker)[0]
        name = attacker.__class__.__name__
        logging.info(f"{attacker.__class__.__name__, attacker, attacker}")
        if name == "Knight" or name == "Pawn" or name == "King":
            logging.info("cannot block knight, pawn, or king")
            return False
        maxx = max(attacker.position[0], king[0])
        minx = min(attacker.position[0], king[0])
        maxy = max(attacker.position[1], king[1])
        miny = min(attacker.position[1], king[1])
        ydiff = maxy - miny
        xdiff = maxx - minx
        if attacker.position[1] == king[1] and king[0] != king[0]:
            for each in range(xdiff - 1):
                each += 1
                tile_list.append([maxx - each, maxy])
        elif attacker.position[0] == king[0] and king[1] != king[1]:
            for each in range(ydiff - 1):
                each += 1
                tile_list.append([maxx, maxy - each])
            pass
        elif king[0] != attacker.position[0] and king[1] != attacker.position[1]:
            if xdiff == ydiff:
                for each in range(xdiff):
                    each += 1
                    tile_list.append([maxx - each, maxy - each])
            else:
                for each in range(max(xdiff, ydiff)):
                    each += 1
                    tile_list.append([maxx - each, maxy + each])
        logging.info(tile_list)
        for each in tile_list:
            if not is_check(0, checkered, king_position=each):
                return True
        return False

    def attack_attacker():
        logging.info("attack_attacker")
        a = is_check(0, checkered, king_position=attacker.position)[0]
        if a:
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



def get_king_position(color):
    black_list_of_pieces = []
    white_list_of_pieces = []

    for obj in gc.get_objects():
        if isinstance(obj, King):
            if obj.color == "black" and color == "white":
                king = obj.position
            elif obj.color == "white" and color == "black":
                king = obj.position
        if isinstance(obj, Piece):
            if obj.color == "black":
                black_list_of_pieces.append(obj)
            elif obj.color == "white":
                white_list_of_pieces.append(obj)
    return king, black_list_of_pieces, white_list_of_pieces

grid = initialize_grid()

for i, each in enumerate(grid[1]):
    each.set_piece(Pawn("black", (1, i)))
grid[0][0].set_piece(Rook("black", (0, 0)))
grid[0][7].set_piece(Rook("black", (0, 7)))
grid[0][1].set_piece(Knight("black", (0, 1)))
grid[0][6].set_piece(Knight("black", (0, 6)))
grid[0][2].set_piece(Bishop("black", (0, 2)))
grid[0][5].set_piece(Bishop("black", (0, 5)))
grid[0][3].set_piece(King("black", (0, 3)))
grid[0][4].set_piece(Queen("black", (0, 4)))

for i, each in enumerate(grid[6]):
    each.set_piece(Pawn("white", (6, i)))
grid[7][0].set_piece(Rook("white", (7, 0)))
grid[7][7].set_piece(Rook("white", (7, 7)))
grid[7][1].set_piece(Knight("white", (7, 1)))
grid[7][6].set_piece(Knight("white", (7, 6)))
grid[7][2].set_piece(Bishop("white", (7, 2)))
grid[7][5].set_piece(Bishop("white", (7, 5)))
grid[7][3].set_piece(King("white", (7, 3)))
grid[7][4].set_piece(Queen("white", (7, 4)))



