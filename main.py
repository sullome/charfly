#!/usr/bin/python
from gi.repository import Gtk, Pango
from random import choice, randrange
from jang.main import single_name
import xml.etree.ElementTree as ET

DATA_DIR = '/home/none/prj/fast-char/'

class FastCharacter(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)

        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        self.nations = self.drop_down('Национальность', self.NATIONS, vbox)
        self.gender = self.drop_down('Пол', self.GENDERS, vbox)
        self.type_ = self.drop_down('Архетип', self.TYPES, vbox)
        self.level = self.drop_down('Ранг', self.LEVELS, vbox, False)

        generate = Gtk.Button('Сгенерировать')
        generate.connect('clicked', self.generate_character)

        vbox.pack_start(generate, True, True, 6)

        left_text = self.textfield()
        self.result = left_text.get_buffer()
        self.result.create_tag('i', style = Pango.Style.ITALIC)

        right_text = self.textfield()
        self.stats = right_text.get_buffer()

        hbox = Gtk.Box(spacing = 1)
        hbox.pack_start(vbox, False, False, 5)
        hbox.pack_start(left_text, True, True, 0)
        hbox.pack_start(right_text, True, True, 0)

        self.add(hbox)

    NATIONS = {'eu_white': 'Белый',
               'latin': 'Latin',
               'eu_afro': 'Негр',
               'chinese': 'Китай'
               }
    GENDERS = {'male': 'Мужской', 'female': 'Женский'}
    TYPES = {'gunslinger': 'Стрелок',
             'huckster': 'Картёжник',
             'doctor': 'Доктор',
             'leader': 'Командир',
             'civil': 'Цивил'
             }
    LEVELS = {'1newbie': 'Новичок',
              '2seasoned': 'Закалённый',
              '3veteran': 'Ветеран',
              '4hero': 'Герой',
              '5legend': 'Легенда'
              }

    FILES_EU = ('eng', 'franch', 'german', 'ital')
    FILES_LAT = ('ital', 'spanish')

    MID_AGE = 30

    def drop_down(self, label, values, container, can_be_random = True):
        lbl = Gtk.Label(label)
        lbl.set_justify(Gtk.Justification.LEFT)

        cb = Gtk.ComboBoxText()

        if can_be_random: cb.append('random', 'Случайно')

        pairs = sorted(values.items())
        for pair in pairs:
            cb.append(*pair)

        cb.set_active(0)

        box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 4)
        box.pack_start(lbl, True, True, 0)
        box.pack_start(cb, False, False, 0)

        container.pack_start(box, True, False, 0)

        return cb

    def textfield(self):
        txt = Gtk.TextView()
        txt.set_editable(False)
        txt.set_cursor_visible(False)
        txt.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        return txt

    def get_value(self, in_widget, values):
        in_id = in_widget.get_active_id()
        if in_id == 'random':
            return choice(list(values.keys()))
        else:
            return in_id

    def get_vals(self, path):
        result = []
    
        tree = ET.parse(path)
        root = tree.getroot()
    
        for type_ in root:
            tag = type_.tag.capitalize().translate(str.maketrans('_', ' '))
            txt = choice(list(type_)).text
            result.append('{}: {}'.format(tag, txt))
    
        emph = choice(result)
    
        result = '\n'.join(result)
    
        return (result, emph)

    def get_se(self, text):
        return self.result.get_start_iter().forward_search(text,
                Gtk.TextSearchFlags.TEXT_ONLY)

    #def get_age(self, mid = self.MID_AGE):
        #age = mid + dF + d10

    def generate_character(self, widget):
        global DATA_DIR
        nation = self.get_value(self.nations, self.NATIONS)
        gender = self.get_value(self.gender, self.GENDERS)
        type_  = self.get_value(self.type_, self.TYPES)
        level  = self.level.get_active_id()[1:]

        if nation[:2] == 'eu':
            nation = choice(self.FILES_EU) 
        elif nation == 'latin':
            nation = choice(self.FILES_LAT)

        name = single_name(nation, gender)

        #age = get_age()

        m, m_emph = self.get_vals(DATA_DIR + 'mannerisms.xml')
        f, f_emph = self.get_vals(DATA_DIR + 'first-impressions.xml')

        self.result.set_text(
            '{}\n{} {}\n\n{}\n\n{}'.format(
            name, nation, gender, m, f
            )
        )

        s, e = self.get_se(m_emph)
        self.result.apply_tag_by_name('i', s, e)

        s, e = self.get_se(f_emph)
        self.result.apply_tag_by_name('i', s, e)

        with open('{}skeleton/{}_{}.txt'.format(DATA_DIR, type_, level)) as f:
            self.stats.set_text(f.read())

def main ():
    win = FastCharacter()
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == '__main__':
    main()

