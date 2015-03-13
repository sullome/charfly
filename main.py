#!/usr/bin/python
from rollingdice.fudge import fudge
from rollingdice.main import dice

import os.path as path
import xml.etree.ElementTree as ET
from random import choice
import gettext

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
        age = mid + 10 * fudge(fancy = False) + dice(10)
    return age

def get_first_reaction():
    tree = ET.parse('first-reactions.xml')
    root = tree.getroot()

    reaction = root.find('*[@numeric="{}"]'.format(fudge(fancy = False)))
    tag = split_words(_(reaction.tag))
    description = _(reaction.text).strip()
    return (tag, description)

def create(nations, genders, mid_age, count = 1, datapath = get_data()):
    from jang import single_name

    result = []

    for i in range(count):
        nation = choice(nations)
        gender = choice(genders)
        age = get_age(mid_age)

        name = single_name(nation, gender)

        mannerism, m_other = xml2opt(
            path.join(datapath, 'mannerisms.xml')
        )
        first_impression, f_other = xml2opt(
            path.join(datapath, 'first-impressions.xml')
        )
        first_reaction = get_first_reaction()

        result.append((name, age, nation, gender,
            mannerism, first_impression,
            m_other, f_other,
            first_reaction))
    return result

def decorate(chars, full = True):
    result = []
    for char in chars:
        if not full:
            result.append((
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
            )
        else:
            result.append((
                '{0[0]} ({0[1]})\n\n'
                '{3}: {0[2]}, {4}: {0[3]}\n\n'
                '{0[4][0]}: {0[4][1]}\n'
                '{5}:\n    '
                '{1}\n\n'
                '{0[5][0]}: {0[5][1]}\n'
                '{5}:\n    '
                '{2}\n\n'
                '{6}: '
                '{0[8][0]}\n    {0[8][1]}'
                ).format(
                    char,
                    '\n    '.join('{0[0]}: {0[1]}'.format(t) for t in char[6]),
                    '\n    '.join('{0[0]}: {0[1]}'.format(t) for t in char[7]),
                    _('Nation'),
                    _('gender'),
                    _('Other'),
                    _('First reaction')
                    ) 
            )
    return '\n\n-----\n\n'.join(result)

def main ():
    character = create('eng', 'male', 30, '/home/none/prj/charfly')
    print(decorate(character))

if __name__ == '__main__':
    main()
