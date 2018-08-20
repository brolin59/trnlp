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
import re
from collections import Counter
from operator import itemgetter

All_lower_char = 'aâeêıîioôöuûübcçdfgğhjklmnprsştvyzqwx'
All_upper_char = 'AÂEÊIÎİOÔÖUÛÜBCÇDFGĞHJKLMNPRSŞTVYZQWX'


class Statistic:
    def __init__(self, text):
        self.text = text

    # Yazı içerisindeki kelimelerin listesini verir. Liste olarak geri döndürür.
    def wordlist(self):
        return list(filter(None, re.split('[^A-Za-zçÇğĞıİöÖşŞüÜâÂêÊîÎôÔûÛ]', self.text)))

    # Yazı içerisindeki satırları sayar.
    def count_lines(self):
        return self.text.count('\n') + 1

    # Yazı içerisindeki boş satırları sayar.
    def count_blank_lines(self):
        return len([i for i in self.text.split('\n') if i.strip() == ''])

    # Yazı içerisindeki boşluk karakterini sayar.
    def count_space(self):
        return self.text.count(' ')

    # Yazı içerisindeki noktaları sayar.
    def count_points(self):
        return len(re.findall(r'[.]', self.text))

    # Yazı içerisindeki kelimeleri sayar.
    def find_words(self):
        words = list(filter(None, re.split('[^0-9A-Za-zçÇğĞıİöÖşŞüÜâÂêÊîÎôÔûÛ]', self.text)))
        freq_words = sorted(dict(Counter(words)).items(), key=itemgetter(1), reverse=True)
        return words, len(words), freq_words

    # Yazı içerisindeki harfleri sayar.
    def find_letters(self):
        char_list = All_lower_char + All_upper_char
        chars = [i for i in self.text if i in char_list]
        freq_chars = sorted(dict(Counter(chars)).items(), key=itemgetter(1), reverse=True)
        return chars, len(chars), freq_chars

    # Yazı içerisindeki sayıları sayar.
    def find_numbers(self):
        numbers = re.findall(r'[0-9]', self.text)
        freq_numbers = sorted(dict(Counter(numbers)).items(), key=itemgetter(1), reverse=True)
        return numbers, len(numbers), freq_numbers

    # Yazı içerisindeki sesli harfleri sayar.
    def find_vowels(self):
        vowels = re.findall(r'[aâeêıîioôöuûüAÂEÊIÎİOÔÖUÛÜ]', self.text)
        freq_vowels = sorted(dict(Counter(vowels)).items(), key=itemgetter(1), reverse=True)
        return vowels, len(vowels), freq_vowels

    # Yazı içerisindeki sessiz harfleri sayar.
    def find_quiets(self):
        quiets = re.findall(r'[bcçdfgğhjklmnprsştvyzqwxBCÇDFGĞHJKLMNPRSŞTVYZQWX]', self.text)
        freq_quiets = sorted(dict(Counter(quiets)).items(), key=itemgetter(1), reverse=True)
        return quiets, len(quiets), freq_quiets

    # Yazı içerisindeki büyük harfleri sayar.
    def find_upper_letters(self):
        uppers = re.findall(r'[AÂEÊIÎİOÔÖUÛÜBCÇDFGĞHJKLMNPRSŞTVYZXQW]', self.text)
        freq_uppers = sorted(dict(Counter(uppers)).items(), key=itemgetter(1), reverse=True)
        return uppers, len(uppers), freq_uppers

    # Yazı içerisindeki küçük harfleri sayar.
    def find_lower_letters(self):
        lowers = re.findall(r'[aâeêıîioôöuûübcçdfgğhjklmnprsştvyzqwx]', self.text)
        freq_lowers = sorted(dict(Counter(lowers)).items(), key=itemgetter(1), reverse=True)
        return lowers, len(lowers), freq_lowers

    # Yazı içerisindeki büyük harf ile başlayan kelimeleri sayar.
    def find_startswith_upper(self):
        words = self.find_words()[0]
        s_upper = [i for i in words if i.istitle()]
        freq_upper = sorted(dict(Counter(s_upper)).items(), key=itemgetter(1), reverse=True)
        return s_upper, len(s_upper), freq_upper

    # Yazı içerisindeki sayı ve harf haricindeki tüm karakterleri sayar.
    def find_undef_chars(self):
        undef_chars = [i.strip() for i in re.findall('\W\s', self.text)]
        freq_undef_chars = sorted(dict(Counter(undef_chars)).items(), key=itemgetter(1), reverse=True)
        return undef_chars, len(undef_chars), freq_undef_chars

    # Verilerin frekansını hesaplar.
    @staticmethod
    def calculate_frequency(find_freq_list, *args):
        if args:
            pass
        else:
            args = tuple(sum(x[1] for x in find_freq_list), )
        fin_list = []
        for i, items in enumerate(find_freq_list):
            freq = (items[1] * 100) / args[0]
            fin_list.append((items[0], items[1], freq))
        return fin_list

    # Yukarıdaki tüm verilerin sonucunu ekrana yazdırır.
    def text_statistic(self):
        toplam_satir_sayisi = self.count_lines()
        toplam_bos_satir_sayisi = self.count_blank_lines()
        bos_satir_frekansi = (toplam_bos_satir_sayisi * 100) / toplam_satir_sayisi
        toplam_yazili_satir_sayisi = toplam_satir_sayisi - toplam_bos_satir_sayisi
        yazili_satir_frekansi = (toplam_yazili_satir_sayisi * 100) / toplam_satir_sayisi

        kelimeler = self.find_words()
        toplam_kelime_sayisi = kelimeler[1]
        tekrarsiz_kelime_sayisi = len(set(kelimeler[0]))
        tekrarlanan = kelimeler[2][:5]
        tekrarlanan_kelime = self.calculate_frequency(tekrarlanan, toplam_kelime_sayisi)

        yazidaki_karakter_sayisi = len(self.text)
        yazidaki_bosluk_sayisi = self.count_space()
        boslu_frekansi = (yazidaki_bosluk_sayisi * 100) / yazidaki_karakter_sayisi

        sayilar = self.find_numbers()
        toplam_rakam_sayisi = sayilar[1]
        rakamlarin_listesi = self.calculate_frequency(sayilar[2], yazidaki_karakter_sayisi)
        rakam_frekansi = (toplam_rakam_sayisi * 100) / yazidaki_karakter_sayisi

        ozel_karakterler = self.find_undef_chars()
        ozel_karakterlerin_sayisi = ozel_karakterler[1]
        ozel_karakter_frekans = (ozel_karakterlerin_sayisi * 100) / yazidaki_karakter_sayisi
        ozel_karakterlerin_liste = self.calculate_frequency(ozel_karakterler[2], yazidaki_karakter_sayisi)

        tum_harfler = self.find_letters()
        tum_harflerin_sayisi = tum_harfler[1]
        tum_harflerin_frekansi = (tum_harflerin_sayisi * 100) / yazidaki_karakter_sayisi

        sesli_harfler = self.find_vowels()
        sesli_harflerin_sayisi = sesli_harfler[1]
        sesli_harflerin_frekansi = (sesli_harflerin_sayisi * 100) / tum_harflerin_sayisi
        sesli_harflerin_listesi = self.calculate_frequency(sesli_harfler[2], yazidaki_karakter_sayisi)

        sessiz_harfler = self.find_quiets()
        sessiz_harflerin_sayisi = sessiz_harfler[1]
        sessiz_harflerin_frekansi = (sessiz_harflerin_sayisi * 100) / tum_harflerin_sayisi
        sessiz_harflerin_listesi = self.calculate_frequency(sessiz_harfler[2], yazidaki_karakter_sayisi)

        buyuk_harfler = self.find_upper_letters()
        buyuk_harflerin_sayisi = buyuk_harfler[1]
        buyuk_harf_frekans = (buyuk_harflerin_sayisi * 100) / tum_harflerin_sayisi
        buyukle_baslayan = self.find_startswith_upper()
        buyukle_baslayan_sayisi = buyukle_baslayan[1]
        buyukle_baslayan_liste = self.calculate_frequency(buyukle_baslayan[2], buyukle_baslayan_sayisi)
        buyukle_baslayan_liste = buyukle_baslayan_liste[:5]
        buyukle_baslayan_frekans = (buyukle_baslayan_sayisi * 100) / toplam_kelime_sayisi

        kucuk_harfler = self.find_lower_letters()
        kucuk_harflerin_sayisi = kucuk_harfler[1]
        kucuk_harf_frekans = (kucuk_harflerin_sayisi * 100) / tum_harflerin_sayisi

        istatistik = """
    Yazının İstatistiksel Bilgileri :
    ------------------------------------------
    Toplam Satır Sayısı .....................: {0}
    Toplam Boş Satır Sayısı .................: {1} / frq : %{2} (Toplam Satır Sayısına Göre)
    Toplam Yazılı Satır Sayısı ..............: {3} / frq : %{4} (Toplam Satır Sayısına Göre)
    ------------------------------------------
    Toplam Kelime Sayısı ....................: {5}
    Tekrarsız Kelime Sayısı..................: {6}
    En Çok Tekrarlanan ilk 5 Kelime .........: {7}
    ------------------------------------------
    Tüm Karakterin Sayısı ...................: {8}
    Boşluk Karakteri Sayısı .................: {9} / frq : %{10} (Tüm Karakterin Sayısına Göre)
    Toplam Rakam Sayısı .....................: {11} / frq : %{12} (Tüm Karakterin Sayısına Göre)
    Rakamların Listesi ......................: {13}
    Özel Karakterlerin Sayısı ...............: {14} / frq : %{15} (Tüm Karakterin Sayısına Göre)
    Özel Karakterlerin Listesi...............: {16}
    ------------------------------------------
    Tüm Harflerin Sayısı ....................: {17} / frq : %{18} (Tüm Karakterin Sayısına Göre)
    Sesli Harflerin Sayısı ..................: {19} / frq : %{20} (Tüm Harflerin Sayısına Göre)
    Sesli Harflerin Listesi .................: {21}
    Sessiz Harflerin Sayısı .................: {22} / frq : %{23} (Tüm Harflerin Sayısına Göre)
    Sessiz Harflerin Listesi ................: {24}
    ------------------------------------------
    Büyük Harflerin Sayısı ..................: {25} / frq : %{26} (Tüm Harflerin Sayısına Göre)
    Büyük Harfle Başlayan Kelimelerin Sayısı : {27} / frq : %{28} (Toplam Kelime Sayısına Göre)
    Büyük Harfli ilk 5 Kelime ...............: {29}
    Küçük Harflerin Sayısı ..................: {30} / frq : %{31} (Tüm Harflerin Sayısına Göre)
            """.format(toplam_satir_sayisi, toplam_bos_satir_sayisi, bos_satir_frekansi, toplam_yazili_satir_sayisi,
                       yazili_satir_frekansi, toplam_kelime_sayisi, tekrarsiz_kelime_sayisi, tekrarlanan_kelime,
                       yazidaki_karakter_sayisi, yazidaki_bosluk_sayisi, boslu_frekansi, toplam_rakam_sayisi,
                       rakam_frekansi,
                       rakamlarin_listesi, ozel_karakterlerin_sayisi, ozel_karakter_frekans, ozel_karakterlerin_liste,
                       tum_harflerin_sayisi, tum_harflerin_frekansi, sesli_harflerin_sayisi,
                       sesli_harflerin_frekansi, sesli_harflerin_listesi, sessiz_harflerin_sayisi,
                       sessiz_harflerin_frekansi,
                       sessiz_harflerin_listesi, buyuk_harflerin_sayisi, buyuk_harf_frekans, buyukle_baslayan_sayisi,
                       buyukle_baslayan_frekans, buyukle_baslayan_liste, kucuk_harflerin_sayisi, kucuk_harf_frekans)
        return istatistik
