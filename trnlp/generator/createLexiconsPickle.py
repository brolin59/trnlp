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

Ses Olayları :
1. Ünlü Düşmesi:
    oğul-u > oğlu

2. Ünlü Daralması:
    Sonu düz-geniş ünlü ile biten sözcükler “-yor” ekini aldığında sözcüğün sonundaki
    “a” veya “e” sesi daralarak “ı, i, u, ü” seslerinden birine dönüşür:
    başla-yor > başlıyor

    “de-” ve “ye-” fiilleri “-yor” ekinden başka ekler aldığında da daralmaya uğrar:
    de-y-ecek > diyecek
    ye-y-ecek > yiyecek

3. Ünlü Türemesi:
    Ünsüzle biten bazı sözcükler “-cik” yapım ekini aldığında iki ünsüz arasında bir ünlü türer:
    bir-cik > biricik
    genç-cik > gencecik

4. Ünsüz Yumuşaması
    Sonu “p, ç, t, k” sert ünsüzleri ile biten sözcükler, ünlü ile başlayan bir ek aldığında sözcüğün
    sonundaki bu sert ünsüzler yumuşayarak “b, c, d, g, ğ” ye dönüşür:
    dolap-ı > dolab-ı

5. Ünsüz Düşmesi
    “k” ünsüzüyle biten bazı sözcüklere “-cik/-cek” eklerinden biri geldiğinde sözcük sonundaki “k” ünsüzü düşer:
    çabuk-cak > çabucak
    sıcak-cık > sıcacık
    ufak-cık > ufacık

6. Ünsüz Türemesi (Ünsüz İkizleşmesi)
    Dilimize yabancı dillerden gelen bazı sözcükler, ünlü ile başlayan bir ek aldıklarında ya da ünlüyle
    başlayan bir yardımcı fiille birleştiğinde sözcüğün sonundaki ünsüzden bir tane türer:
    zan et- > zannet-
    af eyle- > affeyle-
    hak-ı > hakkı

1. Ünlü Düşmesi: oğul-u > oğl-u - UDUS +
2. Ünlü Daralması: başla-yor > başlı-yor - UDAR-YOR, UDAR +
3. Ünlü Türemesi: bir-cik > bir-icik - UTUR +
4. Ünsüz Yumuşaması: dolap-ı > dolab-ı - UZYUM +
6. Ünsüz Düşmesi: çabuk-cak > çabu-cak - UZDUS
7. Ünsüz Türemesi (Ünsüz İkizleşmesi): hak-ı > hakkı - UZTUR
"""

from trnlp.generator.createSuffixPickle import create_suffix_pickle
from trnlp.controler import *
from trnlp.finder import *
from trnlp.helper import *
import os
import re

__all__ = ['create_pickles']

gen_dict = {}
find_in_dict = {}


def load_gen_lexicon(lpath):
    with open(lpath, 'r', encoding='utf-8') as fl:
        lexicon = [line.strip().split('\t') for line in fl]
    return lexicon


def save_gen_lexicon(spath):
    compressed_pickle(spath, gen_dict)


def delete_pickle(lpath):
    delete_file_list = ['gen_tr_lex.pbz2', 'prop_tr_lex.pbz2', 'short_tr_lex.pbz2']
    file_list = os.listdir(lpath)
    [os.unlink('{}{}'.format(lpath, fileName)) for fileName in file_list if fileName in delete_file_list]
    print('.lexicons/ klasöründeki *.pickle dosyaları silindi!')


def find_etymon(etm):
    if etm == '0':
        return 'Türkçe'
    else:
        return etm


def arr_line(line):
    result = []
    word = to_lower(line[0])
    word_type = line[1].split(',')
    word_prop = line[2].split(',')
    word_acoustic = acoustic_phenomenon(word, word_prop)

    c_data = {'base'        : word,
              'verifiedBase': base_finder(line[5]),
              'baseType'    : word_type,
              'baseProp'    : word_prop,
              'etymon'      : find_etymon(line[4]),
              'event'       : 0,
              'currentType' : [line[1]]}

    if word_type == ['özel']:
        c_data['base'] = to_lower(base_finder(line[5]))
        c_data['verifiedBase'] = capital_tr(to_lower(c_data['verifiedBase']))
        c_data['purview'] = line[3]
        result.append((word, c_data))
        return result
    elif word_type == ['kısaltma']:
        c_data['verifiedBase'] = line[4]
        c_data['desc'] = line[3]
        result.append((re.sub(r"\W", "", word), c_data))
        return result
    else:
        ver_base = base_finder(line[5])
        ver_base_type = rfind_parenthesize(line[5]).split(',')
        c_data['purview'] = line[3]

        if len(word) == len(to_lower(ver_base)):
            result.append((word, c_data))
            if word_acoustic:
                for aco_word, aco_wordprop in word_acoustic:
                    copy_c_data = dict(c_data)
                    copy_c_data['base'] = aco_word
                    copy_c_data['baseProp'] = aco_wordprop
                    copy_c_data['event'] = 1
                    result.append((aco_word, copy_c_data))
        else:
            if word.startswith(to_lower(ver_base)):
                base_row = find_in_dict[(ver_base, ','.join(ver_base_type))]
                c_data['base'] = to_lower(ver_base)
                c_data['verifiedBase'] = ver_base
                c_data['baseType'] = ver_base_type
                c_data['baseProp'] = base_row[2].split(',')
                c_data['purview'] = base_row[3]
                c_data['etymon'] = find_etymon(base_row[4])
                c_data['event'] = 0
                c_data['currentType'] = [','.join(ver_base_type)]
                result.append((word, c_data))
                if word_acoustic:
                    for aco_word, aco_wordprop in word_acoustic:
                        copy_c_data = dict(c_data)
                        result.append((aco_word, copy_c_data))
            else:
                base_row = find_in_dict[(to_lower(ver_base), ','.join(ver_base_type))]
                base_prop = base_row[2].split(',')
                base_acoustic = acoustic_phenomenon(to_lower(ver_base), base_prop)
                for aco_base, aco_baseprop in base_acoustic:
                    if word.startswith(aco_base):
                        c_data['base'] = aco_base
                        c_data['verifiedBase'] = ver_base
                        c_data['baseType'] = ver_base_type
                        c_data['baseProp'] = aco_baseprop
                        c_data['purview'] = base_row[3]
                        c_data['etymon'] = find_etymon(base_row[4])
                        c_data['event'] = 1
                        c_data['currentType'] = [','.join(ver_base_type)]
                        result.append((word, c_data))
                    if word_acoustic:
                        for aco_word, aco_wordprop in word_acoustic:
                            copy_c_data = dict(c_data)
                            result.append((aco_word, copy_c_data))
    return result


def apply_to_dict(app_dict):
    for base, v in app_dict:
        base = repc(base)
        if base in gen_dict:
            if v not in gen_dict[base]:
                gen_dict[base].append(v)
        else:
            gen_dict[base] = [v]


def create_files(lex):
    global find_in_dict, gen_dict
    find_in_dict = {}
    gen_dict = {}
    for trline in lex:
        find_in_dict[(trline[0], trline[1])] = trline

    for line in lex:
        app_dict = arr_line(line)
        apply_to_dict(app_dict)


def create_pickles():
    p = package_path()

    delete_pickle(p + 'data/')

    lexicons = ((p + 'data/ana_sozluk.txt', p + 'data/gen_tr_lex'),
                (p + 'data/ozel_sozluk.txt', p + 'data/prop_tr_lex'),
                (p + 'data/kisaltma_sozluk.txt', p + 'data/short_tr_lex'))

    for lpath, spath in lexicons:
        trlexicon = load_gen_lexicon(lpath)
        print(lpath, 'dosyası analiz ediliyor...')
        create_files(trlexicon)
        save_gen_lexicon(spath)
        print(spath, 'dosyası başarı ile oluşturuldu.')

    create_suffix_pickle()


if __name__ == '__main__':
    create_pickles()
    del gen_dict
