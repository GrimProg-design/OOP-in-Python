import pygame
import sys

pygame.init()
clock = pygame.time.Clock()

ROWS = 30
COLS = 50
CELL_SIZE = 20
FPS = 10

class Grid:
    def __init__(self, rows, cols, cell_size=20):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.cells = []
        for row in range(rows):
            row_list = []
            for col in range(cols):
                row_list.append(False)
            self.cells.append(row_list)
        self.screen = pygame.display.set_mode((cols*cell_size, rows*cell_size))
        pygame.display.set_caption("My Game of Life")

    def draw_grid(self):
        self.screen.fill((255, 255, 255))
        for r in range(self.rows):
            for c in range(self.cols):
                if self.cells[r][c]:
                    x = c * self.cell_size
                    y = r * self.cell_size
                    pygame.draw.rect(self.screen, (0, 0, 0), 
                                     (x+1, y+1, self.cell_size-1, self.cell_size-1))
                    
        for c in range(self.cols + 1):
            x = c * self.cell_size
            pygame.draw.line(self.screen, (0, 0, 0), (x, 0), (x, self.rows*self.cell_size))
        for r in range(self.rows + 1):
            y = r * self.cell_size
            pygame.draw.line(self.screen, (0, 0, 0), (0, y), (self.cols*self.cell_size, y))

    def toggle_cell_at_pixel(self, x, y):
        col = x // self.cell_size
        row = y // self.cell_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.cells[row][col] = not self.cells[row][col]

    def next_generation(self):
        new_cells = []
        for row in range(self.rows):
            new_row = []
            for col in range(self.cols):
                new_row.append(False)
            new_cells.append(new_row)

        for r in range(self.rows):
            for c in range(self.cols):
                alive_neighbors = self.count_alive_neighbors(r, c)

                if self.cells[r][c]:
                    if alive_neighbors == 2 or alive_neighbors == 3:
                        new_cells[r][c] = True
                else:
                    if alive_neighbors == 3:
                        new_cells[r][c] = True

        self.cells = new_cells


    def count_alive_neighbors(self, row, col):
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r = row + dr
                c = col + dc
                if 0 <= r < self.rows and 0 <= c < self.cols and self.cells[r][c]:
                    count += 1
        return count


board = Grid(ROWS, COLS, CELL_SIZE)
running = True
paused = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            board.toggle_cell_at_pixel(x, y)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_r:
                new_cells = []
                for row in range(ROWS):
                    row_list = []
                    for col in range(COLS):
                        row_list.append(False)
                    new_cells.append(row_list)
                board.cells = new_cells

    if not paused:
        board.next_generation()

    board.draw_grid()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
