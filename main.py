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

def xml2opt(path):
    result = []

    tree = ET.parse(path)
    root = tree.getroot()

    for type_ in root:
        tag = split_words(_(type_.tag))
        txt = _(choice(list(type_)).text)
        result.append((tag, txt))

    emph = choice(result)
    result.remove(emph)

    return (emph, result)

def get_age(mid):
    # mid + 10 * (4df) + d10
    age = 0
    while age <= 0:
        age = mid + sum(choice([-10, 0, 10]) for i in range(4)) + randint(1,10)
    return age

def get_first_reaction():
    tree = ET.parse('first-reactions.xml')
    root = tree.getroot()

    roll = randint(1,6) + randint(1,6)

    for reaction in root:
        if roll in range(int(reaction.get('start')), int(reaction.get('end')) + 1):
            tag = split_words(_(reaction.tag))
            return (reaction.tag, reaction.text)

def create(nation, gender, mid_age, datapath = get_data()):
    name = single_name(nation, gender)
    age = get_age(mid_age)
    mannerism, m_other = xml2opt(
        path.join(datapath, 'mannerisms.xml')
    )
    first_impression, f_other = xml2opt(
        path.join(datapath, 'first-impressions.xml')
    )
    first_reaction = get_first_reaction()
    return (name, age, nation, gender,
            mannerism, first_impression,
            m_other, f_other,
            first_reaction)

def create_decorated(nation, gender, mid_age, count, datapath = get_data()):
    if count < 1:
        return 'Unexpected value.'

    result = []
    for i in range(count):
        result.append(
            decorate(
                create(choice(nation), choice(gender), mid_age),
                full = False
                )
            )
    return '\n\n----\n\n'.join(result)

def decorate(char, full = True):
    if not full:
        return (
            '{0[0]} ({0[1]})\n'
            '{1}: {0[2]}, {2}: {0[3]}\n\n'
            '{3}: '
            '{0[4][1]} ({0[4][0]})\n'
            '{4}: '
            '{0[5][1]} ({0[5][0]})\n'
            '{5}: '
            '{0[8][0]}'
            ).format(
                char,
                _('Nation'),
                _('gender'),
                _('Mannerism'),
                _('First impression'),
                _('First reaction')
                )
    else:
        return (
            '{0[0]} ({0[1]})\n\n'
            '{3}: {0[2]}, {4}: {0[3]}\n\n'
            '{0[4][0]}: {0[4][1]}\n'
            '{5}:\n    '
            '{1}\n\n'
            '{0[5][0]}: {0[5][1]}\n'
            '{5}:\n    '
            '{2}\n\n'
            '{6}: '
            '{0[8][0]}\n{0[8][1]}'
            ).format(
                char,
                '\n    '.join('{0[0]}: {0[1]}'.format(t) for t in char[6]),
                '\n    '.join('{0[0]}: {0[1]}'.format(t) for t in char[7]),
                _('Nation'),
                _('gender'),
                _('Other'),
                _('First reaction')
                ) 

def main ():
    character = create('eng', 'male', 30, '/home/none/prj/charfly')
    print(decorate(character))

if __name__ == '__main__':
    #main()
    print(get_first_reaction())
