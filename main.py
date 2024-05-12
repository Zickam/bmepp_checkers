import game.bot
import gui


def main():
    _bot = game.bot.Bot()
    _bot2 = game.bot.Bot()
    _gui = gui.main.Gui(_bot, _bot2, with_display=True)
    _gui.mainloop()
    # _gui.change_bots(_bot, _bot2)
    # print('result:', _gui.bots_duel(-1))


if __name__ == "__main__":
    main()

