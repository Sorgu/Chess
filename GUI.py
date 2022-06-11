import ctypes
import pygame
import main as chess

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)
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
white_pawn_pic = pygame.image.load("./pieces/white_pawn.png")
white_rook_pic = pygame.image.load("./pieces/white_rook.png")
white_bishop_pic = pygame.image.load("./pieces/white_bishop.png")
white_knight_pic = pygame.image.load("./pieces/white_knight.png")
white_queen_pic = pygame.image.load("./pieces/white_queen.png")
white_king_pic = pygame.image.load("./pieces/white_king.png")
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
                if value == None:
                    continue
                if value.color == "black":
                    if value.__class__.__name__ == "Pawn":
                        image = pawn_pic
                    elif value.__class__.__name__ == "Rook":
                        image = rook_pic
                    elif value.__class__.__name__ == "Bishop":
                        image = bishop_pic
                    elif value.__class__.__name__ == "Knight":
                        image = knight_pic
                    elif value.__class__.__name__ == "Queen":
                        image = queen_pic
                    elif value.__class__.__name__ == "King":
                        image = king_pic
                elif value.color == "white":
                    if value.__class__.__name__ == "Pawn":
                        image = white_pawn_pic
                    elif value.__class__.__name__ == "Rook":
                        image = white_rook_pic
                    elif value.__class__.__name__ == "Bishop":
                        image = white_bishop_pic
                    elif value.__class__.__name__ == "Knight":
                        image = white_knight_pic
                    elif value.__class__.__name__ == "Queen":
                        image = white_queen_pic
                    elif value.__class__.__name__ == "King":
                        image = white_king_pic
                win.blit(image, (j * SIZE + 12, i * SIZE + 12))
        if check:
            writeText(cur_turn.capitalize() + " is in check", 220, 680, 50)
        elif checkmate:
            writeText(cur_turn.capitalize() + " is in checkmate", 280, 680, 50)
        writeText(cur_turn.capitalize() + "'s turn", 160, 630, 50)
        writeText("Turn: " + str(turn_i), 500, 630, 50)
        if promote:
            pygame.draw.rect(win, (170, 170, 170), [0, (HEIGHT / 8) * 2, 75, 40])
            writeText("Queen", WIDTH / 8 - 40, (HEIGHT / 8) * 2 + 15, 20)
            pygame.draw.rect(win, (170, 170, 170), [(WIDTH / 8) * 2, (HEIGHT / 8) * 2, 75, 40])
            writeText("Knight", (WIDTH / 8) * 3 - 40, (HEIGHT / 8) * 2 + 15, 20)
            pygame.draw.rect(win, (170, 170, 170), [(WIDTH / 8) * 4, (HEIGHT / 8) * 2, 75, 40])
            writeText("Rook", (WIDTH / 8) * 5 - 40, (HEIGHT / 8) * 2 + 15, 20)
            pygame.draw.rect(win, (170, 170, 170), [(WIDTH / 8) * 6, (HEIGHT / 8) * 2, 75, 40])
            writeText("Bishop", (WIDTH / 8) * 7 - 40, (HEIGHT / 8) * 2 + 15, 20)
        if force_draw:
            writeText("Game result: Draw", 280, 680, 50)

        pygame.display.update()

    cur_turn = "white"
    turn_i = 0
    check = False
    checkmate = False
    promote = False
    draw_request = False
    force_draw = False
    update_board_state()


    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if draw_request:
                draw_result = Mbox("Threefold repetition", "Would any of the players like to draw?", 4)
                if draw_result == 7:
                    pass
                elif draw_result == 6:
                    force_draw = True
                    update_board_state()
                draw_request = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_mouse_pos(pygame.mouse.get_pos())
                if row >= ROWS or col >= COLS:
                    continue
                if promote:
                    promote_result = False
                    print(row, col)
                    if row == 2 and col == 0:
                        promote_result = chess.Queen
                    elif row == 2 and col == 2:
                        promote_result = chess.Knight
                    elif row == 2 and col == 4:
                        promote_result = chess.Rook
                    elif row == 2 and col == 6:
                        promote_result = chess.Bishop
                    else:
                        print("invalid selection")
                    if promote_result:
                        chess.promotion(promote_input[1], promote_input[2], promote_result)
                        promote = False
                        update_board_state()



                elif len(stored_commands) == 2:
                    stored_commands.append(row)
                    stored_commands.append(col)
                    result = chess.move_piece(stored_commands, cur_turn, turn_i)
                    if not result:
                        print("invalid")
                    else:
                        result, cur_turn, turn_i, promote_input, threefold_result = result
                        if result == "check":
                            print("CHECK")
                            check = True
                        elif result == "check mate":
                            print("MATE")
                            checkmate = True
                            check = False
                        else:
                            check = False
                        if promote_input[0]:
                            promote = True
                        if threefold_result == "threefold":
                            draw_request = True
                        elif threefold_result == "fivefold":
                            force_draw = True
                    stored_commands = []

                    update_board_state()
                elif len(stored_commands) == 0:
                    stored_commands.append(row)
                    stored_commands.append(col)


main()