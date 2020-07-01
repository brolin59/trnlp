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

from trnlp.finder import first_vowel, last_vowel
from trnlp.helper import vowel_harmony, word_to_number
from trnlp.data.suffix_tables import *
from itertools import product
from trnlp.constant import *
from trnlp.cleaner import *
import re

__all__ = ['bsc',
           'ssc',
           'abbr_control',
           'general_control',
           'acoustic_phenomenon']


def sfx_vowel_harmony(suffix: str, sfx_prop: tuple) -> bool:
    """
    :param suffix : Sesli uyumunun kontrol edileceği ek
    :param sfx_prop : Sesli uyumunun kontrol edileceği ekin özellik dizisi
    :return: 'True' ya da 'False' döndürür
    """

    if (7 in sfx_prop) or (vowel_harmony(suffix)):
        return True
    return False


def regex_solver(sfx_regex: str, sfx_prop: tuple) -> list:
    """
    :param sfx_regex : Ek tablosundaki ekin regex ifadesi
    :param sfx_prop : Ek tablosundaki ekin özellikler dizisi
    :return: Tüm ihtimalleri liste olarak döndürür
    """

    b = list(re.finditer(r"\w|\[(\w+)\]", sfx_regex))
    result = []
    for match in b:
        if '[' not in match.group():
            result.append(match.group())
        else:
            result.append(list(match.group()[1:-1]))
    return [''.join(x) for x in product(*result) if sfx_vowel_harmony(''.join(x), sfx_prop)]


def abbr_control(cabbr):
    copy_dict = dict(cabbr)
    abbr_prop = cabbr['baseProp']
    abbr_base_split = cabbr['desc'].split(';')
    abbrs = []

    if ('HK' in abbr_prop) or ('SN' in abbr_prop) or ('IHB' in abbr_prop):
        for abbr_base in abbr_base_split:
            copy_dict['base'] = abbr_base
            if bsc(copy_dict) and ssc(copy_dict):
                cabbr['desc'] = abbr_base
                abbrs.append(cabbr)
    elif 'HB' in abbr_prop:
        if 'KG' in abbr_prop:
            if bsc(cabbr) and ssc(cabbr):
                abbrs.append(cabbr)
        else:
            if cabbr['base'][-1] in lowerVowels:
                copy_dict['base'] = cabbr['base'][-1]
                if bsc(copy_dict) and ssc(copy_dict):
                    abbrs.append(cabbr)
            else:
                copy_dict['base'] = cabbr['base'][-1] + 'e'
                if bsc(copy_dict) and ssc(copy_dict):
                    abbrs.append(cabbr)
    return abbrs


def letter_harmony(base: str, first_sfx: str, first_sfx_prop: tuple, suffix_place: tuple) -> bool:
    """
    Kök ile ilk ek arasındaki ses olaylarını kontrol eder.
    :param base: Kelime kökü
    :param first_sfx: ilk ek
    :param first_sfx_prop: İlk ekin özellik listesi
    :param suffix_place: İlk tablodaki yeri
    :return: True ya da False döndürür
    """

    if 0 in first_sfx_prop:
        if base[-1] in allVowels:
            return False
    elif 1 in first_sfx_prop:
        if base[-1] not in allVowels:
            return False

    if 4 in first_sfx_prop:
        if (base[-1] in fortis) and (first_sfx[0] in prefix_lenis):
            return False
        elif (base[-1] not in fortis) and (first_sfx[0] not in prefix_lenis):
            return False
    return True


def base_uyz_control(base: str, f_s: str, suffix_place: tuple,
                     base_prop: tuple, fs_prop: tuple,
                     base_event: int, ver_base: str) -> bool:
    """
    Kök ile ilk ek arasındaki ses uyumunu kontrol eder.
    :param base: Kelime kökü
    :param f_s: ilk ek
    :param suffix_place: ilk ek
    :param base_prop: Kelime kökünün özellik listsi
    :param fs_prop: İlk ekin özellik listesi
    :param base_event: İlk ekin özellik listesi
    :param ver_base: İlk ekin özellik listesi
    :return: True ya da False döndürür
    """

    def hrmny(h_rule):
        scf = first_vowel(f_s)

        if scf:
            if scf in h_rule[blv]:
                return True
            else:
                return False
        else:
            return True

    if (base_event == 1) and ('UDUS' in base_prop):
        base = ver_base

    blv = last_vowel(base)
    if not blv:
        return True

    if 'UYZ' in base_prop:
        if 7 in fs_prop:
            return True
        else:
            return hrmny(incHarmonyRule)
    else:
        if 7 in fs_prop:
            if suffix_place in {(2, 3), (2, 68)}:
                return hrmny(harmonyRule)
            else:
                return True
        else:
            return hrmny(harmonyRule)


def base_gz_control(first_sfx_place: tuple, morph_prop: list, first_sfx: str) -> bool:
    """
    Köke geniş zaman ekleme kontrolü
    :param first_sfx_place: ilk ekin tablodaki yeri
    :param morph_prop: Kelime kökünün özellik listsi
    :param first_sfx: ilk ek
    :return: True ya da False döndürür
    """

    if first_sfx_place in ((2, 7), (2, 8)):
        if ('GZ[r]' in morph_prop) and (first_sfx != 'r'):
            return False
        elif ('GZ[ar]' in morph_prop) and (first_sfx != 'ar'):
            return False
        elif ('GZ[er]' in morph_prop) and (first_sfx != 'er'):
            return False
        elif ('GZ[ır]' in morph_prop) and (first_sfx != 'ır'):
            return False
        elif ('GZ[ir]' in morph_prop) and (first_sfx != 'ir'):
            return False
        elif ('GZ[ür]' in morph_prop) and (first_sfx != 'ür'):
            return False
    return True


def base_utur_control(first_sfx_place: tuple, base_prop: list, first_sfx: str) -> bool:
    """
    Ünlü türemesi kontrolü
    :param first_sfx_place: ilk ekin tablodaki yeri
    :param base_prop: Kelime kökünün özellik listsi
    :param first_sfx: ilk ek
    :return: True ya da False döndürür
    """

    if first_sfx_place == (4, 21):
        if ('UTUR[i]' in base_prop) and (first_sfx[0] != 'i'):
            return False
        elif ('UTUR[a]' in base_prop) and (first_sfx[0] != 'a'):
            return False
        elif ('UTUR[ı]' in base_prop) and (first_sfx[0] != 'ı'):
            return False
        elif ('UTUR[e]' in base_prop) and (first_sfx[0] != 'e'):
            return False
    return True


def base_ch_control(base_prop: tuple, first_sfx: str, suffix_place: tuple) -> bool:
    """
    Ses olayı geçirmiş kökün ilk eke uyum kontrolü
    :param base_prop: Kelime kökünün özellik listsi
    :param first_sfx: ilk ek
    :param suffix_place: eklerin tablo ve sütun değeri
    :return: True ya da False döndürür
    """

    if 'UZTUR' in base_prop:
        if first_sfx[0] not in allVowels:
            return False
    if 'UZYUM' in base_prop:
        if first_sfx[0] not in allVowels:
            return False
    if 'UDUS' in base_prop:
        if first_sfx[0] not in allVowels:
            return False
    if 'UDAR-YOR' in base_prop:
        if suffix_place not in {(2, 4), (2, 67)}:
            return False
    if 'UD' in base_prop:
        if first_sfx[0] in allVowels:
            return False
    if 'UZDUS' in base_prop:
        if suffix_place not in ((4, 6), (4, 28)):
            return False
    if 'UDAR' in base_prop:
        if suffix_place not in {(2, 4), (2, 5), (2, 11), (2, 36), (2, 37), (2, 40), (8, 1), (9, 9)}:
            return False
    return True


def base_control(base_prop: list, first_sfx: str, suffix_place: tuple) -> bool:
    """
    Ses olayı geçirmemiş kökün ilk eke uyum kontrolü
    :param base_prop: Kelime kökünün özellik listsi
    :param first_sfx: ilk ek
    :param suffix_place: eklerin tablo ve sütun değeri
    :return: True ya da False döndürür
    """

    if base_prop == ['0']:
        return True
    if 'UZTUR' in base_prop:
        if first_sfx[0] in allVowels:
            return False
    if 'UZYUM' in base_prop:
        if first_sfx[0] in allVowels:
            return False
    if 'UDUS' in base_prop:
        if first_sfx[0] in allVowels:
            return False
    if 'UDAR-YOR' in base_prop:
        if suffix_place in {(2, 4), (2, 67)}:
            return False
    if 'UD' in base_prop:
        if first_sfx[0] in allVowels:
            return False
    if 'UZDUS' in base_prop:
        if suffix_place in ((4, 6), (4, 28)):
            return False
    if 'UDAR' in base_prop:
        if suffix_place in {(2, 4), (2, 5), (2, 11), (2, 36), (2, 37), (2, 40)}:
            return False
    return True


def bsc(arg: dict) -> bool:
    """
    Kökün ilk eke uyum kontrolü
    :param arg: Kök ek sözlüğü
    :return: True ya da False döndürür
    """

    suffixes = arg['suffixes']

    if not suffixes:
        if arg["event"] == 1:
            return False
        return True
    else:
        suffix = suffixes[0]

    base_type = arg['baseType']

    if base_type == ['bağlaç']:
        return False

    base = arg['base']
    base_prop = arg['baseProp']
    base_event = arg['event']
    ver_base = arg['verifiedBase']
    suffix_place = arg['suffixPlace'][0]
    suffix_prop = arg['suffixProp'][0]

    if 12 in suffix_prop:
        if not word_to_number(ver_base):
            return False

    if not letter_harmony(base, suffix, suffix_prop, suffix_place):
        return False

    if not base_uyz_control(base, suffix, suffix_place, base_prop, suffix_prop, base_event, ver_base):
        return False

    if base_event == 0:
        if not base_control(base_prop, suffix, suffix_place):
            return False
    else:
        if not base_ch_control(base_prop, suffix, suffix_place):
            return False

    if 'fiil' in base_type:
        if not base_gz_control(suffix_place, base_prop, suffix):
            return False

    return True


def ssc_prop_control(suffix_list, suffix_place, suffix_prop):
    len_suffix = len(suffix_list)

    for sfxIndex in range(1, len_suffix):
        f_s = suffix_list[sfxIndex - 1]
        s_s = suffix_list[sfxIndex]
        fs_place = suffix_place[sfxIndex - 1]
        ss_place = suffix_place[sfxIndex]
        ss_prop = suffix_prop[sfxIndex]

        if fs_place == ss_place:
            return False

        if (fs_place in {(2, 67), (2, 68)}) and (ss_place in {(2, 44), (2, 46), (2, 48), (2, 53)}):
            f_s = 'yor'

        if 0 in ss_prop:
            if f_s[-1] in allVowels:
                return False
        elif 1 in ss_prop:
            if f_s[-1] not in allVowels:
                return False

        fs_prop = suffix_prop[sfxIndex - 1]

        if 9 in fs_prop:
            if fs_place[0] != ss_place[0]:
                return False

        if 8 in fs_prop:
            if ss_place != (2, 4):
                return False

        if 4 in ss_prop:
            if (f_s[-1] in fortis) and (s_s[0] in prefix_lenis):
                return False
            if (s_s[0] not in prefix_lenis) and (f_s[-1] not in fortis):
                return False

        if 5 in fs_prop:
            if (s_s[0] in allVowels) and (f_s[-1] not in 'bcdgğ'):
                return False
            elif (f_s[-1] in 'bcdgğ') and (s_s[0] not in allVowels):
                return False

        if 10 in fs_prop:
            if ss_place == (2, 4):
                return False
    return True


def ssc7_control(base, base_prop, suffix_prop, suffix_list):
    sum_suffix = ""
    if ('UYZ' not in base_prop) and (7 not in suffix_prop[0]):
        sum_suffix = last_vowel(base)

    for i, sfxPrp in enumerate(suffix_prop, 0):
        if suffix_list[i] == 'giller':
            if not vowel_harmony(sum_suffix):
                return False
            sum_suffix = 'e'
            continue
        clns = clean_quites(suffix_list[i])
        if 7 in sfxPrp:
            if len(clns) > 1:
                sum_suffix = '{}{}'.format(sum_suffix, clns[0])
                if not vowel_harmony(sum_suffix):
                    return False
            else:
                if not vowel_harmony(sum_suffix):
                    return False
            sum_suffix = clns[-1]
        else:
            sum_suffix = '{}{}'.format(sum_suffix, clns)

    if not vowel_harmony(sum_suffix):
        return False

    return True


def ssc(infdaf: dict, id_status=2) -> bool:
    """
    Tüm eklerin uyum kontrolü
    :param infdaf: Kök ek sözlüğü
    :param id_status: ek türetme için gelen 0, yapım eki için gelenler 1, son hali için gelenler 2
    :return: True ya da False döndürür
    """

    suffix_list = infdaf['suffixes']
    if not suffix_list:
        return True

    suffix_prop = infdaf['suffixProp']

    if id_status == 0:
        if 9 in suffix_prop[-1]:
            return False
    elif id_status == 1:
        if 9 in suffix_prop[-1]:
            return False
    elif id_status == 2:
        if (8 in suffix_prop[-1]) or (9 in suffix_prop[-1]):
            return False
        if (5 in suffix_prop[-1]) and (suffix_list[-1][-1] in 'bcdğ'):
            return False
        if 11 in suffix_prop[-1]:
            return False

    if len(suffix_list) < 2:
        return True

    suffix_types = infdaf['suffixTypes']

    olz_count = suffix_types.count('Olz')
    ytsz_count = suffix_types.count('Ytsz')

    if olz_count + ytsz_count > 2:
        return False

    suffix_place = infdaf['suffixPlace']

    if (5, 2) in suffix_place:
        if olz_count > 0:
            if suffix_types.index('Olz') < suffix_place.index((5, 2)):
                return False
        elif ytsz_count > 0:
            if suffix_types.index('Ytsz') < suffix_place.index((5, 2)):
                return False

    if not elimination(suffix_place):
        return False

    if not ssc_prop_control(suffix_list, suffix_place, suffix_prop):
        return False

    if id_status != 0:
        base_prop = infdaf['baseProp']
        if 'UDUS' in base_prop:
            base = infdaf['verifiedBase']
        else:
            base = infdaf['base']

        if not ssc7_control(base, base_prop, suffix_prop, suffix_list):
            return False
    else:
        if not ssc7_control('', ['UYZ'], suffix_prop, suffix_list):
            return False

    return True


def elimination(suffix_place: list) -> bool:
    """
    Yanlış eklenmiş eklerin bir kısmını temizler
    :param suffix_place: Eklerin tablo, satır listesi
    :return: True ya da False döndürür
    """

    exclude = [[(4, 2), (5, 3)],
               [(4, 3), (5, 3)],
               [(4, 5), (4, 17)],
               [(5, 2), (8, 12)],
               [(5, 2), (6, 7)],
               [(5, 3), (8, 6)],
               [(5, 3), (7, 13)],
               [(5, 3), (7, 12)],
               [(5, 5), (6, 8)],
               [(5, 5), (6, 9)],
               [(5, 5), (7, 13)],
               [(5, 6), (7, 12)],
               [(6, 2), (6, 9)],
               [(6, 3), (6, 9)],
               [(6, 4), (8, 6)],
               [(6, 4), (7, 13)],
               [(6, 6), (6, 9)],
               [(6, 14), (8, 6)],
               [(7, 1), (5, 3)],
               [(7, 3), (5, 3)],
               [(7, 15), (5, 3)],
               [(8, 2), (5, 2)]]

    suffix_place = [suffix_place[i - 2:i] for i in range(2, len(suffix_place) + 1)]
    if any(x in suffix_place for x in exclude):
        return False
    return True


def uzyum(string: str):
    yum = {'ç': 'c', 'p': 'b', 't': 'd', 'k': 'ğ', 'g': 'ğ'}
    if string.endswith('nk'):
        return string[:-1] + 'g'
    else:
        return string[:-1] + yum[string[-1]]


def uztur(string: str):
    return string + string[-1]


def udus(string: str):
    return string[:-2] + string[-1]


def udar(string: str):
    udardict = {'e' : 'i',
                'üe': 'ü',
                'ua': 'u',
                'ee': 'i',
                'aa': 'ı',
                'öe': 'ü',
                'ıa': 'ı',
                'oa': 'u',
                'ie': 'i',
                'ae': 'i',
                'âa': 'ı',
                'oe': 'ü',
                'ue': 'ü'}
    clean = clean_quites(string)
    return string[:-1] + udardict[clean[-2:]]


def uzdus(string: str):
    return string[:-1]


def acoustic_phenomenon(word, wordprop):
    if 'UZYUM' in wordprop:
        if 'UDUS' in wordprop:
            return [(uzyum(udus(word)), wordprop)]
        elif 'UZTUR' in wordprop:
            return [(uztur(uzyum(word)), wordprop)]
        elif 'UZDUS' in wordprop:
            uzyum_prop = [x for x in wordprop if x != 'UZDUS']
            uzdus_prop = [x for x in wordprop if x != 'UZYUM']
            return [(uzyum(word), uzyum_prop), (uzdus(word), uzdus_prop)]
        else:
            return [(uzyum(word), wordprop)]
    elif ('UDAR-YOR' in wordprop) or ('UDAR' in wordprop):
        return [(udar(word), wordprop)]
    elif 'UZTUR' in wordprop:
        return [(uztur(word), wordprop)]
    elif 'UZDUS' in wordprop:
        return [(uzdus(word), wordprop)]
    elif 'UDUS' in wordprop:
        return [(udus(word), wordprop)]
    elif 'UD' in wordprop:
        return [(uzdus(word), wordprop)]


def general_control(arg):
    result = []

    if 'bağlaç' in arg['baseType']:
        return result

    places = arg['suffixPlace']
    in_corrector = [xi for xi in places if xi in corrector_tuple]

    if arg['event'] == 0:
        acoustic = acoustic_phenomenon(arg['base'], arg['baseProp'])
    else:
        acoustic = [(arg['base'], arg['baseProp'])]

    if in_corrector:
        suffixes = []
        suffix_place = []
        suffix_types = []
        suffix_prop = []
        addable = False
        for i, place in enumerate(arg['suffixPlace'], 0):
            if place in corrector_data:
                addable = True
            if addable:
                sp = corrector_data[place]
                s_prop = st_dict[sp[0]][sp[1]][5]
                suffixes.append(regex_solver(st_dict[sp[0]][sp[1]][3], s_prop))
                suffix_place.append(sp)
                suffix_types.append(st_dict[sp[0]][sp[1]][2])
                suffix_prop.append(s_prop)
                addable = False
            else:
                suffixes.append([arg['suffixes'][i]])
                suffix_place.append(place)
                suffix_types.append(arg['suffixTypes'][i])
                suffix_prop.append(arg['suffixProp'][i])

        arg['suffixPlace'] = suffix_place
        arg['suffixTypes'] = suffix_types
        arg['suffixProp'] = suffix_prop

        pro_suffixes = [list(x) for x in product(*suffixes)]

        for sfx in pro_suffixes:
            ctemp = dict(arg)
            ctemp['suffixes'] = sfx
            if bsc(ctemp) and ssc(ctemp):
                ctemp['word'] = ctemp['base'] + ''.join(ctemp['suffixes'])
                result.append(ctemp)
        if (not result) and (acoustic):
            for base, base_prop in acoustic:
                for sfx in pro_suffixes:
                    ctemp = dict(arg)
                    ctemp['base'] = base
                    ctemp['baseProp'] = base_prop
                    ctemp['event'] = 1
                    ctemp['suffixes'] = sfx
                    if bsc(ctemp) and ssc(ctemp):
                        ctemp['word'] = ctemp['base'] + ''.join(ctemp['suffixes'])
                        result.append(ctemp)
    else:
        if bsc(arg) and ssc(arg):
            result.append(arg)
    return result


if __name__ == '__main__':
    pass
