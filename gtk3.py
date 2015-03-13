#!/usr/bin/python
from gi.repository import Gtk, Pango
from random import choice
import main as charfly
from jang import get_allnat

class FastCharacter(Gtk.Window):
    NATIONS = get_allnat()
    GENDERS = ['male', 'female']
    MID_AGE = 30

    def __init__(self):
        Gtk.Window.__init__(self)

        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        self.nations = self.drop_down('Национальность', self.NATIONS, vbox)
        self.gender = self.drop_down('Пол', self.GENDERS, vbox)

        self.age = self.input_num('Средний возраст', self.MID_AGE, 1, 100, vbox)
        self.count = self.input_num('Количество', 1, 1, 100, vbox)

        generate = Gtk.Button('Сгенерировать')
        generate.connect('clicked', self.generate_character)

        vbox.pack_start(generate, True, True, 6)

        text = Gtk.TextView()
        text.set_editable(False)
        text.set_cursor_visible(False)
        text.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.result = text.get_buffer()

        scroll = Gtk.ScrolledWindow()
        scroll.add(text)

        text_margin = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        text_margin.pack_start(scroll, True, True, 3)

        hbox = Gtk.Box(spacing = 1)
        hbox.pack_start(vbox, False, False, 5)
        hbox.pack_start(text_margin, True, True, 3)

        self.add(hbox)

    def drop_down(self, label, values, container, can_be_random = True):
        lbl = Gtk.Label(label)
        lbl.set_justify(Gtk.Justification.LEFT)

        cb = Gtk.ComboBoxText()

        if can_be_random: cb.append('random', 'Random')

        for val in values:
            cb.append(val, val.capitalize())

        cb.set_active(0)

        box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 4)
        box.pack_start(lbl, True, True, 0)
        box.pack_start(cb, False, False, 0)

        container.pack_start(box, True, False, 0)

        return cb

    def input_num(self, label, start, lower, upper, container):
        lbl = Gtk.Label(label)
        lbl.set_justify(Gtk.Justification.LEFT)

        adj = Gtk.Adjustment(start, lower, upper, 1, 10, 0)
        num = Gtk.SpinButton()
        num.set_adjustment(adj)
        num.set_value(start)
        num.set_numeric(True)

        box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 4)
        box.pack_start(lbl, True, True, 0)
        box.pack_start(num, False, False, 0)

        container.pack_start(box, True, False, 0)

        return num

    def get_value(self, in_widget, values):
        in_ = in_widget.get_active_id()
        if in_== 'random':
            return values
        else:
            return in_

    def generate_character(self, widget):
        nations = self.get_value(self.nations, self.NATIONS)
        genders = self.get_value(self.gender, self.GENDERS)
        count = self.count.get_value_as_int()
        age = self.age.get_value_as_int()

        characters = charfly.create(nations, genders, age, count)
        if count > 1: 
            text = charfly.decorate(characters, False)
        else:
            text = charfly.decorate(characters)
        self.result.set_text(text)
        return None

def main():
    win = FastCharacter()
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == '__main__':
    main()
