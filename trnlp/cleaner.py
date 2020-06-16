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

from re import compile

# Sessiz harfleri temizler.
CLEAN_QUITE = compile('[^aâeêıîioôöuûü]')

# Ekin eklentilerini temizler.
DSTEM_CLEANER = compile('(\\[.*?\\])|(\\(.*?\\))|({.*?})|(\\|.*?\\|)|(\\+)|(_)')


def clean_quites(word) -> str:
    """
    Ünsüz harfleri temizler ve sadece ünlü harfler kalır.
    :param word: str
    :return: str
    """
    return CLEAN_QUITE.sub('', word)


def clean_adds(word) -> str:
    """
    Bulunan eklerdeki yan açıklamaları, + ve - işaretlerini temizler.
    :param word: str
    :return: str
    """
    return DSTEM_CLEANER.sub('', word)
