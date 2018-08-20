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
