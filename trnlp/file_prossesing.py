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
from trnlp.helper import to_lower, n_gram
from trnlp.tokenization import word_token
from collections import Counter
import shutil
import os

__all__ = ['count_all_txt']


def open_txt(txt_file_path: str):
    try:
        with open(txt_file_path, 'r', encoding='utf-8') as fl:
            txt_file = fl.read()
        del fl
    except UnicodeDecodeError:
        with open(txt_file_path, 'r') as fl:
            txt_file = fl.read()
        del fl
    return txt_file


def huddle_txt_files(folder_path: str):
    def write_to_file(n_lines):
        trg_path = target_path + str(len(os.listdir(target_path)) + 1) + '.txt'
        with open(trg_path, "w", encoding="utf8") as wfl:
            for row in n_lines:
                wfl.write(row + '\n')

    target_path = folder_path + '/trnlp_temp/'

    print('{} geçici klasörü oluşturuluyor...'.format(target_path))

    if os.path.isdir(target_path):
        try:
            shutil.rmtree(target_path)
        except OSError as e:
            print("Error: %s : %s" % (target_path, e.strerror))

    os.makedirs(target_path)

    print('{} klasöründeki .txt dosyaları okunuyor...'.format(folder_path))

    rows = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file[-4:] == '.txt':
                file_path = os.path.join(root, file)
                lines = open_txt(file_path)
                lines = lines.split('\n')
                for line in lines:
                    if line:
                        rows.append(line)

                    if len(rows) == 200000:
                        write_to_file(rows)
                        del rows
                        rows = []
                        continue
    if rows:
        write_to_file(rows)


def count_all_txt(folder_path, ngram=1) -> dict:
    if folder_path.endswith("/"):
        folder_path = folder_path[:-1]

    if os.path.isdir(folder_path):
        pass
    else:
        raise FileNotFoundError("{} klasörü bulunamadı!".format(folder_path))

    counting_word = {}
    counting_word = Counter(counting_word)

    huddle_txt_files(folder_path)

    for root, dirs, files in os.walk(folder_path + '/trnlp_temp/'):
        print('Toplam {} adet dosya bulundu...'.format(len(files)))
        all_txt = ""
        for file in files:
            all_txt = ""
            if file[-4:] == '.txt':
                file_path = os.path.join(root, file)
                lines = open_txt(file_path)
                all_txt = all_txt + lines + '\n'

            print('{} isimli dosya sayılıyor...'.format(file))

            all_txt = [to_lower(low) for low in word_token(all_txt)]

            if ngram == 1:
                counting_word = counting_word + Counter(all_txt)
            else:
                counting_word = counting_word + Counter(n_gram(all_txt, ngram))

        if all_txt:
            counting_word = counting_word + Counter(all_txt)

    counting_word = dict(counting_word)

    print('TÜM DOSYALAR SAYILDI!\n')
    print('{} geçici klasörü siliniyor...'.format(folder_path + '/trnlp_temp/'))

    if os.path.isdir(folder_path + '/trnlp_temp/'):
        try:
            shutil.rmtree(folder_path + '/trnlp_temp/')
        except OSError as e:
            print("Error: %s : %s" % (folder_path + '/trnlp_temp/', e.strerror))

    return counting_word


if __name__ == '__main__':
    pass
