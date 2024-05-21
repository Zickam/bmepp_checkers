from game.main import GameState

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
from gui.constants import BUTTONS_FONT_PATH, BC, WC, WIN_SIZE, RC

pg.init()
button_font = pg.font.Font(BUTTONS_FONT_PATH, WIN_SIZE[1] // 18)
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
    def __init__(self, coordinates: (int, int),
                 text: str,
                 size: (int, int),
                 is_black: bool,
                 stroke=True,
                 is_red=False):
        self.size = size
        self.is_black = is_black
        self.stroke = stroke
        self.is_red = is_red
        super().__init__(coordinates, text)

    def make_image(self) -> pg.Surface:
        image = pg.Surface(self.size)
        center_for_text = (self.size[0] // 2, self.size[1] // 2)
        if self.is_red:
            bg_color = RC
            text_color = WC
        else:
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
        if text_rect.left < 0:
            text_rect.move(-text_rect.left, 0)
        image.blit(text, text_rect)
        return image

    def collide_point(self, coordinates: (int, int)) -> bool:
        return self.rect.collidepoint(coordinates)


width, height = WIN_SIZE
caption_text = Text((width // 2, height // 6), 'Checkers', True)
play_white_button = Button((width // 3.6, height // 2.28), 'PLAY WHITE', (width // 2.857, height // 11.42), False)
play_black_button = Button((width // 1.37, height // 2.28), 'PLAY BLACK', (width // 2.857, height // 11.42), True)

player_player_button = Button((width // 3.6, height // 3.07), 'PVP', (width // 2.857, height // 11.42), True)
bot_bot_button = Button((width // 1.37, height // 3), 'BOTS', (width // 2.857, height // 11.42), False)

difficulty_text = Text((width // 2, height // 1.9), 'Difficulty')
minus_button = Button((width // 2.711, height // 1.7), '-', (width // 16, height // 16), True, False)
plus_button = Button((width // 1.61, height // 1.7), '+', (width // 16, height // 16), False, False)

training_button = Button((width // 2, height // 1.3), 'TRAINING', (width // 3.63, height // 11.4), False, True)
choosing_a_bot_button = Button((width // 2, height // 1.14), 'CHANGE BOT', (width // 3, height // 11.4), False, True)

restart_button = Button((width // 40, height // 40), 'R', (width // 20, height // 20), True, False)
help_button = Button((width // 1.024, height // 40), '?', (width // 20, height // 20), False, False, True)
help_buttons_animation = [
    Button((width // 1.024, height // 40), '!', (width // 20, height // 20), False, False, True),
    Button((width // 1.024, height // 40), '@', (width // 20, height // 20), False, False, True),
    Button((width // 1.024, height // 40), '#', (width // 20, height // 20), False, False, True),
    Button((width // 1.024, height // 40), '$', (width // 20, height // 20), False, False, True),
    Button((width // 1.024, height // 40), '%', (width // 20, height // 20), False, False, True),
    Button((width // 1.024, height // 40), '&', (width // 20, height // 20), False, False, True),
]
# Choosing a bot scene
choosing_main_text = Text((width//1.97, height//10), 'Bot side:')
white_side_text = Text((width//4, height//6), 'White')
black_side_text = Text((width//1.315, height//6), 'Black')
creating_new_bot_button = Button((width//2, height//1.17), 'Create new bot', (width//2, height//12.5), False)
turn_on_deleting_mode_button = Button((width//2, height//1.062), 'Delete mode', (width//2, height//12.5), False)
turn_off_deleting_mode_button = Button((width//2, height//1.062), 'Delete mode', (width//2, height//12.5), True)


def get_bots_variants_buttons(bots) -> list[Button]:
    buttons = []
    offset = height//12.5
    if len(bots) > 7:
        offset = height//(5.5+len(bots))
    y = height//3.5
    for i, b in enumerate(bots):
        if True:
            new_button = Button((width//4, y), b.name, (width//3, height//14), False)
            buttons.append(new_button)
        if True:
            new_button = Button((width//1.315, y), b.name, (width//3, height//14), False)
            buttons.append(new_button)
        y += offset
        if y > height // 1.25:
            break
    return buttons


def get_current_bots_name_texts(chosen1, chosen2, bots) -> list[Text]:
    bot1 = bots[chosen1]
    text1 = Text((width//4, height//4.5), bot1.name)
    bot2 = bots[chosen2]
    text2 = Text((width//1.315, height//4.5), bot2.name)
    return [text1, text2]


def get_difficulty_num(difficulty):
    return Text((width // 2, height // 1.7), f'{difficulty}')


def get_win_text(game_state: int):
    if game_state == 2:
        return Text((width // 2, height // 2), 'BLACK WIN!')
    elif game_state == 1:
        return Text((width // 2, height // 2), 'WHITE WIN!')
    else:
        return Text((width // 2, height // 2), 'DRAW! HAHA')
