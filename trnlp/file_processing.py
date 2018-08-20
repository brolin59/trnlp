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
import os
from collections import Counter
from operator import itemgetter
import re


# txt_file_path ile belirtilen .txt uzantılı yazı dosyasını olduğu gibi açar.
# Str olarak geri döndürür.
# örnek: open_txt_file('deneme.txt')
def open_txt_file(txt_file_path: str):
    try:
        with open(txt_file_path, 'r', encoding='utf-8') as fl:
            txt_file = fl.read()
        del fl
    except UnicodeDecodeError:
        with open(txt_file_path, 'r') as fl:
            txt_file = fl.read()
        del fl
    return txt_file


# folder_path ile belirtilen klasör içerisindeki tüm .txt uzantılı yazı dosyalarını hafızaya alır.
# Tüm alt klasörleri de tarar.
# Str olarak geri döndürür.
def open_all_txt(folder_path: str):
    all_txt = ''
    for root, dirs, files in os.walk(folder_path):
        print('Toplam {} adet dosya bulundu...'.format(len(files)))
        for file in files:
            print('{} isimli dosya okunuyor...'.format(file))
            if file[-4:] == '.txt':
                file_path = os.path.join(root, file)
                lines = open_txt_file(file_path)
                all_txt = all_txt + lines + '\n'
    print('TÜM DOSYALAR HAFIZAYA ALINDI!')
    return all_txt


# Bu fonksiyon folder_path ile belirtilen klasörü tüm alt klasörleri ile beraber tarayarak .txt uzantılı tüm
#  dosyaları okur. n_type ile belirtilen satır sayısına ulaşıldığında target_path yolu ile belirtilen klasör
#  içerisine 1.txt, 2.txt... şeklinde kaydeder. Özellikle büyük datalar ile uğraşırken yazıları bu şekilde
#  dosyalamak büyük hız kazancı sağlıyor. Örneğin bir klasör içerisindeki 124.000 txt doyanın içerisindeki
#  kelimeleri saymaya kalktığımızda benim bilgisayarım ile yaklaşık 25dk sürerken dosyaları bu komut ile 500.000
#  satır olacak şekilde 18 dosyaya ayırdığımda dosyalama işlemi dahil sayım işlemi 4dk civarında sürmektedir.
def huddle_txt_files(folder_path: str, target_path: str, n_type=500000):
    def write_to_file(n_lines):
        trg_path = target_path + '/' + str(len(os.listdir(target_path)) + 1) + '.txt'
        with open(trg_path, "w", encoding="utf8") as wfl:
            for row in n_lines:
                wfl.write(row + '\n')

    rows = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file[-4:] == '.txt':
                file_path = os.path.join(root, file)
                lines = open_txt_file(file_path)
                lines = lines.split('\n')
                for line in lines:
                    if line:
                        rows.append(line)

                    if len(rows) == n_type:
                        write_to_file(rows)
                        del rows
                        rows = []
                        continue
    if rows:
        write_to_file(rows)


# Bu fonksiyon folder_path ile belirtilen klasörü tüm alt klasörleri ile beraber tarayarak .txt uzantılı tüm
# dosyaları okur. nth ile belirlenen sınıra ulaştığında kelimeleri sayar ve döngüye devam eder. Sonuç olarak
# büyükten küçüğe doğru sıralanmış şekilde kelime listesi olarak döndürür. [('bir', 15),('iki', 12),('üç',8)]
def open_and_count_all_txt(folder_path, nth=499999):
    all_txt = ''
    counting_word = {}
    counting_word = Counter(counting_word)
    for root, dirs, files in os.walk(folder_path):
        print('Toplam {} adet dosya bulundu...'.format(len(files)))
        for file in files:
            print('{} isimli dosya okunuyor...'.format(file))
            if file[-4:] == '.txt':
                file_path = os.path.join(root, file)
                lines = open_txt_file(file_path)
                all_txt = all_txt + lines + '\n'
            print('{} isimli dosya sayılıyor...'.format(file))
            if len(all_txt) > nth:
                all_txt = list(filter(None, re.split('[^A-Za-zçÇğĞıİöÖşŞüÜâÂêÊîÎôÔûÛ]', all_txt)))
                counting_word = counting_word + Counter(all_txt)
                all_txt = ''
        if all_txt:
            counting_word = counting_word + Counter(all_txt)
    counting_word = dict(counting_word)
    print('TÜM DOSYALAR SAYILDI!')
    return sorted(counting_word.items(), key=itemgetter(1), reverse=True)
