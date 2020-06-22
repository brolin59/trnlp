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
from trnlp.constant import allVowels, frontVowels, backVowels, roundedVowels, unroundedVowels, harmonyRule
from trnlp.cleaner import clean_quites
import itertools
import pickle
import bz2
import re


def levenshtein_distance(fword: str, sword: str) -> int:
    """
    Levenshtein distance algoritması iki kelimenin birbirlerine olan uzaklığını verir.
    :param fword: İlk kelime
    :param sword: İkinci kelime
    :return: int olarak Levenshtein uzaklığı
    """
    lenfword = len(fword)
    lensword = len(sword)
    minlen = min(lenfword, lensword)

    if fword == "":
        return lensword
    if sword == "":
        return lenfword

    difference = abs(lensword - lenfword)
    result = 0
    reciprocal = 0

    for i in range(1, minlen + 1):
        if fword[i - 1] == sword[i - 1]:
            result = result + 0
        else:
            result = result + 1

        if fword[-i] == sword[-i]:
            reciprocal = reciprocal + 0
        else:
            reciprocal = reciprocal + 1

    result = min(result, reciprocal)
    result = result + difference
    return result


def wordtoten(word: str) -> str:
    """
    Gelen kelimeyi, sesli harfler "1", sessiz harfler "0" olmak üzere sayıya çevirir.
    :param word: Döndürülecek kelime.
    :return: 0101... şeklnde döndürür.
    """
    word = to_lower(word)
    wtt = ""
    for ch in word:
        if ch in allVowels:
            wtt += '1'
        else:
            wtt += '0'
    return wtt


def to_lower(word: str) -> str:
    """
    Gelen string(yazı) veriyi küçük harfe çevirir.
    :param word: Küçük harfe çevrilecek string değer.
    :return: Küçük harfe çevrilmiş string değer.
    """
    tolower_text = (word.replace('İ', 'i'))
    tolower_text = (tolower_text.replace('I', 'ı'))
    return tolower_text.lower()


def to_upper(word: str) -> str:
    """
    Gelen string(yazı) veriyi büyük harfe çevirir.
    :param word: Büyük harfe çevrilecek string değer.
    :return: Büçük harfe çevrilmiş string değer.
    """
    toupper_text = (word.replace('i', 'İ'))
    toupper_text = (toupper_text.replace('ı', 'I'))
    return toupper_text.upper()


def capital_tr(word: str) -> str:
    """
    Gelen string(yazı) verisinin ilk harfini büyük harfe çevirir.
    :param word: İlk harfi büyük harfe çevrilecek string değer.
    :return: İlk harfi büyük harfe çevrilmiş string değer.
    """
    return '{}{}'.format(to_upper(word[0]), word[1:])


def isCap(word: str) -> bool:
    """
    İlk harfin büyük olup olmadığını kontrol eder.
    :param word: Kontrol edilecek string(yazı) verisi
    :return: True yada False döndürür.
    """
    try:
        return word[0].isupper()
    except IndexError:
        return False


def repc(word: str) -> str:
    """
    Şapkalı harfleri normale çevirir.
    :param word: str
    :return: str
    """
    replace_letter = [('â', 'a'), ('ê', 'e'), ('î', 'i'), ('ô', 'o'), ('û', 'u')]
    for tpl in replace_letter:
        word = word.replace(tpl[0], tpl[1])
    return word


def comb(x: list, y: list) -> list:
    """
    :param x : list
    :param y : list
    :return: İki listenin kombinasyonunu liste olarak döndürür.
    """
    return list(itertools.product(x, y))


def syllabification(word: str) -> list:
    """
    Heceleme algoritması
    :param word : Hecelenecek kelime
    :return: Heceleri liste içerisinde string olarak döndürür
    """
    spell_slicer = (('001000', 5), ('000100', 5), ('01000', 4), ('00100', 4), ('00010', 4), ('1000', 3), ('0100', 3),
                    ('0011', 3), ('0010', 3), ('011', 2), ('010', 2), ('100', 2), ('10', 1), ('11', 1))

    syllable_list = []
    tenword = wordtoten(word)

    if ('111' in tenword) or (tenword.endswith('000')):
        return []

    len_spell = tenword.count('1')

    if (len_spell == 1) or (tenword == '0'):
        return [word]

    for i in range(tenword.count('1')):
        for x, y in spell_slicer:
            if tenword.startswith(x):
                syllable_list.append(word[:y])
                word = word[y:]
                tenword = tenword[y:]
                break

    if tenword == '0':
        syllable_list[-1] = syllable_list[-1] + word
    elif word:
        syllable_list.append(word)

    if len(syllable_list) != len_spell:
        return []

    return syllable_list


def vowel_harmony(f_str: str) -> bool:
    """
    Genel sesli uyumu kontrolü yapar.
    :param f_str : Sesli uyumunun kontrol edileceği kelime string şeklinde
    :return: bool
    """
    result = True

    cln_quites = clean_quites(f_str) + '.'

    if cln_quites == '.':
        return result

    for i, letter in enumerate(cln_quites):
        if cln_quites[i + 1] == '.' or letter == '.':
            break
        elif cln_quites[i + 1] in harmonyRule[letter]:
            continue
        else:
            result = False
    return result


def labial_harmony(word: str) -> bool:
    """
    Küçük sesli uyumu kontrolü yapar. True yada False döndürür.
    :param word: str
    :return: bool
    """
    cln_word = clean_quites(to_lower(repc(word)))

    if (not cln_word) or (len(cln_word) == 1):
        return True

    first_char = cln_word[0]
    for char in cln_word[1:]:
        second_char = char
        if (first_char in unroundedVowels) and (second_char in unroundedVowels):
            first_char = second_char
            continue
        elif (first_char in roundedVowels) and (second_char in 'aeuü'):
            first_char = second_char
            continue
        else:
            return False

    return True


def palatal_harmony(word: str) -> bool:
    """
    Büyük sesli uyumu kontrolü yapar. True yada False döndürür.
    :param word: str
    :return: bool
    """
    cln_word = clean_quites(to_lower(repc(word)))

    if (not cln_word) or (len(cln_word) == 1):
        return True

    first_char = cln_word[0]
    for char in cln_word[1:]:
        second_char = char
        if (first_char in frontVowels) and (second_char in frontVowels):
            first_char = second_char
            continue
        elif (first_char in backVowels) and (second_char in backVowels):
            first_char = second_char
            continue
        else:
            return False

    return True


def number_to_word(number: str) -> str:
    """
    Sayıyı yazıya dönüştürür.
    :param number: Dönüştürülece sayı string şeklinde
    :return: Yazıya döndürülmüş sayı string şeklinde
    """

    def three_digits_number(co, ii):
        trk_number_3 = {0: '',
                        1: 'bin',
                        2: 'milyon',
                        3: 'milyar',
                        4: 'trilyon',
                        5: 'katrilyon'}
        _number_list = []

        if (ii == 1) and (co == '001'):
            return 'bin'

        for i, _number in enumerate(co):
            if _number == '0':
                continue

            if i == 0:
                if _number == '1':
                    _number_list.append('yüz')
                else:
                    _number_list = _number_list + [trk_numbers_0_9[_number], 'yüz']
            elif i == 1:
                _number_list.append(trk_numbers_10_90[_number])
            elif i == 2:
                _number_list.append(trk_numbers_0_9[_number])
        return ' '.join(_number_list) + ' ' + trk_number_3[ii]

    if ',' in number:
        splt_number = number.split(',')
        fp = number_to_word(splt_number[0])
        sp = number_to_word(splt_number[1])
        return fp + 'virgül ' + sp

    trk_numbers_0_9 = {'1': 'bir',
                       '2': 'iki',
                       '3': 'üç',
                       '4': 'dört',
                       '5': 'beş',
                       '6': 'altı',
                       '7': 'yedi',
                       '8': 'sekiz',
                       '9': 'dokuz',
                       '0': ''}
    trk_numbers_10_90 = {'1': 'on',
                         '2': 'yirmi',
                         '3': 'otuz',
                         '4': 'kırk',
                         '5': 'elli',
                         '6': 'altmış',
                         '7': 'yetmiş',
                         '8': 'seksen',
                         '9': 'doksan',
                         '0': ''}

    number = number.replace('.', '')
    len_number = len(number)
    if len_number % 3 == 0:
        add_zero = 0
    else:
        add_zero = 3 - (len_number % 3)

    number = ('0' * add_zero) + number
    number_list = [number[i:i + 3] for i in range(0, len(number), 3)]
    number_list.reverse()

    ntow = ''
    for s, part in enumerate(number_list):
        if part == '000':
            continue
        ntow = three_digits_number(part, s) + ' ' + ntow

    if not ntow:
        return 'sıfır'
    else:
        return ntow


def word_to_number(number_string: str) -> str:
    """
    Yazıyla yazılmış olan sayıyı sayıya dönüştürür.
    :param number_string: Dönüştürülece yazı string şeklinde
    :return: Sayıya döndürülmüş yazı string şeklinde
    """

    def three_digits_number(co):
        yuzluk = '000'
        reco = [i for i in re.split(regexi, co) if i]
        if reco:
            reco.reverse()
            reco = reco + ['']
            for i, it in enumerate(reco):
                if it == 'yüz':
                    if reco[i + 1] in trk_numbers_0_9:
                        yuzluk = trk_numbers_0_9[reco[i + 1]] + yuzluk[1:]
                    else:
                        yuzluk = '1' + yuzluk[1:]
                    break
                elif it in trk_numbers_10_90:
                    yuzluk = yuzluk[0] + trk_numbers_10_90[it] + yuzluk[2]
                elif it in trk_numbers_0_9:
                    yuzluk = yuzluk[:2] + trk_numbers_0_9[it]
        return yuzluk

    if number_string.strip() == 'sıfır':
        return '0'

    if 'virgül' in number_string:
        splt_word = number_string.split('virgül')
        fp = word_to_number(splt_word[0])
        sp = word_to_number(splt_word[1])
        return fp + ',' + sp

    trk_numbers_0_9 = {'bir'  : '1',
                       'iki'  : '2',
                       'üç'   : '3',
                       'dört' : '4',
                       'beş'  : '5',
                       'altı' : '6',
                       'yedi' : '7',
                       'sekiz': '8',
                       'dokuz': '9'}

    trk_numbers_10_90 = {'on'    : '1',
                         'yirmi' : '2',
                         'otuz'  : '3',
                         'kırk'  : '4',
                         'elli'  : '5',
                         'altmış': '6',
                         'yetmiş': '7',
                         'seksen': '8',
                         'doksan': '9'}

    cd = {'katrilyon': 18, 'trilyon': 15, 'milyar': 12, 'milyon': 9, 'bin': 6, 'yüz': 3}
    number_digit = ['katrilyon', 'trilyon', 'milyar', 'milyon', 'bin']
    regexi = '(yüz|doksan|seksen|yetmiş|altmış|elli|kırk|otuz|yirmi|on|dokuz|sekiz|yedi|altı|beş|dört|üç|iki|bir)'

    _word = number_string.replace(' ', '')
    liste = []
    uzunluk = 0
    for part in number_digit:
        repart = re.search(part, _word)
        if repart:
            x, y = repart.span()
            _uzunluk = cd[_word[x:y]]
            if _uzunluk > uzunluk:
                uzunluk = _uzunluk
            liste.append((_word[:x], _word[x:y]))
            _word = _word[y:]

    if _word:
        liste.append(_word)

    sayi = '0' * uzunluk

    for part in liste:
        if type(part) is tuple:
            if part == ('', 'bin'):
                sayi = sayi[:-cd[part[1]]] + '001' + sayi[3 - cd[part[1]]:]
                continue
            sayi = sayi[:-cd[part[1]]] + three_digits_number(part[0]) + sayi[3 - cd[part[1]]:]
        elif type(part) is str:
            sayi = sayi[:-3] + three_digits_number(part)
    sayi = sayi.lstrip('0')

    return sayi


def nth_replace(string, old, new, n=1) -> str:
    """
    Eşleşen n'inci karakteri yenisi ile değiştirir.
    :param string: string
    :param old: Değiştirilecek karakter
    :param new: Yerine yazılacak karakter
    :param n: Eşleşen kaçıncı karakterin değiştirileceği
    :return: string
    """
    left_join = old
    right_join = old
    groups = string.split(old)
    nth_split = [left_join.join(groups[:n]), right_join.join(groups[n:])]
    return new.join(nth_split)


def package_path():
    return __file__[:-9].replace('\\', '/')


def tr_sort(liste: list):
    """
    Liste içerisindeki string değişkenleri Türk alfabesine göre sıralar.
    :param liste: Liste içinde string değişkenler
    :return: Sıralanmış liste
    """
    tr_letters = "abcçdefgğhıijklmnoöprsştuüvyz"
    trans = {i: tr_letters.index(i) for i in tr_letters}
    return sorted(liste, key=lambda x: trans.get(x[0]))


def change_punch(satir):
    rep_text = satir
    char_rep_dict = {'”'   : '"',
                     '“'   : '"',
                     '’'   : "'",
                     '‘'   : "'",
                     "`"   : "'",
                     '…'   : '...',
                     'ș'   : 'ş',
                     '""'  : '"',
                     '\'\'': '"'}

    for old, new in char_rep_dict.items():
        rep_text = rep_text.replace(old, new)
    return rep_text


def repa(word):
    apostrophes = "ʿ’'`.-"
    for apos in apostrophes:
        word = word.replace(apos, '')
    return word


def n_gram(n_iter, n=2) -> list:
    ngram_list = []

    if len(n_iter) == n:
        ngram_list.append(n_iter)
    elif len(n_iter) < n:
        return []
    else:
        for i, char in enumerate(n_iter):
            if i < len(n_iter) - (n - 1):
                ngram_list.append(n_iter[i:i + n])

    return ngram_list


def debug(func):
    import functools

    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Çağırdı {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} döndürdü {value!r}")
        return value

    return wrapper_debug


def unrepeated_list(l: list) -> list:
    temp = []
    for x in l:
        if x not in temp:
            temp.append(x)
    return temp


def compressed_pickle(title, data):
    with bz2.BZ2File(title + ".pbz2", "w") as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)


def decompress_pickle(file):
    data = bz2.BZ2File(file, "rb")
    data = pickle.load(data)
    return data


if __name__ == '__main__':
    with open(package_path() + 'data/freq_dict.pickle', 'rb') as handle:
        lexicon = pickle.load(handle)

    compressed_pickle("freq_dict", lexicon)
