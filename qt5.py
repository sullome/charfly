#!/usr/bin/python
import main as charfly
from jang import get_allnat

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

class OptionList():
    def __init__(self, options = None, parent = None):
        #super(OptionList, self).__init__(parent)

        self.values = dict()

    def get_all_active():
        pass

    def add_options(options):
        pass

class CharflyQt(QWidget):
    def __init__(self, parent = None):
        super(CharflyQt, self).__init__(parent)

        self.NATIONS = get_allnat()
        self.GENDERS = ['male', 'female']
        self.MID_AGE = 30

        lbl = QLabel('Национальность')
