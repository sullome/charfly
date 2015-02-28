#!/usr/bin/python
import os.path as path
import xml.etree.ElementTree as ET
from random import choice, randint
import gettext
from jang.main import single_name

gettext.install('charfly', '/home/none/prj/charfly/locale')

split_words = lambda s: s.capitalize().translate(str.maketrans('_', ' '))

def get_data():
    return '/home/none/prj/charfly'

def get_age(mid):
    # mid + 10* (4df) + d10
    age = 0
    while age <= 0:
        age = mid + sum(choice([-10, 0, 10]) for i in range(4)) + randint(1,10)
    return age

def xml2opt(path):
    result = []

    tree = ET.parse(path)
    root = tree.getroot()

    for type_ in root:
        tag = split_words(_(type_.tag))
        txt = _(choice(list(type_)).text)
        result.append('{}: {}'.format(tag, txt))

    emph = choice(result)
    result.remove(emph)

    return (emph, result)

def create(nation, gender, mid_age, datapath = get_data()):
    name = single_name(nation, gender)
    age = get_age(mid_age)
    mannerism, m_other = xml2opt(
        path.join(datapath, 'mannerisms.xml')
    )
    first_impression, f_other = xml2opt(
        path.join(datapath, 'first-impressions.xml')
    )
    return (name, age, mannerism, m_other, first_impression, f_other)

def decorate(char):
    return ('{0[0]} ({0[1]})'
        '\n\n{0[2]}'
        '\n{3}:\n    {1}'
        '\n\n{0[4]}'
        '\n{3}:\n    {2}').format(
            char,
            '\n    '.join(char[3]),
            '\n    '.join(char[5]),
            _('Other')
        ) 

def main ():
    character = create('eng', 'male', 30, '/home/none/prj/charfly')
    print(decorate(character))

if __name__ == '__main__':
    main()
