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

from trnlp.morphology import TrnlpWord
from itertools import product, groupby
from trnlp.constant import *
from trnlp.helper import *
from trnlp.tokenization import word_token

__all__ = ['SpellingCorrector']


class SpellingCorrector:
    __freq_dict = {}
    _obj_ = TrnlpWord()

    def __init__(self):
        self.__user_freq_dict = {}
        self.__org_word = ""
        self.__word_list = ""
        self.__load_inf_dict()
        self.__iteration = False

    def settext(self, word: str) -> None:
        self.__word_list = word_token(to_lower(word))

    @classmethod
    def __load_inf_dict(cls) -> None:
        cls.__freq_dict = decompress_pickle(package_path() + 'data/freq_dict.pbz2')

    def __split(self, word: str) -> list:
        return [(word[:i], word[i:]) for i in range(len(word) + 1)]

    def __word_calculator(self, word: str) -> bool:
        counter = 0
        for letter in to_lower(word):
            if letter in allLowerLetters:
                counter += 1
        if (counter / len(word)) > 0.65:
            return True

    def vowelizero(self, word: str) -> list:
        if not self.__word_calculator(word):
            return []

        a1 = ['', 'a', 'e', 'ı', 'i', 'o', 'ö', 'u', 'ü']

        if word[0] in allVowels:
            result = [word[0]]
        else:
            result = [a1, word[0]]

        for i in range(1, len(word)):
            fl = word[i - 1]
            fs = word[i]

            if (fl not in allVowels) and (fs not in allVowels):
                result.append(a1)
                result.append(fs)
            else:
                result.append(fs)

        if word[-1] not in allVowels:
            result.append(a1)

        return [''.join(x) for x in product(*result)]

    def deasciifier(self, word: str) -> list:
        ascii_list = []
        for char in word:
            if char in deascii_dict:
                ascii_list.append(deascii_dict[char])
            else:
                ascii_list.append([char])

        result = ['']
        for may in ascii_list:
            result = [''.join(s) for s in product(result, may)]
        return result

    def unrepeater(self, word: str) -> list:
        result = []
        i1 = [c for c, _ in groupby(word)]
        i2 = [''.join(c)[:2] for _, c in groupby(word)]
        zip_i = [set(i) for i in list(zip(i1, i2))]

        a = zip_i[0]

        for i in zip_i[1:]:
            result = [''.join(s) for s in product(a, i)]
            a = result
        return result

    def transposes(self, word: str) -> list:
        split_word = self.__split(word)
        return [L + R[1] + R[0] + R[2:] for L, R in split_word if len(R) > 1]

    def inserts(self, word: str, char_set=trLowerLetters) -> list:
        split_word = self.__split(word)
        return [L + c + R for L, R in split_word for c in char_set]

    def replaces(self, word: str, char_set=trLowerLetters) -> list:
        split_word = self.__split(word)
        return [L + c + R[1:] for L, R in split_word if R for c in char_set]

    def deletes(self, word: str) -> list:
        split_word = self.__split(word)
        return [L + R[1:] for L, R in split_word if R]

    def __known(self, words: list) -> list:
        known_list = []
        for w in words:
            if w in self.__user_freq_dict:
                known_list.append(w)
        return known_list

    def __freq(self, x1):
        f1 = self.__user_freq_dict[x1[0]]
        if x1[1] <= 0:
            return f1 * 2
        else:
            return f1 / x1[1]

    def __manipulate(self, word, **kwargs):
        result = set()

        for key, value in kwargs.items():
            if (key == "deasciifier") and (value is True):
                [result.add((x, 0.1))
                 for x in self.__known(self.deasciifier(word))]
            elif (key == "unrepeater") and (value is True):
                [result.add((x, (len(self.__org_word) - len(x))))
                 for x in self.__known(self.unrepeater(word))]
            elif (key == "transposes") and (value is True):
                [result.add((x, 2))
                 for x in self.__known(self.transposes(word))]
            elif (key == "inserts") and (value is True):
                [result.add((x, 0.5))
                 for x in self.__known(self.inserts(word))]
            elif (key == "replaces") and (value is True):
                [result.add((x, 2))
                 for x in self.__known(self.replaces(word))]
            elif (key == "deletes") and (value is True):
                [result.add((x, 1))
                 for x in self.__known(self.deletes(word))]
            elif (key == "vowelizero") and (value is True) and (self.__iteration is False):
                [result.add((x, (len(x) - len(self.__org_word))))
                 for x in self.__known(self.vowelizero(word))]

        return list(result)

    def correction(self, **kwargs):
        result = []

        if not self.__word_list:
            return [[self.__org_word]]

        if "freq" not in kwargs:
            self.__user_freq_dict = self.__freq_dict
        else:
            self.__user_freq_dict = kwargs["freq"]

        if "all" not in kwargs:
            kwargs["all"] = False

        if "word_list" in kwargs:
            _wordlist = kwargs["word_list"]
        else:
            _wordlist = self.__word_list

        if kwargs["all"] is True:
            kwargs["deasciifier"] = True
            kwargs["unrepeater"] = True
            kwargs["transposes"] = True
            kwargs["inserts"] = True
            kwargs["replaces"] = True
            kwargs["deletes"] = True
            kwargs["vowelizero"] = True

        for word in _wordlist:
            self.__org_word = word
            temp = self.__manipulate(word, **kwargs)

            if temp:
                temp.sort(key=lambda x: self.__freq(x))
                temp.reverse()

            self._obj_.setword(word)
            inf_temp = []
            if self._obj_.get_inf:
                for may in self._obj_.get_inf:
                    inf_temp.append((self._obj_.correct_form(may),))

            try:
                temp = inf_temp[:1] + temp + inf_temp[1:]
            except IndexError:
                temp = inf_temp + temp

            if not temp:
                result.append([word])
            else:
                temp = unrepeated_list([x[0] for x in temp])
                result.append(temp)

        return result


if __name__ == '__main__':
    pass
