import pygame as pg
from gui.constants import BUTTONS_FONT_PATH, GC, BC, WC, WIN_SIZE

pg.init()
button_font = pg.font.Font(BUTTONS_FONT_PATH, WIN_SIZE[1] // 17)
caption_font = pg.font.Font(BUTTONS_FONT_PATH, WIN_SIZE[1] // 5)


class Text:
    def __init__(self, coordinates: (int, int), text: str, big=False):
        self.coordinates = coordinates
        self.text = text
        self.big = big
        self.sprite = self.make_image()
        self.rect = self.sprite.get_rect(center=coordinates)

    def make_image(self) -> pg.Surface:
        if self.big:
            image = caption_font.render(self.text, 1, BC)
        else:
            image = button_font.render(self.text, 1, BC)
        return image

    def render(self, screen: pg.Surface):
        screen.blit(self.sprite, self.rect)


class Button(Text):
    def __init__(self, coordinates: (int, int), text: str, size: (int, int), is_black: bool, stroke=True):
        self.size = size
        self.is_black = is_black
        self.stroke = stroke
        super().__init__(coordinates, text)

    def make_image(self) -> pg.Surface:
        image = pg.Surface(self.size)
        center_for_text = (self.size[0] // 2, self.size[1] // 2)
        if self.is_black:
            bg_color = BC
            text_color = WC
        else:
            bg_color = WC
            text_color = BC
        if self.stroke:
            image.fill(text_color)
        else:
            image.fill(bg_color)
        pg.draw.rect(image, bg_color, (2, 2, self.size[0] - 4, self.size[1] - 4))
        text = button_font.render(self.text, 1, text_color)
        text_rect = text.get_rect(center=center_for_text)
        image.blit(text, text_rect)
        return image

    def collide_point(self, coordinates: (int, int)) -> bool:
        return self.rect.collidepoint(coordinates)


caption_text = Text((400, 100), 'Checkers', True)
play_white_button = Button((200, 300), 'PLAY WHITE', (280, 70), False)
play_black_button = Button((600, 300), 'PLAY BLACK', (280, 70), True)
difficulty_text = Text((400, 500), 'Difficulty')
minus_button = Button((295, 550), '-', (50, 50), True, False)
plus_button = Button((495, 550), '+', (50, 50), False, False)
restart_button = Button((20,20), 'R', (40,40), True, False)