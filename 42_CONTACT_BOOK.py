# import sys
# path = r"E:\Documents_Files\RobinData\PYTHON\RawDataofpy"
# sys.path.append(path)

from PySide6.QtWidgets import *
from CONTACT_BOOK_GUI import ContactBookGUI
from CONTACT_BOOK_MANAGER import ContactBookManager


def main():

    gui = ContactBookGUI()
    manager = ContactBookManager
    gui.MainWindow.show()

if __name__ == "__main__":
    main()
