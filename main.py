import game
import gui


def main():
    _bot = game.bot.Bot()
    # _bot2 = game.bot.Bot()
    _gui = gui.main.Gui(_bot)
    _gui.mainloop()


if __name__ == "__main__":
    main()
