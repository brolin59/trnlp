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

The full license is in the file LICENSE.txt, distributed with this software
"""

from re import findall
from trnlp.constant import allVowels


def rfind_parenthesize(x: str):
    """
    Harf dizisinin en sonunda bulunan '{}' süslü parantez içerisindeki ifadeyi döndürür.
    :param x : str
    :return: str
    """
    return x[x.rfind('(') + 1:x.rfind(')')]


def rfind_curly_braces(x: str) -> str:
    """
    Harf dizisinin en sonunda bulunan '{}' süslü parantez içerisindeki ifadeyi döndürür.
    :param x : str
    :return: str
    """
    return x[x.rfind('{') + 1:x.rfind('}')]


def rfind_square_bracket(x: str) -> str:
    """
    Harf dizisinin en sonunda bulunan '[]' köşeli parantez içerisindeki ifadeyi döndürür.
    :param x : str
    :return: str
    """
    return x[x.rfind('[') + 1:x.rfind(']')]


def find_table_number(adding: str) -> int:
    """
    Ekin tablo numarasını döndürür.
    :param adding : str
    :return: int
    """
    numbers = rfind_square_bracket(adding)
    list_no = numbers[:numbers.find('_')]
    return int(list_no)


def find_row_number(adding: str) -> int:
    """
    Ekin tablo içerisindeki satır numarasını döndürür.
    :param adding : str
    :return: int
    """
    numbers = rfind_square_bracket(adding)
    row_no = numbers[numbers.find('_') + 1:]
    return int(row_no)


def find_numbers(inf: str):
    items_no = findall(r'\[(.*?)\]', inf)
    return [(int(x.split('_')[0]), int(x.split('_')[1])) for x in items_no if x]


def base_finder(string):
    return string[:string.find('(')]


def last_vowel(word: str) -> str:
    """
    Kelimenin son sesli harfini bulur.
    :param word: str
    :return: char
    """
    vowel = ''
    i = 1
    while i <= len(word):
        if word[-i] in allVowels:
            vowel = word[-i]
            break
        i += 1
    return vowel


def first_vowel(word: str) -> str:
    """
    Kelimenin ilk sesli harfini bulur.
    :param word: str
    :return: char
    """
    vowel = ''
    i = 0
    while i < len(word):
        if word[i] in allVowels:
            vowel = word[i]
            break
        i += 1
    return vowel
