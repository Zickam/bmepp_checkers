import string

import pygame as pg
pg.init()
import time
from constants import *
from game import Game


class Gui:
    def __init__(self, game):
        self.__game = game
        self.__clock = pg.time.Clock()
        self.frame_start = time.time()

        self.__screen = pg.display.set_mode(WIN_SIZE)
        self.make_sprites()

    def make_sprites(self):
        self.__board_sprite = self.make_board()

    def make_board(self):
        Alph = string.ascii_lowercase
        Nums = [str(x) for x in range(1, 27)]

        height = WIN_SIZE[1]
        offset_size = height // 20
        font_size = offset_size // 2
        cell_size = (height - 2 * offset_size) // CELLS_NUMBER
        font = pg.font.Font('font.ttf', font_size)
        image = pg.Surface((height, height))
        image.fill(WCC)

        left = top = offset_size - 2
        board_rect_size = CELLS_NUMBER * cell_size + 4
        pg.draw.rect(image, BBC, (left, top, board_rect_size, board_rect_size))

        # draw background
        for i in range(CELLS_NUMBER):
            for j in range(CELLS_NUMBER):
                x = i * cell_size + offset_size
                y = j * cell_size + offset_size
                color = WCC if (i + j) % 2 == 0 else BCC
                pg.draw.rect(image, color, (x, y, cell_size, cell_size))

        # draw text
        text_offset = offset_size // 2
        text_offset2 = text_offset + CELLS_NUMBER * cell_size + offset_size
        for i in range(CELLS_NUMBER):
            char = font.render(Alph[i], True, BCC)
            x = (i + .5) * cell_size + offset_size
            x -= char.get_width() // 2
            uy = text_offset - char.get_height() // 2
            by = text_offset2 - char.get_height() // 2
            image.blit(char, (x, uy))
            char = pg.transform.rotate(char, 180)
            image.blit(char, (x, by))

            num = font.render(Nums[CELLS_NUMBER-i-1], True, BBC)
            lx = text_offset - char.get_height() // 2
            rx = text_offset2 - char.get_height() // 2
            y = (i + .5) * cell_size + offset_size
            y -= char.get_width() // 2
            num = pg.transform.rotate(num, 90)
            image.blit(num, (lx, y))
            num = pg.transform.rotate(num, 180)
            image.blit(num, (rx, y))
        return image

    def mainloop(self):
        while True:
            self.render()
            self.handle_events()

            self.__clock.tick(FPS)

    def render(self):
        board_sprite_x = WIN_SIZE[0] - self.__board_sprite.get_width()
        self.__screen.blit(self.__board_sprite, (board_sprite_x, 0))
        pg.display.update()

    def handle_events(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.close()
            if event.type == pg.MOUSEBUTTONUP:
                if event.button in (1, 3):  # RMB, LMB
                    pass

    def close(self):
        exit()

def main():
    game = Game()
    gui = Gui(game)
    gui.mainloop()


if __name__ == "__main__":
    main()
