import pygame as pg
import string
from gui.constants import WIN_SIZE, BCC, WCC, BBC, FONT_PATH, CBC, CWC, HRC
pg.init()


class Sprites:
    def __init__(self, CELLS_NUMBER):
        self.CELLS_NUMBER = CELLS_NUMBER
        self.height = WIN_SIZE[1]
        self.offset_size = self.height // 20
        self.font_size = self.offset_size // 2
        self.checker_scale = 2.8
        self.cell_size = (self.height - 2 * self.offset_size) // self.CELLS_NUMBER

        self.board = self.make_board()
        self.white_checker = self.make_checker(True, False)
        self.queen_white_checker = self.make_checker(True, True)
        self.black_checker = self.make_checker(False, False)
        self.queen_black_checker = self.make_checker(False, True)
        self.hint = self.make_hint()


    def make_board(self) -> pg.Surface:
        Alph = string.ascii_lowercase
        Nums = [str(x) for x in range(1, 27)]

        font = pg.font.Font(FONT_PATH, self.font_size)
        image = pg.Surface((self.height, self.height))
        image.fill(WCC)

        left = top = self.offset_size - 2
        board_rect_size = self.CELLS_NUMBER * self.cell_size + 4
        pg.draw.rect(image, BBC, (left, top, board_rect_size, board_rect_size))

        # draw background
        for i in range(self.CELLS_NUMBER):
            for j in range(self.CELLS_NUMBER):
                x = i * self.cell_size + self.offset_size
                y = j * self.cell_size + self.offset_size
                color = WCC if (i + j) % 2 == 0 else BCC
                pg.draw.rect(image, color, (x, y, self.cell_size, self.cell_size))

        # draw text
        text_offset = self.offset_size // 2
        text_offset2 = text_offset + self.CELLS_NUMBER * self.cell_size + self.offset_size
        for i in range(self.CELLS_NUMBER):
            char = font.render(Alph[i], True, BBC)
            x = (i + .5) * self.cell_size + self.offset_size
            x -= char.get_width() // 2
            uy = text_offset - char.get_height() // 2
            by = text_offset2 - char.get_height() // 2
            image.blit(char, (x, uy))
            char = pg.transform.rotate(char, 180)
            image.blit(char, (x, by))

            num = font.render(Nums[self.CELLS_NUMBER-i-1], True, BBC)
            lx = text_offset - char.get_height() // 2
            rx = text_offset2 - char.get_height() // 2
            y = (i + .5) * self.cell_size + self.offset_size
            y -= char.get_width() // 2
            num = pg.transform.rotate(num, 90)
            image.blit(num, (lx, y))
            num = pg.transform.rotate(num, 180)
            image.blit(num, (rx, y))
        return image

    def make_checker(self, is_white: bool, is_queen: bool) -> pg.Surface:
        if is_white:
            big_circle_color = CWC
            small_circle_color = CBC
        else:
            big_circle_color = CBC
            small_circle_color = CWC

        image = pg.Surface((self.cell_size, self.cell_size), pg.SRCALPHA)
        center = (self.cell_size // 2, self.cell_size // 2)
        pg.draw.circle(image, big_circle_color, center, self.cell_size // self.checker_scale)

        pg.draw.circle(image, small_circle_color, center, self.cell_size // self.checker_scale // 1.1, 3)
        if not is_queen:
            pg.draw.circle(image, small_circle_color, center, self.cell_size // self.checker_scale // 2, 3)
        return image

    def make_hint(self):
        image = pg.Surface((self.cell_size, self.cell_size), pg.SRCALPHA)
        center = (self.cell_size // 2, self.cell_size // 2)
        pg.draw.circle(image, HRC, center, self.cell_size // (self.checker_scale * 2))
        return image

    def get_coordinates(self, row: int, column: int, is_player_first = True) -> (int, int):
        if is_player_first:
            x = column * self.cell_size + self.offset_size
            y = row * self.cell_size + self.offset_size
        else:
            x = (self.CELLS_NUMBER - column - 1) * self.cell_size + self.offset_size
            y = (self.CELLS_NUMBER - row - 1) * self.cell_size + self.offset_size
        rect = pg.Rect(x, y, self.cell_size, self.cell_size)
        return rect


