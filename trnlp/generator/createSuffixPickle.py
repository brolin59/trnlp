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

from trnlp.helper import *
from trnlp.controler import ssc
from itertools import product
from trnlp.data.suffix_tables import *
import os
import re

save_folder_path = package_path() + 'data/'


def delete_folder():
    sfx_files = ['dafNoun.pickle', 'dafVerb.pickle', 'infVerb.pickle', 'infNoun.pickle']
    folder_list = os.listdir(save_folder_path)
    for folder_name in folder_list:
        if folder_name in sfx_files:
            os.unlink(save_folder_path + folder_name)
            print(save_folder_path + folder_name + ' dosyası silindi.')


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
    result = list()
    for match in b:
        if '[' not in match.group():
            result.append(match.group())
        else:
            result.append(list(match.group()[1:-1]))
    return [''.join(x) for x in product(*result) if sfx_vowel_harmony(''.join(x), sfx_prop)]


def suffix_suffix_control(suffix_list, suffix_table, suffix_types, suffix_prop):
    temp_dict = {'suffixes'   : suffix_list,
                 'suffixPlace': suffix_table,
                 'suffixProp' : suffix_prop,
                 'suffixTypes': suffix_types}
    if ssc(temp_dict, 0):
        return True
    return False


def enclisis(f_sfx_var_list: list):
    for f_sfx in f_sfx_var_list:
        f_table_number = f_sfx[1][-1][0]
        f_row_number = f_sfx[1][-1][1]
        f_after_sfx_nos = st_dict[f_table_number][f_row_number][4]
        for f_after_sfx_no in f_after_sfx_nos:
            if f_after_sfx_no == -1:
                continue
            if f_after_sfx_no == 0:
                continue
            s_sfx = st_dict[f_table_number][f_after_sfx_no]
            s_sfx_var_list = regex_solver(s_sfx[3], s_sfx[5])
            s_sfx_result = [([ek], [(f_table_number, f_after_sfx_no)], [s_sfx[2]], [s_sfx[5]]) for ek in s_sfx_var_list]
            adding = list(f_sfx)
            adding = [(adding[0] + ekl, adding[1] + positionl, adding[2] + typel, adding[3] + propl)
                      for ekl, positionl, typel, propl in s_sfx_result]
            [f_sfx_var_list.append(add) for add in adding if suffix_suffix_control(add[0], add[1], add[2], add[3])]

    return f_sfx_var_list


def crt(table_str, table_no):
    temp_dict = dict()
    for row_no, row in enumerate(eval(table_str), 0):
        if row_no == 0:
            continue
        if -1 in row[4]:
            harmonic_list = regex_solver(row[3], row[5])
            harmonic_list = [([ek], [(table_no, row_no)], [row[2]], [row[5]]) for ek in harmonic_list]
            for enc_dict in enclisis(harmonic_list):
                clean_ekli = ''.join(enc_dict[0])
                if clean_ekli in temp_dict:
                    temp_dict[clean_ekli].append(enc_dict)
                else:
                    temp_dict[clean_ekli] = [enc_dict]
    return temp_dict


def save_to_file(table_str, dicter):
    if table_str == 'ice':
        table_str = 'infNoun'
    elif table_str == 'fce':
        table_str = 'infVerb'
    compressed_pickle(save_folder_path + table_str, dicter)


def create_suffix_pickle():
    delete_folder()
    daf_noun_dict = dict()
    daf_verb_dict = dict()

    for table_str in st_str_dict:
        print(table_str, 'tablosunun çekimleri yapılıyor...')
        table_no = st_str_dict[table_str]
        result_dict = crt(table_str, table_no)
        if table_no in {1, 2}:
            save_to_file(table_str, result_dict)
        elif table_no in {3, 6, 7, 8, 9}:
            for tmp in result_dict:
                if tmp in daf_verb_dict:
                    daf_verb_dict[tmp] = daf_verb_dict[tmp] + result_dict[tmp]
                else:
                    daf_verb_dict[tmp] = result_dict[tmp]
            continue
        elif table_no in {4, 5}:
            for tmp in result_dict:
                if tmp in daf_noun_dict:
                    daf_noun_dict[tmp] = daf_noun_dict[tmp] + result_dict[tmp]
                else:
                    daf_noun_dict[tmp] = result_dict[tmp]
            continue

    save_to_file('dafVerb', daf_verb_dict)
    save_to_file('dafNoun', daf_noun_dict)


if __name__ == '__main__':
    create_suffix_pickle()
