# -*- coding: utf-8 -*-

"""
Example usage:
my_ascii_turkish_txt = "Opusmegi cagristiran catirtilar."
deasciifier = Deasciifier(my_ascii_turkish_txt)
my_deasciified_turkish_txt = deasciifier.convert_to_turkish()
print(my_deasciified_turkish_txt)
This system is based on the turkish-mode by Dr. Deniz Yüret
Python Code by Emre Sevinç
"""

import pickle
from trnlp.helper import package_path

__all__ = ['Deasciifier']

ascii_pickle_path = package_path() + 'data/ascii_to_str_dict.pickle'


class Deasciifier:
    with open(ascii_pickle_path, 'rb') as f:
        turkish_pattern_table = pickle.load(f)
    del f

    turkish_context_size = 10

    turkish_asciify_table = {u'ç': u'c',
                             u'Ç': u'C',
                             u'ğ': u'g',
                             u'Ğ': u'G',
                             u'ö': u'o',
                             u'Ö': u'O',
                             u'ü': u'u',
                             u'Ü': u'U',
                             u'ı': u'i',
                             u'İ': u'I',
                             u'ş': u's',
                             u'Ş': u'S'}

    turkish_downcase_asciify_table = {'H': 'h', 'C': 'c', 'm': 'm', 'ı': 'i', 'q': 'q', 'İ': 'i', 'N': 'n', 'U': 'u',
                                      'Ç': 'c', 'i': 'i', 'G': 'g', 'I': 'i', 'w': 'w', 'k': 'k', 'o': 'o', 'a': 'a',
                                      'D': 'd', 'p': 'p', 'Ö': 'o', 'W': 'w', 'd': 'd', 'S': 's', 'Q': 'q', 'Y': 'y',
                                      't': 't', 'A': 'a', 'l': 'l', 'f': 'f', 'ç': 'c', 'P': 'p', 'J': 'j', 's': 's',
                                      'b': 'b', 'ü': 'u', 'r': 'r', 'x': 'x', 'B': 'b', 'v': 'v', 'j': 'j', 'K': 'k',
                                      'h': 'h', 'F': 'f', 'Ü': 'u', 'T': 't', 'Ğ': 'g', 'ş': 's', 'z': 'z', 'g': 'g',
                                      'V': 'v', 'n': 'n', 'ö': 'o', 'O': 'o', 'ğ': 'g', 'c': 'c', 'R': 'r', 'y': 'y',
                                      'Ş': 's', 'M': 'm', 'E': 'e', 'u': 'u', 'X': 'x', 'Z': 'z', 'e': 'e', 'L': 'l'}

    turkish_upcase_accents_table = {'E': 'e', 'Ü': 'U', 'ğ': 'G', 'X': 'x', 'ü': 'U', 'o': 'o', 'M': 'm', 'Ç': 'C',
                                    'm': 'm', 'L': 'l', 'u': 'u', 's': 's', 'H': 'h', 'C': 'c', 'y': 'y', 'T': 't',
                                    'V': 'v', 'N': 'n', 'B': 'b', 'j': 'j', 'Ğ': 'G', 'J': 'j', 'x': 'x', 'v': 'v',
                                    'O': 'o', 'A': 'a', 'F': 'f', 'Q': 'q', 'w': 'w', 'r': 'r', 'ı': 'I', 'Z': 'z',
                                    'p': 'p', 'U': 'u', 'P': 'p', 't': 't', 'g': 'g', 'ç': 'C', 'Y': 'y', 'Ş': 'S',
                                    'I': 'i', 'e': 'e', 'h': 'h', 'İ': 'i', 'z': 'z', 'd': 'd', 'K': 'k', 'k': 'k',
                                    'l': 'l', 'f': 'f', 'G': 'g', 'n': 'n', 'D': 'd', 'c': 'c', 'i': 'i', 'ş': 'S',
                                    'W': 'w', 'q': 'q', 'R': 'r', 'Ö': 'O', 'S': 's', 'ö': 'O', 'b': 'b', 'a': 'a'}

    def __init__(self, ascii_string):
        self.ascii_string = ascii_string
        self.turkish_string = ascii_string

    def print_turkish_string(self):
        print(self.turkish_string)

    @staticmethod
    def set_char_at(mystr, pos, c):
        return mystr[0:pos] + c + mystr[pos + 1:]

    def convert_to_turkish(self):
        # Convert a string with ASCII-only letters into one with Turkish letters.
        for i in range(len(self.turkish_string)):
            c = self.turkish_string[i]
            if self.turkish_need_correction(c, point=i):
                self.turkish_string = self.set_char_at(self.turkish_string, i, self.turkish_toggle_accent(c))
            else:
                self.turkish_string = self.set_char_at(self.turkish_string, i, c)

        return self.turkish_string

    @staticmethod
    def turkish_toggle_accent(c):
        turkish_toggle_accent_table = {
                u'c': u'ç',
                u'C': u'Ç',
                u'g': u'ğ',
                u'G': u'Ğ',
                u'o': u'ö',
                u'O': u'Ö',
                u'u': u'ü',
                u'U': u'Ü',
                u'i': u'ı',
                u'I': u'İ',
                u's': u'ş',
                u'S': u'Ş',
                u'ç': u'c',
                u'Ç': u'C',
                u'ğ': u'g',
                u'Ğ': u'G',
                u'ö': u'o',
                u'Ö': u'O',
                u'ü': u'u',
                u'Ü': u'U',
                u'ı': u'i',
                u'İ': u'I',
                u'ş': u's',
                u'Ş': u'S'
        }
        return turkish_toggle_accent_table.get(c, c)

    def turkish_need_correction(self, char, point=0):
        # Determine if char at cursor needs correction.
        ch = char
        tr = Deasciifier.turkish_asciify_table.get(ch, ch)
        pl = Deasciifier.turkish_pattern_table.get(tr.lower(), False)

        if pl:
            m = self.turkish_match_pattern(pl, point)
        else:
            m = False

        if tr == u'I':
            if ch == tr:
                return not m
            else:
                return m
        else:
            if ch == tr:
                return m
            else:
                return not m

    def turkish_match_pattern(self, dlist, point=0):
        # Check if the pattern is in the pattern table.
        rank = 2 * len(dlist)
        str_char = self.turkish_get_context(Deasciifier.turkish_context_size, point=point)
        start = 0

        _len = len(str_char)
        while start <= Deasciifier.turkish_context_size:
            end = 1 + Deasciifier.turkish_context_size
            while end <= _len:
                s = str_char[start:end]
                r = dlist.get(s, False)
                if r and abs(r) < abs(rank):
                    rank = r
                end = 1 + end
            start = 1 + start

        return rank > 0

    def turkish_get_context(self, size=turkish_context_size, point=0):
        s = ' ' * (1 + (2 * size))
        s = s[0:size] + 'X' + s[size + 1:]
        i = 1 + size
        space = False
        index = point
        index = index + 1

        while i < len(s) and not space and index < len(self.ascii_string):
            current_char = self.turkish_string[index]
            x = Deasciifier.turkish_downcase_asciify_table.get(current_char, False)
            if not x:
                if not space:
                    i = i + 1
                    space = True
            else:
                s = s[0:i] + x + s[i + 1:]
                i = i + 1
                space = False
            index = index + 1

        s = s[0:i]

        index = point
        i = size - 1
        space = False

        index = index - 1
        while i >= 0 and index >= 0:
            current_char = self.turkish_string[index]
            x = Deasciifier.turkish_upcase_accents_table.get(current_char, False)
            if not x:
                if not space:
                    i = i - 1
                    space = True
            else:
                s = s[0:i] + x + s[i + 1:]
                i = i - 1
                space = False
            index = index - 1

        return s


if __name__ == '__main__':
    my_ascii_turkish_txt = "Opusmegi cagristiran catirtilar."
    deasciifier = Deasciifier(my_ascii_turkish_txt)
    my_deasciified_turkish_txt = deasciifier.convert_to_turkish()
    print(my_deasciified_turkish_txt)
