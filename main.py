import game
import gui


def main():
    _game = game.main.Game()
    _gui = gui.main.Gui(_game)
    _gui.mainloop()


if __name__ == "__main__":
    main()
