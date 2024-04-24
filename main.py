import game
import gui


def main():
    _bot = game.bot.Bot()
    _bot2 = game.bot.Bot()
    _gui = gui.main.Gui(_bot, _bot2)
    #_gui.mainloop()
    print('result:', _gui.bots_duel())


if __name__ == "__main__":
    main()
