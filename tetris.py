import random
import pygame

colors = [
    (0, 0, 0),
    (3, 56, 174),
    (114, 203, 59),
    (255, 213, 0),
    (255, 151, 28),
    (255, 50, 19),
]


class Block:
    x_in_grids = 0
    y_in_grids = 0
    blocks = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 6]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
    ]

    def __init__(self, x, y):
        self.x_in_grids = x
        self.y_in_grids = y
        self.type = random.randint(0, len(self.blocks) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def block(self):
        return self.blocks[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.blocks[self.type])


class Tetris:
    position_x = 100
    position_y = 10
    score = 0
    state = "running"
    game_level = 2
    grids = []
    height = 0
    width = 0
    grid_size = 30
    block = None

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.grids = []
        self.state = "running"
        self.score = 0
        for row in range(height):
            new_line = []
            for column in range(width):
                new_line.append(0)
            self.grids.append(new_line)

    def new_block(self):
        self.block = Block(3, 0)

    def go_down(self):
        self.block.y_in_grids += 1
        if self.is_intersected():
            self.block.y_in_grids -= 1
            self.freeze()

    def is_intersected(self):
        intersection = False
        for row in range(4):
            for column in range(4):
                i = row * 4 + column
                if i in self.block.block():
                    if column + self.block.x_in_grids > self.width - 1 or column + self.block.x_in_grids < 0 \
                            or row + self.block.y_in_grids > self.height - 1 or \
                            self.grids[row + self.block.y_in_grids][column + self.block.x_in_grids] > 0:
                        intersection = True
        return intersection

    def freeze(self):
        for row in range(4):
            for column in range(4):
                if row * 4 + column in self.block.block():
                    self.grids[row + self.block.y_in_grids][column + self.block.x_in_grids] = self.block.color
        self.break_lines()
        self.new_block()
        if self.is_intersected():
            self.state = "game_over"

    def rotate(self):
        self.block.rotate()

    def go_side(self, dx):
        old_x = self.block.x_in_grids
        self.block.x_in_grids += dx
        if self.is_intersected():
            self.block.x_in_grids = old_x

    def go_space(self):
        while not self.is_intersected():
            self.block.y_in_grids += 1
        self.block.y_in_grids -= 1
        self.freeze()

    def break_lines(self):
        lines = 0
        for row in range(1, self.height):
            zeros = 0
            for column in range(self.width):
                if self.grids[row][column] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for r_b2t in range(row, 1, -1):
                    for column in range(self.width):
                        self.grids[r_b2t][column] = self.grids[r_b2t - 1][column]
        self.score += lines ** 2


WHITE = (255, 255, 255)
GRAY = (194, 194, 194)
BLACK = (0, 0, 0)
SCREEN_SIZE = (500, 620)
game_over = False
fps = 25
clock = pygame.time.Clock()
counter = 0
pressing_down = False
game = Tetris(20, 10)
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Tetris/俄羅斯方塊")
while not game_over:
    if game.block is None:
        game.new_block()
    counter += 1
    if counter > 10000:
        counter = 0
    if pressing_down or counter % (fps // game.game_level // 2) == 0:
        if game.state == "running":
            game.go_down()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_ESCAPE:
                game.__init__()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False
    screen.fill(WHITE)
    for row in range(game.height):
        for column in range(game.width):
            pygame.draw.rect(screen, GRAY, [
                game.position_x + game.grid_size * column,
                game.position_y + game.grid_size * row,
                game.grid_size, game.grid_size
            ], 1)
            if game.grids[row][column] > 0:
                pygame.draw.rect(screen, colors[game.grids[row][column]], [
                    game.position_x + game.grid_size * column + 1,
                    game.position_y + game.grid_size * row + 1,
                    game.grid_size - 2, game.grid_size - 2
                ])

    if game.block is not None:
        for row in range(4):
            for column in range(4):
                if row * 4 + column in game.block.block():
                    pygame.draw.rect(screen, colors[game.block.color],
                                     [game.position_x + game.grid_size * (column + game.block.x_in_grids) + 1,
                                      game.position_y + game.grid_size * (row + game.block.y_in_grids) + 1,
                                      game.grid_size - 2, game.grid_size - 2])
    font_score = pygame.font.SysFont('Courier', 20, True, True)
    font_game_over = pygame.font.SysFont('Times', 40, True, True)
    font_esc = pygame.font.SysFont('Times', 30, True, True)
    text_score = font_score.render("Score: {}".format(str(game.score)), True, BLACK)
    text_game_over = font_game_over.render("Game Over", True, BLACK)
    text_esc = font_esc.render("Press ESC to start over", True, BLACK)
    screen.blit(text_score, [20, 20])
    if game.state == "game_over":
        screen.blit(text_game_over, [140, 200])
        screen.blit(text_esc, [80, 360])
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
