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

from trnlp.helper import package_path, to_lower, isCap
from trnlp.constant import stopwords
from trnlp.token_data.data import *
from pickle import load
import collections
import re

__all__ = ['TrnlpToken',
           'unitoascii',
           'simple_token',
           'whitespace_token',
           'word_token']


def _decode(string: str) -> str:
    """
    Bu fonksiyon unidecode kütüphanesinden alınmış ve türkçe için özelleştirilmiştir.
    Türkçe için genişletilmiş Ascii çevirici.
    :param string: unicode string
    :return: Tr Ascii string
    """
    cache = {}
    decval = []

    for char in string:
        codepoint = ord(char)

        if codepoint in {199, 214, 220, 231, 246, 252, 286, 287, 304, 305, 350, 351, 8364, 8378, 8240}:
            decval.append(str(char))
            continue

        if codepoint < 0x80:
            decval.append(str(char))
            continue

        if codepoint > 0xeffff:
            continue

        section = codepoint >> 8
        position = codepoint % 256

        if section in cache:
            table = cache[section]
        else:
            try:
                mod = __import__('unidecoder.x%03x' % section, fromlist=['data'])
            except ImportError:
                cache[section] = None
                continue
            cache[section] = table = mod.data

        if table and len(table) > position:
            decval.append(table[position])

    return ''.join(decval)


def unitoascii(string: str) -> str:
    """
    Türkçe için genişletilmiş Ascii çevirici.
    :param string: unicode string
    :return: Tr Ascii string
    """
    try:
        string.encode('ASCII')
    except UnicodeEncodeError:
        return _decode(string)

    return string


def simple_token(utext: str, sw=None) -> list:
    """
    Yazı içerisindeki her karakteri parçalar
    :param utext: Parçalanacak yazı
    :param sw:
    :return: liste şeklinde parçalanmış yazı ve karakterler
    """
    if sw is None:
        sw = ()
    result = list(filter(None, [i.strip() for i in re.split(r"(\W+?\s?)", utext)]))
    return [x for x in result if to_lower(x) not in sw]


def whitespace_token(utext: str, sw=None) -> list:
    """
    Yazıyı boşluklara göre parçalar
    :param utext: Parçalanacak yazı
    :param sw:
    :return: liste şeklinde parçalanmış yazı
    """
    if sw is None:
        sw = ()
    result = [x for x in utext.split(' ') if x]
    return [x for x in result if to_lower(x) not in sw]


def word_token(utext: str, numbers=True, sw=None) -> list:
    """
    Yazı içerisindeki kelimeleri döndürür. Sayılar yada sayı içeren bölümler bulunmaz.
    :param utext: Parçalanacak yazı
    :param numbers:
    :param sw:
    :return: liste şeklinde kelimeler
    """
    if sw is None:
        sw = ()
    try:
        # Gerekli karakter dönüşümleri
        utext = unitoascii(utext).replace("''", '"')

        # Boş satırları temizle
        utext = '\n'.join([line for line in utext.split('\n') if line.strip()])

        # Birden fazla olan boşlukları teke düşür.
        utext = re.sub(r" +", " ", utext)

        a1 = []
        a2 = ""
        for line in utext.split('\n'):
            line = line.strip()
            if line.endswith('-'):
                a2 = a2 + line[:-1]
                continue
            else:
                if a2:
                    splt_line = line.split(' ')
                    a2 = a2 + splt_line[0]
                    a1.append(a2)
                    a1.append(' '.join(splt_line[1:]))
                    a2 = ""
                else:
                    a1.append(line)
        if a2:
            a1.append(a2)

        utext = '\n'.join(a1)

        if numbers:
            regexi = r"([a-z0-9À-ž]+([’\'][a-z]+)?)"
        else:
            regexi = r"([a-zÀ-ž]+([’\'][a-z]+)?)"

        result = [x[0] for x in re.findall(regexi, utext, flags=re.IGNORECASE)]
        return [x for x in result if to_lower(x) not in sw]
    except IndexError:
        return []


class TrnlpToken:
    def __init__(self):
        self.__text = ""
        self.__spans = []
        self.__types = []
        self.__tokens = []
        self.__shortList = {}
        self.__load_dict()

    @property
    def spans(self) -> list:
        return self.__spans

    @property
    def types(self) -> list:
        return self.__types

    @property
    def tokens(self) -> list:
        return self.__tokens

    @property
    def wordtoken(self) -> list:
        return self.__word_token()

    @property
    def phrasetoken(self) -> list:
        return self.__phrase_token()

    @property
    def wordcounter(self):
        return self.__word_counter()

    @property
    def ziptoken(self) -> list:
        return self.__zip_token()

    def settext(self, text) -> None:
        self.__spans = []
        self.__types = []
        self.__tokens = []
        self.__text = text
        self.__arr_text()
        self.__span_token()

    def __load_dict(self) -> None:
        with open(package_path() + 'data/shortlist.pickle', 'rb') as handle:
            self.__shortList = load(handle)

    def __arr_text(self) -> None:
        # Gerekli karakter dönüşümleri
        self.text = unitoascii(self.__text).replace("''", '"')

        # Boş satırları temizle
        self.__text = '\n'.join([line for line in self.__text.split('\n') if line.strip()])

        # Birden fazla olan boşlukları teke düşür.
        self.__text = re.sub(r" +", " ", self.__text)

        a1 = []
        a2 = ""
        for line in self.__text.split('\n'):
            line = line.strip()
            if line.endswith('-'):
                a2 = a2 + line[:-1]
                continue
            else:
                if a2:
                    splt_line = line.split(' ')
                    a2 = a2 + splt_line[0]
                    a1.append(a2)
                    a1.append(' '.join(splt_line[1:]))
                    a2 = ""
                else:
                    a1.append(line)
        if a2:
            a1.append(a2)
        self.__text = '\n'.join(a1)

    def __span_token(self) -> None:
        self.__abbr_decoder()

    def __regex_finder(self, regex_list: list):
        for regex in regex_list:
            for matches in re.finditer(regex, self.__text, flags=re.IGNORECASE | re.DOTALL):
                yield matches

    def __abbr_decoder(self) -> None:
        for matches in self.__regex_finder(abbr):
            for grp_num in range(0, len(matches.groups())):
                grp_num = grp_num + 1
                match = to_lower(matches.group(grp_num))
                if match in self.__shortList:
                    self.__spans.append(matches.span(grp_num))
                    self.__types.append('abbr')
        self.__regex_decoder()

    def __regex_decoder(self) -> None:
        non_eol = set()
        for matches in self.__regex_finder([r"([\[\(\"].*?[\"\)\]])"]):
            x, y = matches.span()
            [non_eol.add(x) for x in range(x, y)]

        for regex_list, r_types in all_regex:
            for matches in self.__regex_finder(regex_list):
                x, y = matches.span()
                if r_types == 'word':
                    mword = to_lower(self.__text[x:y])
                    if mword in self.__shortList:
                        self.__spans.append(matches.span())
                        self.__types.append('abbr')
                        continue
                elif r_types == 'eos':
                    if x in non_eol:
                        self.__spans.append(matches.span())
                        self.__types.append('punch')
                        continue
                self.__spans.append(matches.span())
                self.__types.append(r_types)
        self.__span_solver()

    def __span_solver(self) -> None:
        span_set = set()
        spans = []
        types = []
        for s in range(len(self.__spans)):
            span_type = self.__types[s]
            x, y = self.__spans[s]
            if x == y:
                continue
            elif (y - x == 1) and (x not in span_set):
                spans.append((x, y))
                types.append(span_type)
                span_set.add(x)
                continue
            else:
                in_span_set = [i for i in range(x, y) if i in span_set]
                if not in_span_set:
                    spans.append((x, y))
                    types.append(span_type)
                    [span_set.add(x) for x in range(x, y)]

        spans_type = list(zip(spans, types))
        spans_type.sort(key=lambda l: l[0][0])
        self.__spans = [x for x, y in spans_type]
        self.__types = [y for x, y in spans_type]
        self.__set_tokens()

    def __set_tokens(self) -> None:
        self.__tokens = [self.__text[self.__spans[i][0]:self.__spans[i][1]] for i in range(len(self.__spans))]

    @staticmethod
    def is_header(txt: str) -> bool:
        txt = txt.split(' ')
        txt_list = [True for wrd in txt if isCap(wrd)]
        return True if (len(txt_list) / len(txt)) > 0.65 else False

    def __word_token(self) -> list:
        return [self.__tokens[i] for i in range(len(self.__tokens))
                if (self.__types[i] == 'word') or (self.__types[i] == 'suffix')]

    def __zip_token(self) -> list:
        return list(zip(self.__tokens, self.__types, self.__spans))

    def __phrase_token(self) -> list:
        phrase_list = []
        phrase = ""
        for tkn, tkn_type in zip(self.__tokens, self.__types):
            if tkn_type == 'eos':
                phrase = "{}{}".format(phrase, tkn)
                phrase_list.append(phrase.strip())
                phrase = ""
            elif tkn_type == 'enter':
                phrase = "{}{}".format(phrase, ' ')
            else:
                phrase = "{}{}".format(phrase, tkn)
        if phrase:
            phrase_list.append(phrase.strip())
        return phrase_list

    def __word_counter(self):
        return collections.Counter(self.__word_token())

    def clean_punch(self, zip_list=None) -> list:
        punchs = {'eos', 'enter', 'space', 'punch'}
        if zip_list is None:
            zip_list = self.__zip_token()
        result = []
        for part, wtype, span in zip_list:
            if wtype in punchs:
                continue
            else:
                result.append((part, wtype, span))
        return result

    def clean_stopwords(self, zip_list=None) -> list:
        if zip_list is None:
            zip_list = self.__zip_token()
        result = []
        for part, wtype, span in zip_list:
            if to_lower(part) in stopwords:
                continue
            else:
                result.append((part, wtype, span))
        return result


if __name__ == '__main__':
    pass
