# -*- coding: utf-8 -*-

__version__ = '0.1'
__author__ = 'Esat Mahmut Bayol'

"""/*

Copyright 2018 Esat Mahmut Bayol

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

# Çok iyi Python bildiğimi söyleyemem. Bildiğim kadarı ile kafamdaki şablonu yazılama dökmeye çalışacağım.
# Amacım bir kelimeyi kök/gövde ve eklerine doğru şekilde ayırabilmek olacak. Allah'ın izni ve yardımı ile yaparız
# inşallah.
# Her işe besmele ile başlanır diyerek kodlamaya başlıyorum. Hayırlara vesile olur inşallah.

# ########## Bismillahirrahmanirrahim ##########

import re
from TurkishNLP import spellword
from TurkishNLP.helpers import to_lower, unrepeated_list, tr_sozluk_yukle, replace_cap_letter, lddistance
from TurkishNLP.Auxiliary.Tr_Suffix_to_Vt import *
from operator import itemgetter

vt_table_name = ek_tipleri

not_get_suffix = ('bağlaç', 'ünlem', 'zarf', '0')
# not_get_suffix demeti ek almayan kelime türlerini içerir. Bu türdeki kelimeler ek aldıklarında isim olurlar.
# '0' zaten kimya sembollerini gösterdiği için ek almaları gibi bir durum olası değil.

sozluk = tr_sozluk_yukle()

isimler = ('isim', 'sıfat', 'zamir', 'edat', 'özel', 'nsz')
fiiller = ('fiil', 'yardımcı fiil')

isim_kok_sozluk = [x for x in sozluk if x[1] in isimler]
fiil_kok_sozluk = [x for x in sozluk if x[1] in fiiller]

dstem_temizleyici = re.compile('(\(.*?\))|({.*?})')

isim_ekler = [('isim_cekim_ekleri',),
              ('isim_ek_fiil_ekleri',),
              ('yardimci_fiiller',),
              ('isim_cekim_ekleri', 'isim_ek_fiil_ekleri')]

fiil_ekler = [('fiil_catisi',),
              ('birlesik_fiil_ekleri',),
              ('fiil_cekim_ekleri',),
              ('x_fiil_ekleri',),
              ('fiil_cekim_ekleri', 'fiil_ek_fiil_ekleri'),
              ('fiil_cekim_ekleri', 'x_fiil_ekleri'),
              ('fiil_catisi', 'fiil_cekim_ekleri'),
              ('birlesik_fiil_ekleri', 'fiil_cekim_ekleri'),
              ('x_fiil_ekleri', 'isim_cekim_ekleri'),
              ('fiil_catisi', 'birlesik_fiil_ekleri', 'fiil_cekim_ekleri')]

tur_dict = {'isim': 'isim_ekler',
            'sıfat': 'isim_ekler',
            'edat': 'isim_ekler',
            'zamir': 'isim_ekler',
            'özel': 'isim_ekler',
            'nsz': 'isim_ekler',
            'fiil': 'fiil_ekler',
            'yardımcı fiil': 'fiil_ekler'}

suffix_shortname = {'isim_ek_fiil_ekleri': 'iefe',
                    'isim_cekim_ekleri': 'içe',
                    'x_fiil_ekleri': 'xfe',
                    'fiil_cekim_ekleri': 'fçe',
                    'fiil_ek_fiil_ekleri': 'fefe',
                    'yardimci_fiiller': 'yf',
                    'birlesik_fiil_ekleri': 'bfe',
                    'fiil_catisi': 'fç'}


class ClsEkBul:
    def __init__(self, word):
        if not word or (word.isalpha is False):
            self.result = []
            self.stem_list = []
        self.stem = []
        word = to_lower(word)
        word = replace_cap_letter(word)
        self.word = word
        self.stem_list = self.find_stem()
        self.result = self.find_suffix(word)
        if self.result:
            self.stem = list(set([x[0] for x in self.result]))
        self.result = list(set(['+'.join(z) for z in self.result]))

    def find_stem(self):
        word = self.word
        temp_stem_list = []
        first_syllable = spellword(word)

        if first_syllable is False:
            return []
        else:
            first_syllable = first_syllable[0]

        search_in_dict = [x for x in sozluk if x[0][:len(first_syllable)] == first_syllable]

        if not search_in_dict and first_syllable[-1] in 'bcdgğ':
            yumusama_harfleri = {'b': 'p',
                                 'c': 'ç',
                                 'd': 't',
                                 'g': 'k',
                                 'ğ': 'k'}
            first_syllable = first_syllable[:-1] + yumusama_harfleri[first_syllable[-1]]
            search_in_dict = [x for x in sozluk if x[0][:len(first_syllable)] == first_syllable]
            if not search_in_dict:
                return []
            else:
                word = first_syllable + word[len(first_syllable):]

        if word.startswith('di'):
            temp_stem_list.append(('di', ('de', 'fiil'), 0))
        elif word.startswith('yi'):
            temp_stem_list.append(('yi', ('ye', 'fiil'), 0))

        mstem = ''
        _mstem = ''
        yor_bul = re.search('[ıiuü]yor', word)
        if yor_bul:
            x, y = yor_bul.span()
            if x == 0:
                yor_bul = re.search('[ıiuü]*yor', word[x:])
                if yor_bul:
                    x, y = yor_bul.span()
                    mstem = word[:x]
                    if yor_bul.group()[0] in ('ı', 'u'):
                        _mstem = mstem + 'a'
                        mstem = word[:x + 1]
                    elif yor_bul.group()[0] in ('i', 'ü'):
                        _mstem = mstem + 'e'
                        mstem = word[:x + 1]
                    else:
                        mstem = ''
            else:
                mstem = word[:x]
                if yor_bul.group()[0] in ('ı', 'u'):
                    _mstem = mstem + 'a'
                    mstem = word[:x + 1]
                elif yor_bul.group()[0] in ('i', 'ü'):
                    _mstem = mstem + 'e'
                    mstem = word[:x + 1]
                else:
                    mstem = ''

        for stem in search_in_dict:

            tlstem = to_lower(stem[0])

            rpstem = replace_cap_letter(tlstem)

            if stem[1] in not_get_suffix:
                if word == rpstem:
                    temp_stem_list.append((stem[0], stem[1], 0))
                    continue
                else:
                    continue

            if mstem and (stem[1] == 'fiil') and (_mstem == rpstem):
                temp_stem_list.append((mstem, (_mstem, stem[1]), 0))

            if word == rpstem:
                temp_stem_list.append((stem[0], stem[1], 0))

            if (word != rpstem) and (word.startswith(rpstem)):
                levenshtein_dist = lddistance(word, rpstem)
                temp_stem_list.append((tlstem, stem[1], levenshtein_dist))
                continue

            letter_harmony = re.findall('\((\w+)\)', stem[2])
            rp_letter_harmony = letter_harmony

            if letter_harmony:
                rp_letter_harmony = replace_cap_letter(rp_letter_harmony[0])
                if word.startswith(rp_letter_harmony):
                    levenshtein_dist = lddistance(word, rp_letter_harmony)
                    temp_stem_list.append((letter_harmony[0], (stem[0], stem[1]), levenshtein_dist))

        organized_list = sorted(unrepeated_list(temp_stem_list), key=itemgetter(2))

        return organized_list

    def arr_word_list(self, word):
        w_g_list = []
        mstem_list = self.stem_list

        if not mstem_list:
            return []

        for stem in mstem_list:

            if type(stem[1]) is tuple:
                suffix = word[len(stem[0]):]
                if suffix:
                    w_list = [stem[0] + '{' + stem[1][0] + '}' + '(' + stem[1][1] + ')', suffix]
                else:
                    w_list = [stem[0] + '{' + stem[1][0] + '}' + '(' + stem[1][1] + ')']
            else:
                suffix = word[len(stem[0]):]
                if suffix:
                    w_list = [stem[0] + '(' + stem[1] + ')', suffix]
                else:
                    w_list = [stem[0] + '(' + stem[1] + ')']

            w_g_list.append(w_list)

        return w_g_list

    def find_suffix(self, word):
        genel = []
        word_list = []
        if type(word) is str:
            word = to_lower(word)
            word_list = self.arr_word_list(word)
        else:
            pass

        if not word_list:
            return []

        for mstem in word_list:
            if len(mstem) > 1:
                suffix = mstem[-1]
            else:
                genel.append(mstem)
                continue

            _stem = mstem[0]
            stem = dstem_temizleyici.sub('', _stem)
            stem_type = _stem[_stem.find('(') + 1:_stem.find(')')]
            fs = self.find_from_list(stem[-1], suffix, stem_type)
            if fs:
                for x in fs:
                    genel.append(mstem[:-1] + x)
        return genel

    def find_from_list(self, last_char, suffix, stem_type):
        genel_liste = []

        def ilk_eki_bul():
            _temp_list = []

            for row in suffix_table_name:
                if -1 not in row[5]:
                    continue

                if row[6] == 2:
                    pass
                else:
                    if row[6] != last_char:
                        continue

                _regex_code = row[4]
                _row_number = row[0]
                _regex = re.match(_regex_code, suffix)

                if _regex:
                    a, b = _regex.span()
                    add = _regex.group() + '(' + row[3] + ')' + '{' + shortname + '-' + _row_number + '}'

                    if suffix[b:]:
                        _temp_list.append([add, suffix[b:]])
                    else:
                        genel_liste.append([add])

            return _temp_list

        lower_vowel = 'aâeêıîioôöuûü'
        lower_quiet = 'bcçdfgğhjklmnprsştvyzqwx'

        if last_char in lower_vowel:
            last_char = 1
        elif last_char in lower_quiet:
            last_char = 0
        else:
            return []

        search_this_list = eval(tur_dict[stem_type])

        for this_tupple in search_this_list:
            temp_list = []
            for i, this in enumerate(this_tupple):
                shortname = suffix_shortname[this]
                suffix_table_name = eval(this)

                if i == 0:
                    temp_list = ilk_eki_bul()
                    if not temp_list:
                        break
                else:
                    if not temp_list:
                        break

                kalan_liste = []
                while temp_list:
                    aranacak_liste = temp_list
                    temp_list = []

                    for ekli_kelimeler in aranacak_liste:
                        ekli_kelimeler = [j for j in ekli_kelimeler if j]
                        if '{' in ekli_kelimeler[-1]:
                            genel_liste.append(ekli_kelimeler)
                            continue

                        kalan_ekler = ekli_kelimeler[-1]
                        ek_no = re.findall('{\w+-(\d+)}', ekli_kelimeler[-2])[-1]
                        ek_no = int(ek_no)

                        son_eklenen_ekin_kisa_adi = re.findall('{(\w+)-\d+}', ekli_kelimeler[-2])[-1]

                        if shortname == son_eklenen_ekin_kisa_adi:
                            ek_tipi_daraltilmis_listesi = [x for x in suffix_table_name if
                                                           int(x[0]) in suffix_table_name[ek_no - 1][5]]
                        else:
                            ek_tipi_daraltilmis_listesi = [x for x in suffix_table_name if
                                                           -1 in x[5]]

                        if not ek_tipi_daraltilmis_listesi:
                            kalan_liste.append(ekli_kelimeler)
                            continue

                        counter = 0
                        for ek_tipi_satiri in ek_tipi_daraltilmis_listesi:
                            row_number = ek_tipi_satiri[0]
                            regex_code = ek_tipi_satiri[4]
                            regex = re.match(regex_code, kalan_ekler)
                            if regex:
                                counter += 1
                                x, y = regex.span()
                                regex = regex.group()
                                kalan = kalan_ekler[y:]
                                if kalan:
                                    ekle = [regex + '(' + ek_tipi_satiri[
                                        3] + ')' + '{' + shortname + '-' + row_number + '}']
                                    ekle = ekli_kelimeler[:-1] + ekle
                                    ekle.append(kalan)
                                    temp_list.append(ekle)
                                else:
                                    ekle = [regex + '(' + ek_tipi_satiri[
                                        3] + ')' + '{' + shortname + '-' + row_number + '}']
                                    ekle = ekli_kelimeler[:-1] + ekle
                                    genel_liste.append(ekle)
                        if counter == 0:
                            kalan_liste.append(ekli_kelimeler)

                if kalan_liste:
                    temp_list = kalan_liste

        return genel_liste


if __name__ == '__main__':
    f = 'bakışlarım'
    e = ClsEkBul(f)
    print(e.result)
    print(e.stem)
