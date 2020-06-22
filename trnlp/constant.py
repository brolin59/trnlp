#!/usr/local/bin/python
# -*- coding: utf-8 -*-

"""
This file is part of trnlp.

trnlp is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

trnlp is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with trnlp.  If not, see <https://www.gnu.org/licenses/>.
Copyright (c) 2016-2020, Esat Mahmut Bayol

The full license is in the file LICENSE.txt, distributed with this software.
"""

allLowerLetters = ('a', 'b', 'c', 'ç', 'd', 'e', 'f', 'g', 'ğ', 'h', 'ı', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'ö',
                   'p', 'r', 's', 'ş', 't', 'u', 'ü', 'v', 'y', 'z', 'q', 'w', 'x')

allUpperLetters = ('A', 'B', 'C', 'Ç', 'D', 'E', 'F', 'G', 'Ğ', 'H', 'I', 'İ', 'J', 'K', 'L', 'M', 'N', 'O', 'Ö',
                   'P', 'R', 'S', 'Ş', 'T', 'U', 'Ü', 'V', 'Y', 'Z', 'Q', 'W', 'X')

trLowerLetters = ('a', 'b', 'c', 'ç', 'd', 'e', 'f', 'g', 'ğ', 'h', 'ı', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'ö',
                  'p', 'r', 's', 'ş', 't', 'u', 'ü', 'v', 'y', 'z', 'â', 'ê', 'î', 'ô', 'û')

trUpperLetters = ('A', 'B', 'C', 'Ç', 'D', 'E', 'F', 'G', 'Ğ', 'H', 'I', 'İ', 'J', 'K', 'L', 'M', 'N', 'O', 'Ö',
                  'P', 'R', 'S', 'Ş', 'T', 'U', 'Ü', 'V', 'Y', 'Z')

allVowels = ('a', 'e', 'ı', 'i', 'o', 'ö', 'u', 'ü', 'â', 'ê', 'î', 'ô', 'û')

lowerVowels = ('a', 'e', 'ı', 'i', 'o', 'ö', 'u', 'ü')

backVowels = ('a', 'ı', 'o', 'u')

frontVowels = ('e', 'i', 'ö', 'ü')

unroundedVowels = ('a', 'e', 'ı', 'i')

roundedVowels = ('o', 'ö', 'u', 'ü')

capVowels = ('â', 'ê', 'î', 'ô', 'û')

fortis = {'f', 'h', 's', 'ç', 'ş', 'p', 't', 'k'}

prefix_lenis = {'c', 'd', 'g'}

lenis = {'b', 'c', 'd', 'g', 'ğ'}

deascii_dict = {'c': ['c', 'ç'],
                'g': ['g', 'ğ'],
                'i': ['ı', 'i'],
                'ı': ['ı', 'i'],
                'o': ['o', 'ö'],
                's': ['s', 'ş'],
                'u': ['u', 'ü']}

asciify_table = {u'ç': u'c',
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

# inc_harmony_rule sözlüğü sesli uyumunu bozan kökün son ünlüsü ile
# eklenen ekin ilk ünlüsü arasındaki ilişkiyi belirler.
incHarmonyRule = {'a': 'ei',
                  'â': 'ei',
                  'i': 'aı',
                  'o': 'eü',
                  'u': 'eü',
                  'ü': 'au',
                  'û': 'eü'}

# harmony_rule sözlüğü kökün son ünlüsü ile eklenen ekin ilk ünlüsü arasındaki ilişkiyi belirler.
harmonyRule = {'a': 'aı',
               'â': 'aı',
               'e': 'ei',
               'ı': 'aı',
               'i': 'ei',
               'î': 'ei',
               'o': 'au',
               'ö': 'eü',
               'u': 'au',
               'û': 'au',
               'ü': 'eü'}

qKeybordNear = {'q': ('w', 's', 'a'),
                'w': ('e', 'd', 's', 'a', 'q'),
                'e': ('r', 'f', 'd', 's', 'w'),
                'r': ('t', 'g', 'f', 'd', 'e'),
                't': ('y', 'h', 'g', 'f', 'r'),
                'y': ('u', 'j', 'h', 'g', 't'),
                'u': ('ı', 'k', 'j', 'h', 'y'),
                'ı': ('o', 'l', 'k', 'j', 'u'),
                'o': ('p', 'ş', 'l', 'k', 'ı'),
                'p': ('ğ', 'i', 'ş', 'l', 'o'),
                'ğ': ('ü', 'i', 'ş', 'p'),
                'ü': ('i', 'ğ'),
                'a': ('q', 'w', 's', 'x', 'z'),
                's': ('q', 'w', 'e', 'd', 'c', 'x', 'z', 'a'),
                'd': ('w', 'e', 'r', 'f', 'v', 'c', 'x', 's'),
                'f': ('e', 'r', 't', 'g', 'b', 'v', 'c', 'd'),
                'g': ('r', 't', 'y', 'h', 'n', 'b', 'v', 'f'),
                'h': ('t', 'y', 'u', 'j', 'm', 'n', 'b', 'g'),
                'j': ('y', 'u', 'ı', 'k', 'ö', 'm', 'n', 'h'),
                'k': ('u', 'ı', 'o', 'l', 'ç', 'ö', 'm', 'j'),
                'l': ('ı', 'o', 'p', 'ş', 'ç', 'ö', 'k'),
                'ş': ('o', 'p', 'ğ', 'i', 'ç', 'l'),
                'i': ('p', 'ğ', 'ü', 'ş'),
                'z': ('a', 's', 'x',),
                'x': ('z', 'a', 's', 'd', 'c'),
                'c': ('x', 's', 'd', 'f', 'v'),
                'v': ('c', 'd', 'f', 'g', 'b'),
                'b': ('v', 'f', 'g', 'h', 'n'),
                'n': ('b', 'g', 'h', 'j', 'm'),
                'm': ('n', 'h', 'j', 'k', 'ö'),
                'ö': ('m', 'j', 'k', 'l', 'ç'),
                'ç': ('ö', 'k', 'l', 'ş')}

stopwords = {'acaba', 'ama', 'ancak', 'artık', 'asla', 'aslında', 'az', 'bana', 'bazen', 'bazı', 'bazıları',
             'bazısı', 'belki', 'ben', 'beni', 'benim', 'beş', 'bile', 'bir', 'biri', 'birisi', 'birkaç', 'birkaçı',
             'birçok', 'birçokları', 'birçoğu', 'birşey', 'birşeyi', 'biz', 'bize', 'bizi', 'bizim', 'bu', 'buna',
             'bunda', 'bundan', 'bunu', 'bunun', 'burada', 'böyle', 'böylece', 'bütün', 'da', 'daha', 'de', 'demek',
             'değil', 'diye', 'diğer', 'diğeri', 'diğerleri', 'dolayı', 'elbette', 'en', 'fakat', 'falan', 'felan',
             'filan', 'gene', 'gibi', 'hangi', 'hangisi', 'hani', 'hatta', 'hem', 'henüz', 'hep', 'hepsi',
             'hepsine', 'hepsini', 'her', 'herbiri', 'herkes', 'herkese', 'herkesi', 'hiç', 'hiçbiri', 'hiçbirine',
             'hiçbirini', 'hiçkimse', 'ile', 'ise', 'için', 'içinde', 'işte', 'kadar', 'kaç', 'kendi', 'kendine',
             'kendini', 'ki', 'kim', 'kime', 'kimi', 'kimin', 'kimisi', 'madem', 'mi', 'mu', 'mü', 'mı', 'nasıl',
             'ne', 'neden', 'nedir', 'nerde', 'nerede', 'nereden', 'nereye', 'nesi', 'neyse', 'niye', 'niçin',
             'ona', 'ondan', 'onlar', 'onlara', 'onlardan', 'onların', 'onu', 'onun', 'orada', 'oysa', 'oysaki',
             'sana', 'sen', 'senden', 'seni', 'senin', 'siz', 'sizden', 'size', 'sizi', 'sizin', 'son', 'sonra',
             'tabi', 'tamam', 'tüm', 'tümü', 'var', 've', 'veya', 'veyahut', 'ya', 'yada', 'yani', 'yerine', 'yine',
             'yoksa', 'zaten', 'zira', 'çok', 'çoğu', 'çoğuna', 'çoğunu', 'çünkü', 'öbürü', 'ön', 'önce', 'ötürü',
             'öyle', 'üzere', 'şayet', 'şey', 'şimdi', 'şu', 'şuna', 'şunda', 'şundan', 'şunlar', 'şunu', 'şunun',
             'şöyle'}
