from PySide6.QtWidgets import *
from scripts.gui import ContactBookGUI


def main():
    gui = ContactBookGUI()
    gui.MainWindow.show()


if __name__ == "__main__":
    main()
