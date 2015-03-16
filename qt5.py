#!/usr/bin/python
import main as charfly
from jang import get_allnat

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QGroupBox

class OptionList(QGroupBox):
    def __init__(self, label, options):
        QGroupBox.__init__(self, label = label)

        self.box = QVBoxLayout()
        self.values = []

        self.add_options(options)
        self.setLayout(self.box)

    def get_all_active():
        active = [option.text().lower()
            for option
            in self.values
            if option.isChecked()
            ]
        return active

    def add_options(options):
        for option in options:
            option = QCheckBox(option.capitalize())
            self.values.append(option)
            self.box.addWidget(option)

class CharflyQt(QWidget):
    def __init__(self, parent = None):
        super(CharflyQt, self).__init__(parent)

        self.MID_AGE = 30

        self.nations = OptionList('Национальность', get_allnat())
        self.genders = OptionList('Пол', ['male', 'female'])

        self.age = QSpinBox()
        self.age.setRange(1, 100)
        self.age.setValue(self.MID_AGE)
        self.count = QSpinBox()
        self.count.setRange(1, 100)

        form = QFormLayout()
        form.addRow('Средний возраст', self.age)
        form.addRow('Количество', self.count)

        generate = QPushButton('Сгенерировать')
        generate.clicked.connect(self.generate_character())

        vbox = QVBoxLayout()
        vbox.addWidget(form)
        vbox.addWidget(self.nations)
        vbox.addWidget(self.genders)
        vbox.addWidget(generate)
