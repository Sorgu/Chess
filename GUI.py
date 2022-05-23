import pygame
import main as chess

#class Game_Piece:
#    def __init__(self, image, position):
#        self.image = image
#        self.pos = image.get_rect().move(0, height)
#        self.position = position

pygame.init()
WIDTH, HEIGHT = 600, 720
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
pawn_pic = pygame.image.load("./pieces/pawn.png")
rook_pic = pygame.image.load("./pieces/rook.png")
bishop_pic = pygame.image.load("./pieces/bishop.png")
knight_pic = pygame.image.load("./pieces/knight.png")
queen_pic = pygame.image.load("./pieces/queen.png")
king_pic = pygame.image.load("./pieces/king.png")
BG_COLOR = "white"
ROWS, COLS = 8, 8

SIZE = WIDTH / ROWS

field = [[0 for _ in range(COLS)]for _ in range(ROWS)]
def draw(win, field):
    win.fill(BG_COLOR)
    for i, row in enumerate(field):
        y = SIZE * i
        for j, value in enumerate(row):
            x = SIZE * j
            if i % 2 == 0 and j % 2 == 0:
                color = "burlywood1"
            elif i % 2 == 1 and j % 2 == 1:
                color = "burlywood1"
            else:
                color = "chocolate"
            pygame.draw.rect(win, color, (x, y, SIZE, SIZE))
            #pygame.draw.rect(win, "black", (x, y, SIZE, SIZE), 1)
    pygame.display.update()


def writeText(string, coordx, coordy, fontSize):
    #set the font to write with
    font = pygame.font.Font('freesansbold.ttf', fontSize)
    #(0, 0, 0) is black, to make black text
    print(string)
    text = font.render(str(string), True, (0, 0, 0))
    #get the rect of the text
    textRect = text.get_rect()
    #set the position of the text
    textRect.center = (coordx, coordy)
    #add text to window
    win.blit(text, textRect)
    pygame.display.update()
#draw(win, field)
#win.blit(pawn_pic, (1*SIZE, 1*SIZE))
#pygame.display.update()
#input()
def get_mouse_pos(mouse_pos):
    mx, my = mouse_pos
    row = int(my // SIZE)
    col = int(mx // SIZE)
    return row, col
def main():
    run = True
    draw(win, field)
    stored_commands = []

    def update_board_state():
        draw(win, field)
        board_state = chess.update_board()
        for i, row in enumerate(board_state):
            for j, value in enumerate(row):
                if value == "NoneType":
                    continue
                if value == "Pawn":
                    image = pawn_pic
                elif value == "Rook":
                    image = rook_pic
                elif value == "Bishop":
                    image = bishop_pic
                elif value == "Knight":
                    image = knight_pic
                elif value == "Queen":
                    image = queen_pic
                elif value == "King":
                    image = king_pic
                win.blit(image, (j * SIZE + 12, i * SIZE + 12))
        if check:
            writeText(cur_turn.capitalize() + " is in check", 220, 680, 50)
        elif checkmate:
            writeText(cur_turn.capitalize() + " is in checkmate", 280, 680, 50)
        writeText(cur_turn.capitalize() + "'s turn", 160, 630, 50)
        writeText("Turn: " + str(turn_i), 500, 630, 50)
        pygame.display.update()

    cur_turn = "white"
    turn_i = 0
    check = False
    checkmate = False
    update_board_state()


    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_mouse_pos(pygame.mouse.get_pos())
                if row >= ROWS or col >= COLS:
                    continue
                if len(stored_commands) == 2:
                    stored_commands.append(row)
                    stored_commands.append(col)
                    result = chess.move_piece(stored_commands, cur_turn, turn_i)
                    if not result:
                        print("invalid")
                    else:
                        result, cur_turn, turn_i = result
                        if result == "check":
                            print("CHECK")
                            check = True
                        elif result == "check mate":
                            print("MATE")
                            checkmate = True
                            check = False
                        else:
                            check = False
                    stored_commands = []

                    update_board_state()
                elif len(stored_commands) == 0:
                    stored_commands.append(row)
                    stored_commands.append(col)


main()