from game import Game
from gui.gui import Gui


def main():
    game = Game()
    gui = Gui(game)
    gui.mainloop()


if __name__ == "__main__":
    main()
