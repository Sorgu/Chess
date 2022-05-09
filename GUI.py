import pygame
import main as chess
pygame.init()
WIDTH, HEIGHT = 600, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
pawn_pic = pygame.image.load("./pieces/pawn.png")


BG_COLOR = "white"
ROWS, COLS = 8, 8

SIZE = WIDTH / ROWS

field = [[0 for _ in range(COLS)]for _ in range(ROWS)]
print(field)
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
                if value == "Pawn":
                    win.blit(pawn_pic, (j * SIZE + 12, i * SIZE + 12))

        pygame.display.update()
    while run:
        update_board_state()
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
                    chess.move_piece(stored_commands)
                    print(chess.update_board())
                    stored_commands = []
                elif len(stored_commands) == 0:
                    stored_commands.append(row)
                    stored_commands.append(col)


main()