#!/usr/bin/python
import main as charfly

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget,
        QGroupBox, QVBoxLayout, QHBoxLayout, QFormLayout,
        QCheckBox, QSpinBox, QPushButton, QTextEdit)

class OptionList(QGroupBox):
    def __init__(self, label, options):
        QGroupBox.__init__(self, label)

        self.box = QVBoxLayout()
        self.values = []

        self.add_options(options)
        self.setLayout(self.box)

    def get_all_active(self):
        active = [option.text().lower()
            for option
            in self.values
            if option.isChecked()
            ]
        return active

    def add_options(self, options):
        for option in options:
            option = QCheckBox(option.capitalize())
            self.values.append(option)
            self.box.addWidget(option)

class CharflyQt(QWidget):
    def __init__(self, parent = None):
        super(CharflyQt, self).__init__(parent)

        self.MID_AGE = 30

        self.nations = OptionList('Национальность', charfly.get_allnat())
        self.genders = OptionList('Пол', ['male', 'female'])

        self.age = QSpinBox()
        self.age.setRange(1, 100)
        self.age.setValue(self.MID_AGE)
        self.count = QSpinBox()
        self.count.setRange(1, 100)

        form = QWidget()
        layout = QFormLayout()
        layout.addRow('Средний возраст', self.age)
        layout.addRow('Количество', self.count)
        form.setLayout(layout)

        generate = QPushButton('Сгенерировать')
        generate.clicked.connect(self.generate_character)

        self.result = QTextEdit()

        vbox = QVBoxLayout()
        vbox.addWidget(self.nations)
        vbox.addWidget(self.genders)
        vbox.addWidget(form)
        vbox.addWidget(generate)

        hbox = QHBoxLayout()

        left = QWidget()
        left.setLayout(vbox)
        right = self.result

        hbox.addWidget(left)
        hbox.addWidget(right)

        self.setLayout(hbox)
        self.setWindowTitle('Charfly')

    def generate_character(self):
        nations = self.nations.get_all_active()
        genders = self.genders.get_all_active()
        age = self.age.value()
        count = self.count.value()
        
        characters = charfly.create(nations, genders, age, count)
        text = charfly.decorate(characters, count <= 1)
        self.result.setPlainText(text)

        return None

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    charfly_window = CharflyQt()
    charfly_window.show()
    sys.exit(app.exec_())
