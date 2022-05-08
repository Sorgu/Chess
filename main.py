import itertools
import logging
from pprint import *

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
                            if grid[z][w].piece.__class__.__name__ == "King":
                                logging.info(f"{self.color} has put enemy in check")

                            return False
                        return "Attack"
                    else:
                        logging.info(f"Enemy piece in the way at {z, w}")
                        return False
            else:
                if current_step == total_steps:
                    return "Move"
                else:
                    return "Empty"
        except IndexError:
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


class Pawn(Piece):
    def move(self, steps):
        x, y = self.position
        if self.color == "black" and x != 1:
            if steps != 1:
                logging.info("Invalid input, pawn can only move 1 tile after first move")
                return False
        elif self.color == "white" and x != 1:
            if steps != 1:
                logging.info("Invalid input, pawn can only move 1 tile after first move")
                return False
        if steps > 2:
            logging.info("Invalid move, too many steps")
            return False
        if self.color == "white":
            steps = -steps
        for each in range(steps):
            x_with_steps = x + steps
            if grid[x_with_steps][y].check_for_piece():
                logging.info(f"Invalid move, another piece in the way {grid[x_with_steps][y].check_for_piece()}")
                return False
            else:
                continue

        grid[x][y].set_piece(None)
        new_position = (x + steps, y)
        grid[x + steps][y].set_piece(self)
        self.position = new_position
        logging.info(f"{self.color} {self.__class__.__name__} moved from {x, y}to {self.position}")
        self.attack("e", check_if_check=True)
        self.attack("w", check_if_check=True)

    def attack(self, direction, check_if_check=False):
        x, y = self.position
        if direction == "w":
            dir = -1
        elif direction == "e":
            dir = 1
        else:
            logging.info(f"Invalid input: {direction}")
            return False
        if self.color == "white":
            new_position = (x - 1, y + dir)
        else:
            new_position = (x + 1, y + dir)
        z, w = new_position
        if grid[z][w].check_for_piece():
            if grid[z][w].piece.color != self.color:
                if check_if_check:
                    if grid[z][w].piece.__class__.__name__ == "King":
                        logging.info(f"{self.color} has checked their opponent with their {self.__class__.__name__}")
                    return
                attacked_piece = grid[z][w].piece.__class__.__name__
                grid[x][y].set_piece(None)
                grid[z][w].set_piece(self)
                logging.info(
                    f"{self.color} {self.__class__.__name__} went from {x, y} and took {attacked_piece} at {z, w}")
        else:
            logging.info("No enemy pieces to attack")
            return False


class Rook(Piece):
    def move(self, steps, direction_input):
        x, y = self.position
        flag_attack = False

        for each in range(steps):
            each += 1
            negative_each = -each
            if direction_input == "s":
                new_position = x + negative_each, y
            elif direction_input == "n":
                new_position = x + each, y
            elif direction_input == "e":
                new_position = x, y + each
            elif direction_input == "w":
                new_position = x, y + negative_each
            else:
                logging.info("invalid input on rook move")
                return False
            z, w = new_position
            if grid[z][w].check_for_piece():
                if grid[z][w].piece.color == self.color:
                    logging.info(f"Friendly piece in the way at {z, w, grid[z][w].piece}")
                    return False
                else:
                    if each == steps:
                        flag_attack = True
                    else:
                        logging.info(f"Enemy piece in the way at {z, w}")
                        return False
            else:
                continue
        if flag_attack:
            attacked_piece = grid[z][w].piece.__class__.__name__
            grid[x][y].set_piece(None)
            grid[z][w].set_piece(self)
            self.position = (z, w)
            logging.info(
                f"{self.color, self.__class__.__name__} moved from {x, y} and attacked {attacked_piece} at {z, w}")
        else:
            grid[x][y].set_piece(None)
            grid[z][w].set_piece(self)
            self.position = (z, w)
            logging.info(f"{self.color, self.__class__.__name__} moved from {x, y} to {z, w}")


class Bishop(Piece):
    def move(self, steps, direction_input):
        x, y = self.position
        flag_attack = False

        for each in range(steps):
            each += 1
            negative_each = -each
            if direction_input == "sw":
                new_position = x + negative_each, y + negative_each
            elif direction_input == "se":
                new_position = x + negative_each, y + each
            elif direction_input == "nw":
                new_position = x + each, y + negative_each
            elif direction_input == "ne":
                new_position = x + each, y + each
            else:
                logging.info("invalid input on rook move")
                return False
            z, w = new_position
            if grid[z][w].check_for_piece():
                if grid[z][w].piece.color == self.color:
                    logging.info(f"Friendly piece in the way at {z, w, grid[z][w].piece}")
                    return False
                else:
                    if each == steps:
                        flag_attack = True
                    else:
                        logging.info(f"Enemy piece in the way at {z, w}")
                        return False
            else:
                continue
        if flag_attack:
            attacked_piece = grid[z][w].piece.__class__.__name__
            grid[x][y].set_piece(None)
            grid[z][w].set_piece(self)
            self.position = (z, w)
            logging.info(
                f"{self.color, self.__class__.__name__} moved from {x, y} and attacked {attacked_piece} at {z, w}")
        else:
            grid[x][y].set_piece(None)
            grid[z][w].set_piece(self)
            self.position = (z, w)
            logging.info(f"{self.color, self.__class__.__name__} moved from {x, y} to {z, w}")


class Knight(Piece):
    def move(self, direction_input):
        x, y = self.position
        flag_attack = False

        if direction_input == "sw":
            new_position = x - 2, y - 1
        elif direction_input == "se":
            new_position = x - 2, y + 1
        elif direction_input == "nw":
            new_position = x + 2, y - 1
        elif direction_input == "ne":
            new_position = x + 2, y + 1
        elif direction_input == "wn":
            new_position = x - 1, y + 2
        elif direction_input == "ws":
            new_position = x - 1, y - 2
        elif direction_input == "en":
            new_position = x + 1, y + 2
        elif direction_input == "ew":
            new_position = x + 1, y - 2
        else:
            logging.info("invalid input on rook move")
            return False
        z, w = new_position
        if grid[z][w].check_for_piece():
            if grid[z][w].piece.color == self.color:
                logging.info(f"Friendly piece in the way at {z, w, grid[z][w].piece}")
                return False
            else:
                flag_attack = True

        else:
            pass
        if flag_attack:
            attacked_piece = grid[z][w].piece.__class__.__name__
            grid[x][y].set_piece(None)
            grid[z][w].set_piece(self)
            self.position = (z, w)
            logging.info(
                f"{self.color, self.__class__.__name__} moved from {x, y} and attacked {attacked_piece} at {z, w}")
        else:
            grid[x][y].set_piece(None)
            grid[z][w].set_piece(self)
            self.position = (z, w)
            logging.info(f"{self.color, self.__class__.__name__} moved from {x, y} to {z, w}")


class Queen(Piece):
    def move(self, targetx, targety, check_if_check=False):

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
        z, w = self.position
        x, y = self.position
        maxx_minx = max(x, targetx) - min(x,targetx)
        if maxx_minx == 0:
            steps = max(y, targety) - min(y, targety)
        else:
            steps = maxx_minx
        chosen_direction = direction(targetx, targety, x, y)

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
            elif not command:
                return False
            else:
                raise Exception(logging.critical("Not supposed to happen"))

class King(Piece):
    def move(self, direction_input):
        steps = 1
        x, y = self.position
        flag_attack = False

        for each in range(steps):
            each += 1
            negative_each = -each
            if direction_input == "sw":
                new_position = x + negative_each, y + negative_each
            elif direction_input == "se":
                new_position = x + negative_each, y + each
            elif direction_input == "nw":
                new_position = x + each, y + negative_each
            elif direction_input == "ne":
                new_position = x + each, y + each
            elif direction_input == "s":
                new_position = x + negative_each, y
            elif direction_input == "n":
                new_position = x + each, y
            elif direction_input == "e":
                new_position = x, y + each
            elif direction_input == "w":
                new_position = x, y + negative_each
            else:
                logging.info("invalid input on rook move")
                return False
            z, w = new_position
            if grid[z][w].check_for_piece():
                if grid[z][w].piece.color == self.color:
                    logging.info(f"Friendly piece in the way at {z, w, grid[z][w].piece}")
                    return False
                else:
                    if each == steps:
                        flag_attack = True
                    else:
                        logging.info(f"Enemy piece in the way at {z, w}")
                        return False
            else:
                continue
        if flag_attack:
            attacked_piece = grid[z][w].piece.__class__.__name__
            grid[x][y].set_piece(None)
            grid[z][w].set_piece(self)
            self.position = (z, w)
            logging.info(
                f"{self.color, self.__class__.__name__} moved from {x, y} and attacked {attacked_piece} at {z, w}")
        else:
            grid[x][y].set_piece(None)
            grid[z][w].set_piece(self)
            self.position = (z, w)
            logging.info(f"{self.color, self.__class__.__name__} moved from {x, y} to {z, w}")


def initialize_grid():
    grid = []
    for every in range(8):
        grid_row = []
        for each in range(8):
            grid_row.append(Tile())
        grid.append(grid_row)
    return grid


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

grid[1][5].piece.move(2)
grid[3][5].piece.move(1)
grid[4][5].piece.move(1)
grid[5][5].piece.attack("w")
grid[7][3].piece.move("se")
grid[0][4].piece.move(1, 5)
grid[1][5].piece.move(2, 4)
grid[2][4].piece.move(6, 4)
grid[6][4].piece.move(4,3)
for each in grid:
    for every in each:
        print(every)
        pass
