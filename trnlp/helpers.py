# -*- coding: utf-8 -*-
""" /*Copyright 2018 Esat Mahmut Bayol

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; either version 2 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA

*/"""
import sqlite3
import os
import re

current_file = (os.path.abspath(os.path.dirname(__file__))).replace('\\', '/')


def replace_cap_letter(word):
    # degistir listesindeki ilk öğeyi ikincisi ile değiştiriyoruz. Yani şapkalı harfleri normale çeviriyoruz.
    replace_letter = [('â', 'a'), ('ê', 'e'), ('î', 'i'), ('ô', 'o'), ('û', 'u')]
    for tpl in replace_letter:
        word = word.replace(tpl[0], tpl[1])
    return word


def son_sesli_bul(kelimecik):
    # Fonksiyona gelen yazının son sesli harfini bulur.
    son_sesli = ''
    for harf in kelimecik:
        if harf in 'aâeêıîioôöuûü':
            son_sesli = harf
    return son_sesli


# Fonksiyonların süresini ölçmek için kullanıyorum
# Süresi ölçülecek fonksiyonun bir satır üzerine '@timing' yazmanız yeterli
##########################################################################################
def timing(fnk):
    """
    Fonksiyonların işlem süresini ölçer.
    :param fnk: Fonksiyonun adı
    :return: str
    """
    import time

    def wrap(*args):
        time1 = time.time()
        ret = fnk(*args)
        time2 = time.time()
        print('%s function took %0.3f ms' % (fnk.__name__, (time2 - time1) * 100.0))
        return ret

    return wrap


def unrepeated_list(lst):
    """
    Listeyi tekrarsız yapar.
    :param lst: list
    :return: list
    """
    return list(set(lst))


# replace komutu tüm eşleşmeleri değiştirir. nyh_replace sadece n ile belirtilen konumdaki karakteri yenisi
# ile değiştirir.
# Örneğin :
# >> yazi = 'deneme',
# >> nth_replace(yazi, 'e', 'a', 2)
# >> dename
####################################################################
def nth_replace(string, old, new, n=1):
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


# listedeki her bir elemanı ayrı satıra yazdırır
def print_list_item(_list: list):
    for item in _list:
        print(item)


# Sozluğu yükler
def tr_sozluk_yukle():
    with sqlite3.connect(current_file + '/Data/tr_NLP.sqlite') as vt:
        im = vt.cursor()
        im.execute("SELECT * FROM tr_sozluk")
        tr_sozluk = im.fetchall()
    return tr_sozluk


# Kısaltmaların listesi (kısaltma,açılımı) şeklinde
def load_shortlist():
    with sqlite3.connect(current_file + '/Data/tr_NLP.sqlite') as vt:
        im = vt.cursor()
        im.execute("SELECT * FROM tr_kisaltmalar")
        kisaltmalar = im.fetchall()
        kisaltmalar = [i[0] for i in kisaltmalar]
    return kisaltmalar


# Levenshtein Distance hesaplamasını yapar. İki kelimenin birbirine olan yakınlığını bulmak için hızlı bir algoritma.
def lddistance(fword, sword):
    lenfword = len(fword)
    lensword = len(sword)
    minlen = min(lenfword, lensword)

    if fword == "":
        return lensword
    if sword == "":
        return lenfword

    fark = abs(lensword - lenfword)
    sonuc = 0
    sonucters = 0

    for i in range(1, minlen + 1):
        if fword[i - 1] == sword[i - 1]:
            sonuc = sonuc + 0
        else:
            sonuc = sonuc + 1

        if fword[-i] == sword[-i]:
            sonucters = sonucters + 0
        else:
            sonucters = sonucters + 1

    sonuc = min(sonuc, sonucters)
    sonuc = sonuc + fark
    return sonuc


def noktalama_degistir(satir):
    rep_text = satir
    char_rep_dict = {'”': '"',
                     '“': '"',
                     '’': "'",
                     '‘': "'",
                     "`": "'",
                     '…': '...',
                     'ș': 'ş',
                     '""': '"',
                     '\'\'': '"'}

    for old, new in char_rep_dict.items():
        rep_text = rep_text.replace(old, new)
    return rep_text


# Kelimenin harflerinin n'li durumunu çıkarır.
# Örneğin; char_gram('deneme', 2) ==> ['de', 'en', 'ne', 'em', 'me']
def char_gram(word, n=2):
    len_word = len(word)
    ngram_list = []

    if len_word == n:
        ngram_list.append(word)
    elif len_word < n:
        return []
    else:
        for i, char in enumerate(word):
            if i < len_word - (n - 1):
                ngram_list.append(word[i:i + n])

    return ngram_list


# Kelimelerin n'li durumunu çıkarır.
# Kelimeler liste olarak verilmelidir. Bir yazı içerisindeki kelimelerin listesini elde etme için TextStatistic'teki
# wordlist komutu kullanılabilir.
def word_gram(word_list: list, n=2):
    len_word = len(word_list)
    ngram_list = []

    if len_word == n:
        ngram_list.append(word_list)
    elif len_word < n:
        return []
    else:
        for i, char in enumerate(word_list):
            if i < len_word - (n - 1):
                ngram_list.append(word_list[i:i + n])

    return ngram_list


def number_to_word(number):
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
        return ''.join(_number_list) + trk_number_3[ii]

    trk_numbers_0_9 = {'1': 'bir', '2': 'iki', '3': 'üç', '4': 'dört', '5': 'beş',
                       '6': 'altı', '7': 'yedi', '8': 'sekiz', '9': 'dokuz', '0': ''}
    trk_numbers_10_90 = {'1': 'on', '2': 'yirmi', '3': 'otuz', '4': 'kırk', '5': 'elli',
                         '6': 'altmış', '7': 'yetmiş', '8': 'seksen', '9': 'doksan', '0': ''}

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


def word_to_number(word):
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

    if word.strip() == 'sıfır':
        return '0'

    trk_numbers_0_9 = {'bir': '1', 'iki': '2', 'üç': '3', 'dört': '4', 'beş': '5',
                       'altı': '6', 'yedi': '7', 'sekiz': '8', 'dokuz': '9'}
    trk_numbers_10_90 = {'on': '1', 'yirmi': '2', 'otuz': '3', 'kırk': '4', 'elli': '5',
                         'altmış': '6', 'yetmiş': '7', 'seksen': '8', 'doksan': '9'}
    cd = {'katrilyon': 18, 'trilyon': 15, 'milyar': 12, 'milyon': 9, 'bin': 6, 'yüz': 3}
    number_digit = ['katrilyon', 'trilyon', 'milyar', 'milyon', 'bin']

    regexi = '(yüz|doksan|seksen|yetmiş|altmış|elli|kırk|otuz|yirmi|on|dokuz|sekiz|yedi|altı|beş|dört|üç|iki|bir)'

    _word = word.replace(' ', '')
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


def sirala(liste: list):
    harfler = "abcçdefgğhıijklmnoöprsştuüvyz"
    cevrim = {i: harfler.index(i) for i in harfler}
    return sorted(liste, key=lambda x: cevrim.get(x[0]))
