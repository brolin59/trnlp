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

# ----------------------------------------------------------------------------- #
# Açıklamalar :                                                                 #
# ----------------------------------------------------------------------------- #

Bu bölümde bir kelimeye eklenebilecek ek tipleri tanımlanmıştır.

Eklerin değişkenleri bir dizi(tuple) içerisinde dizi(tuple) şeklinde tanımlanmıştır. Bu format bir tablo ya da matris
gibi düşünülebilir.

Ana dizinin ilk satırındaki sayı o değişkene atanmış tablo numarısını içerir. Örneğin isim_cekim_ekleri tablosu 2 nolu
tablodur.

Ekler ikinci satırdan(1 indexinden) itibaren tanımlanmaya başlanmıştır.

Her bir ek dizisinin elemanları sırası ile aşağıdaki gibidir:

    1. Dizi Elemanı(0. indeks)     : Ekin satır numarası(indeksi).

    2. Dizi Elemanı(1. indeks)     : Ekin ait olduğu grubun numarası.
        *** 1. ve 2. değerler sadece tabloyu okumayı kolaylaştırmak adına kullanılmıştır.

    3. Dizi Elemanı(2. indeks)     : Ekin adının kısaltılmış şekli.
                                    (Kısaltma listeleri SUFFIX_SHORTLIST sözlüğünde belirtilmiştir.)

    4. Dizi Elemanı(3. indeks)     : Ekin regex formatında yazılışı.

    5. Dizi Elemanı(4. indeks)     : Bu ekten sonra gelebilecek eklerin satır numaraları.
        *** 0 bu ekten sonra başka bir ek gelemeyeceğini, -1 ise bu ekin başlangıç eki olarak kullanılabileceğini
        ifade eder.

    6. Dizi Elemanı(5. indeks)     : Ekte gerçekleşebilecek ses olaylarının numaralandırılmış şekli.
        Ses olaylarını temsil eden sayıların açıklamaları aşağıdaki gibidir :
        Önceki harf ünsüz(Sessiz)                       : 0
        Önceki harf ünlü(Sesli)                         : 1
        Önceki harf ünlü(Sesli) veya ünlüz(Sessiz)      : 2
        Kaynaştırma harfi                               : 3
        Ünsüz(Sessiz) Sertleşmesi                       : 4
        Ünsüz(Sessiz) Yumuşaması                        : 5
        Ünlü(Sesli) Türemesi                            : 6
        Ünlü(Sesli) uyumunu bozan ek                    : 7
        Sadece -yor ekinden önce gelebilen ek           : 8
        Sonrasında mutlaka kendi tablosundan ek olmalı  : 9
        Sonrasında -yor eki gelemez                     : 10
        Son ek olarak kullanılmaz                       : 11
        Sayılara gelebilen ek                           : 12
        Çoğul ek                                        : 13
"""

ice = (1,
       (1, 0, 'Çe', 'l[ae]r', (-1, 2, 4, 6, 8, 11, 14, 17, 20, 21, 23, 26, 28, 36, 38, 40, 42, 44, 46, 48, 50),
        (2, 13)),
       (2, 1, 'İe1t', '[ıiuü]m', (-1, 14, 17, 20, 21, 23, 26, 28, 36, 38, 40, 44, 46, 48, 50, 54), (0, 6)),
       (3, 1, 'İe1t', 'm', (-1, 14, 17, 20, 21, 23, 26, 28, 36, 38, 40, 44, 46, 48, 50, 54), (1,)),
       (4, 1, 'İe1ç', '[ıiuü]m[ıiuü]z', (-1, 14, 17, 20, 21, 23, 26, 28, 36, 38, 40, 44, 46, 50, 54), (0, 6, 13)),
       (5, 1, 'İe1ç', 'm[ıiuü]z', (-1, 14, 17, 20, 21, 23, 26, 28, 36, 38, 40, 44, 46, 50, 54), (1, 13)),
       (6, 1, 'İe2t', '[ıiuü]n', (-1, 14, 17, 20, 21, 23, 26, 28, 36, 38, 40, 42, 44, 46, 48, 50, 54), (0, 6)),
       (7, 1, 'İe2t', 'n', (-1, 14, 17, 20, 21, 23, 26, 28, 36, 38, 40, 42, 44, 46, 48, 50, 54), (1,)),
       (8, 1, 'İe2ç', '[ıiuü]n[ıiuü]z', (-1, 14, 17, 20, 21, 23, 26, 28, 36, 38, 40, 42, 46, 54), (0, 6, 13)),
       (9, 1, 'İe2ç', 'n[ıiuü]z', (-1, 14, 17, 20, 21, 23, 26, 28, 36, 38, 40, 42, 46, 54), (1, 13)),
       (10, 1, 'İe3t', 's[ıiuü]', (-1, 15, 16, 18, 22, 24, 25, 29, 35, 37, 39, 41, 44, 46, 47, 50, 54), (1, 3)),
       (11, 1, 'İe3t', '[ıiuü]', (-1, 15, 16, 18, 22, 24, 25, 29, 35, 37, 39, 41, 44, 46, 47, 50, 54, 56), (0,)),
       (12, 1, 'İe3ç', 'l[ae]r[ıi]', (-1, 15, 16, 18, 22, 24, 25, 29, 35, 37, 39, 41, 44, 46, 47, 50, 54), (2, 13)),
       (13, 2, 'HeBlrt', 'y[ıiuü]', (-1, 3, 5, 7, 9, 15, 16), (1, 3)),
       (14, 2, 'HeBlrt', '[ıiuü]', (-1,), (0,)),
       (15, 2, 'HeBlrt', 'n[ıiuü]', (39,), (1, 3)),
       (16, 2, 'HeTyn', 'n[ıiuü]n', (-1, 27, 36, 38, 40, 42, 44, 46, 48, 50, 54), (1, 3)),
       (17, 2, 'HeTyn', '[ıiuü]n', (-1, 27, 36, 38, 40, 42, 44, 46, 48, 50, 54), (0,)),
       (18, 2, 'HeYak', 'n[ae]', (35, 37, 39, 46), (1, 3)),
       (19, 2, 'HeYak', 'y[ae]', (-1, 35, 37, 39), (1, 3)),
       (20, 2, 'HeYak', '[ae]', (-1, 39, 46), (0,)),
       (21, 2, 'HeBul', '[dt][ae]', (-1, 27, 35, 37, 39, 41, 44, 46, 47, 50, 52, 54, 56), (2, 4)),
       (22, 2, 'HeBul', 'nd[ae]', (27, 35, 37, 39, 41, 44, 46, 47, 50, 54, 56), (1, 3)),
       (23, 2, 'HeUzk', '[dt][ae]n', (-1, 36, 38, 40, 42, 44, 46, 48, 50, 52, 53, 54), (2, 4)),
       (24, 2, 'HeUzk', 'nd[ae]n', (-1, 36, 38, 40, 42, 44, 46, 48, 50, 52, 53, 54), (1, 3)),
       (25, 2, 'HeVas', 'yl[ae]', (-1, 35, 37, 39, 41, 44, 46, 47, 50, 52, 53, 54), (1, 3)),
       (26, 2, 'HeVas', 'l[ae]', (-1, 35, 37, 39, 41, 44, 46, 47, 50, 52, 53, 54), (0,)),
       (27, 3, 'Ait', 'ki', (-1, 30, 15, 33, 18, 31, 24, 25, 35, 37, 39, 41, 44, 46, 47, 50, 52, 53, 54), (2, 7)),
       (28, 2, 'HeGör', '[cç][ae]', (-1, 35, 37, 39, 41, 44, 46, 50, 52, 53, 54), (2, 4)),
       (29, 2, 'HeGör', 'nc[ae]', (35, 37, 39, 41, 44, 46, 50, 52, 53, 54), (1, 3)),
       (30, 4, 'Çe', 'l[ae]r', (14, 20, 23, 26, 28, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50), (1, 13)),
       (31, 5, 'HeBul', 'nd[ae]', (35, 37, 39, 41, 44, 46, 47, 50, 54), (1, 3)),
       (32, 5, 'HeBul', '[dt][ae]', (35, 37, 39, 41, 44, 46, 47, 50, 54), (2, 4)),
       (33, 5, 'HeTyn', 'n[ıiuü]n', (36, 38, 40, 42, 44, 46, 48, 50, 54), (1, 3)),
       (34, 5, 'HeTyn', '[ıiuü]n', (36, 38, 40, 42, 44, 46, 48, 50, 54), (0,)),
       (35, 0, 'EfGçDi', 'yd[ıiuü]', (-1, 43, 45, 49, 51, 52), (1, 3)),
       (36, 0, 'EfGçDi', '[dt][ıiuü]', (-1, 43, 45, 49, 51, 52), (0, 4)),
       (37, 0, 'EfGçMiş', 'ym[ıiuü]ş', (-1, 42, 44, 46, 48, 50, 52, 57), (1, 3)),
       (38, 0, 'EfGçMiş', 'm[ıiuü]ş', (-1, 42, 44, 46, 48, 50, 52, 53, 54, 57), (0,)),
       (39, 0, 'EfKŞrt', 'ys[ea]', (-1, 43, 45, 49, 51, 52), (1, 3)),
       (40, 0, 'EfKŞrt', 's[ea]', (-1, 43, 45, 49, 51, 52), (0,)),
       (41, 1, 'EfKe1t', 'y[ıiuü]m', (-1, 46), (1, 3, 6)),
       (42, 1, 'EfKe1t', '[ıiuü]m', (-1,), (0, 6)),
       (43, 1, 'EfKe1t', 'm', (0,), (1,)),
       (44, 1, 'EfKe2t', 's[ıiuü]n', (-1,), (2, 3, 6)),
       (45, 1, 'EfKe2t', 'n', (0,), (1,)),
       (46, 1, 'EfGz', '[dt][ıiuü]r', (-1,), (2, 4)),
       (47, 1, 'EfKe1ç', 'y[ıiuü]z', (-1, 46), (1, 3, 13)),
       (48, 1, 'EfKe1ç', '[ıiuü]z', (-1, 46), (0, 13)),
       (49, 1, 'EfKe1ç', 'k', (0,), (1, 13)),
       (50, 1, 'EfKe2ç', 's[ıiuü]n[ıiuü]z', (-1, 46), (2, 3, 6, 13)),
       (51, 1, 'EfKe2ç', 'n[ıiuü]z', (0,), (1, 13)),
       (52, 1, 'EfKe3ç', 'l[ae]r', (-1,), (2, 13)),
       (53, 1, 'EfKe3ç', 'l[ae]rd[ıi]r', (-1,), (2, 13)),
       (54, 1, 'EfKe3ç', '[dt][ıiuü]rl[ae]r', (-1,), (2, 4, 13)),
       (55, 2, 'Ye-Fz', 'ken', (-1,), (0, 7)),
       (56, 2, 'Ye-Fz', 'yken', (-1,), (1, 7)),
       (57, 2, 'Ye-Fz', '[cç][ae]s[ıi]n[ae]', (0,), (0, 4)))

fce = (2,
       (1, 1, 'GçDi', '[dt][ıiuü]', (-1, 21, 23, 27, 29, 30, 43, 47), (2, 4)),
       (2, 1, 'GçMiş', 'm[ıiuü]ş', (-1, 20, 22, 24, 28, 30, 32, 44, 46, 48, 53, 60), (2,)),
       (3, 1, 'Şz', '[ıiuü]yor', (-1, 20, 22, 24, 28, 30, 32, 44, 46, 48, 49, 51, 53, 55, 57, 59, 60), (0, 6, 7)),
       (4, 1, 'Şz', 'yor', (-1, 20, 22, 24, 28, 30, 32, 44, 46, 48, 53, 60), (1, 7)),
       (5, 1, 'Gkz', 'y[ae]c[ae][kğ]', (-1, 20, 22, 24, 28, 30, 32, 44, 46, 48, 53), (1, 3, 5)),
       (6, 1, 'Gkz', '[ae]c[ae][kğ]', (-1, 20, 22, 24, 28, 30, 32, 44, 46, 48, 53), (0, 5)),
       (7, 1, 'Gz', '[aeıiuü]r', (-1, 20, 22, 24, 28, 30, 32, 44, 46, 48, 60), (0,)),
       (8, 1, 'Gz', 'r', (-1, 20, 22, 24, 28, 30, 32, 44, 46, 48), (1,)),
       (9, 1, 'Grlk', 'm[ae]l[ıi]', (-1, 19, 22, 25, 28, 30, 43, 45, 47, 53), (2,)),
       (10, 1, 'KŞrt', 's[ae]', (-1, 21, 23, 27, 29, 30, 43, 45), (2,)),
       (11, 1, 'Kİtk', 'y[ae]', (-1, 19, 22, 26, 28, 30, 43, 45), (1, 3)),
       (12, 1, 'Kİtk', '[ae]', (-1, 19, 22, 26, 28, 30, 43, 45), (0,)),
       (13, 1, 'KEmr', 's[ıiuü]n', (-1,), (2,)),
       (14, 1, 'KEmr', 'y[ıiuü]n[ıiuü]z', (-1,), (1, 3)),
       (15, 1, 'KEmr', '[ıiuü]n[ıiuü]z', (-1,), (0,)),
       (16, 1, 'KEmr', 'y[ıiuü]n', (-1,), (1, 3)),
       (17, 1, 'KEmr', '[ıiuü]n', (-1,), (0,)),
       (18, 1, 'KEmr', 's[ıiuü]nl[ae]r', (-1,), (2,)),
       (19, 1, 'Ke1t', 'y[ıiuü]m', (0,), (1, 3, 6)),
       (20, 1, 'Ke1t', '[ıiuü]m', (54,), (0, 6)),
       (21, 1, 'Ke1t', 'm', (48, 54), (1,)),
       (22, 1, 'Ke2t', 's[ıiuü]n', (54,), (2, 3, 6)),
       (23, 1, 'Ke2t', 'n', (0,), (1,)),
       (24, 1, 'Ke1ç', '[ıiuü]z', (0,), (0, 13)),
       (25, 1, 'Ke1ç', 'y[ıiuü]z', (0,), (1, 3, 13)),
       (26, 1, 'Ke1ç', 'l[ıi]m', (0,), (2, 13)),
       (27, 1, 'Ke1ç', 'k', (0,), (1, 13)),
       (28, 1, 'Ke2ç', 's[ıiuü]n[ıiuü]z', (54, 60), (2, 3, 6, 13)),
       (29, 1, 'Ke2ç', 'n[ıiuü]z', (0,), (2, 13)),
       (30, 1, 'Ke3ç', 'l[ae]r', (44, 46, 48, 53), (2, 13)),
       (31, 1, 'KEmr', 's[ıiuü]n[ıiuü]z', (-1,), (1,)),
       (32, 1, 'Ye-Fz', 'ken', (0,), (0, 7)),
       (33, 1, 'KEmr', 's[ae]n[ae]', (-1,), (2,)),
       (34, 1, 'Olz', 'm[ae]', (-1, 1, 2, 5, 9, 10, 11, 13, 14, 16, 18, 19, 21, 22, 25, 33), (2,)),
       (35, 1, 'Olz', 'm[ıiuü]', (-1, 4), (2, 8)),
       (36, 1, 'Ytsz', 'y[ae]m[ae]', (-1, 1, 2, 5, 9, 10, 11, 13, 14, 16, 18, 19, 21, 25), (1, 3)),
       (37, 1, 'Ytsz', 'y[ae]m[ıi]', (-1, 4), (1, 3, 8)),
       (38, 1, 'Ytsz', '[ae]m[ae]', (-1, 1, 2, 5, 9, 10, 11, 13, 14, 16, 18, 19, 21, 25), (0,)),
       (39, 1, 'Ytsz', '[ae]m[ıi]', (-1, 4), (0, 8)),
       (40, 1, 'Ytsz', 'y[ae]m[ae]z', (-1, 1, 2, 10, 13, 22, 24, 28, 30), (1, 3)),
       (41, 1, 'Ytsz', '[ae]m[ae]z', (-1, 1, 2, 10, 13, 28, 30), (0,)),
       (42, 1, 'Olz', 'm[ae]z', (-1, 1, 2, 10, 13, 28, 30), (2,)),
       (43, 1, 'EfGçDi', 'yd[ıiuü]', (50, 52, 56, 58, 59), (1, 3)),
       (44, 1, 'EfGçDi', '[dt][ıiuü]', (47, 50, 52, 56, 58, 59), (0, 4)),
       (45, 1, 'EfGçMiş', 'ym[ıiuü]ş', (49, 51, 55, 57, 59, 61), (1, 3)),
       (46, 1, 'EfGçMiş', 'm[ıiuü]ş', (49, 51, 55, 57, 59, 60, 61), (0,)),
       (47, 1, 'EfKŞrt', 'ys[ea]', (50, 52, 56, 58, 59), (1, 3)),
       (48, 1, 'EfKŞrt', 's[ea]', (50, 52, 56, 58, 59), (0,)),
       (49, 1, 'EfKe1t', '[ıiuü]m', (54,), (0, 6)),
       (50, 1, 'EfKe1t', 'm', (0,), (1,)),
       (51, 1, 'EfKe2t', 's[ıiuü]n', (54,), (0, 3, 6)),
       (52, 1, 'EfKe2t', 'n', (0,), (1,)),
       (53, 1, 'EfGz', '[dt][ıiuü]r', (-1, 59), (0, 4)),
       (54, 1, 'EfGz', '[dt][ıiuü]r', (0,), (0, 4)),
       (55, 1, 'EfKe1ç', '[ıiuü]z', (54,), (0, 13)),
       (56, 1, 'EfKe1ç', 'k', (0,), (1, 13)),
       (57, 1, 'EfKe2ç', 's[ıiuü]n[ıiuü]z', (54,), (0, 3, 6, 13)),
       (58, 1, 'EfKe2ç', 'n[ıiuü]z', (0,), (1, 13)),
       (59, 1, 'EfKe3ç', 'l[ae]r', (54,), (2, 13)),
       (60, 1, 'Ye-Fz', '[cç][ae]s[ıi]n[ae]', (0,), (0, 4)),
       (61, 1, 'Ye-Fz', 'ken', (-1,), (0, 7)),
       (62, 1, 'Yv-Ke1ç', 'z', (0,), (1, 13)),
       (63, 1, 'Yv-Gkz', '[aeıi]c[ae]', (-1, 21, 23, 62), (0,)),
       (64, 1, 'Yv-Gkz', 'y[aeıi]c[ae]', (-1, 21, 23, 62), (1,)),
       (65, 1, 'Yv-Gkz', '[cç][ae]', (-1, 21, 23, 62), (0, 4)),
       (66, 1, 'Yv-Gkz', 'yc[ae]', (-1, 21, 23, 62), (1,)),
       (67, 1, 'Yv-Şz', 'yo', (-1, 21, 22, 23, 62, 28, 30, 44, 46, 48, 53), (1, 7)),
       (68, 1, 'Yv-Şz', '[ıiuü]yo', (-1, 21, 22, 23, 62, 28, 30, 44, 46, 48, 53), (0, 7)))

corrector_tuple = ((2, 63), (2, 64), (2, 65), (2, 66), (2, 67), (2, 68), (4, 32))
corrector_data = {(2, 62): (2, 24),
                  (2, 63): (2, 6),
                  (2, 64): (2, 5),
                  (2, 65): (2, 6),
                  (2, 66): (2, 5),
                  (2, 67): (2, 4),
                  (2, 68): (2, 3),
                  (2, 21): (2, 20),
                  (2, 23): (2, 22),
                  (4, 32): (4, 6),
                  (1, 3) : (1, 2),
                  }

bfe = (3,
       (1, 1, 'BfBil', 'y[ae]bil', (-1,), (1, 3, 7)),
       (2, 1, 'BfBil', '[ae]bil', (-1,), (0, 6, 7)),
       (3, 1, 'BfVer', 'y[ıiuü]ver', (-1,), (1, 3, 7)),
       (4, 1, 'BfVer', '[ıiuü]ver', (-1,), (0, 6, 7)),
       (5, 1, 'BfGel', 'y[ae]gel', (-1,), (1, 3, 7)),
       (6, 1, 'BfGel', '[ae]gel', (-1,), (0, 6, 7)),
       (7, 1, 'BfDur', 'y[ae]dur', (-1,), (1, 3, 7)),
       (8, 1, 'BfDur', '[ae]dur', (-1,), (0, 6, 7)),
       (9, 1, 'BfGör', 'y[ae]gör', (-1,), (1, 3, 7)),
       (10, 1, 'BfGör', '[ae]gör', (-1,), (0, 6, 7)),
       (11, 1, 'BfKal', 'y[ae]kal', (-1,), (1, 3, 7)),
       (12, 1, 'BfKal', '[ae]kal', (-1,), (0, 6, 7)),
       (13, 1, 'BfKoy', 'y[ae]koy', (-1,), (1, 3, 7)),
       (14, 1, 'BfKoy', '[ae]koy', (-1,), (0, 6, 7)),
       (15, 1, 'BfYaz', 'y[ae]yaz', (-1,), (1, 3, 7)),
       (16, 1, 'BfYaz', '[ae]yaz', (-1,), (0, 6, 7)),
       (17, 1, 'Olz', 'm[ae]', (-1, 1, 3, 5, 7, 9, 11, 13, 15), (2, 9)),
       (18, 1, 'Ytsz', 'y[ae]m[ae]', (-1, 1, 3, 5, 7, 9, 11, 13, 15), (1, 3, 9)),
       (19, 1, 'Ytsz', '[ae]m[ae]', (-1, 1, 3, 5, 7, 9, 11, 13, 15), (0, 9)))

ii = (4,
      (1, 1, 'İi', 'l[ıiuü][kğ]', (-1,), (2, 5)),
      (2, 1, 'İi', '[cç][ıiuü]', (-1, 1), (2, 4)),
      (3, 1, 'İi', 'l[ıiuü]', (-1, 1), (2,)),
      (4, 1, 'İi', 's[ıiuü]z', (-1, 1, 13), (2,)),
      (5, 1, 'İi', '[cç][ıiuü]l', (-1,), (2, 4)),
      (6, 1, 'İi', '[cç][ıiuü][kğ]', (-1,), (2, 4, 5)),
      (7, 1, 'İi', 'nc[ıiuü]', (-1,), (1,)),
      (8, 1, 'İi', '[ıiuü]nc[ıiuü]', (-1,), (0,)),
      (9, 1, 'İi', 'ms[ıiuü]', (-1,), (1,)),
      (10, 1, 'İi', '[ıiuü]ms[ıiuü]', (-1,), (0,)),
      (11, 1, 'İi', 's[ae]l', (-1, 1), (2,)),
      (12, 1, 'İi', 't[ıiuü]', (-1,), (2,)),
      (13, 1, 'İi', '[cç][ae]', (-1,), (2, 4)),
      (14, 1, 'İi', 'mtırak', (-1, 1), (2, 7)),
      (15, 1, 'İi', '[ıiuü]mtırak', (-1,), (2, 6, 7)),
      (16, 1, 'İi', 'l[ae]y[ıi]n', (-1,), (2,)),
      (17, 1, 'İi', '[ae]r', (-1, 1, 3), (0, 12)),
      (18, 1, 'İi', 'ş[ae]r', (-1, 1, 3), (1, 3, 12)),
      (19, 1, 'İi', 'gil', (-1,), (2, 7)),
      (20, 1, 'İi', 'm[ae]n', (-1,), (2,)),
      (21, 1, 'İi', '[aeıi]c[ıi][kğ]', (-1,), (0, 5)),
      (22, 1, 'İi', 's[ıiuü]', (-1,), (0,)),
      (23, 1, 'İi', 'la', (-1,), (0,)),
      (24, 1, 'İi', 'l[ae]r', (0,), (2, 13)),
      (25, 1, 'İi', '[cç][ae]ğ[ıi]z', (-1,), (2, 4)),
      (26, 1, 'İi', '[dt][ae]ş', (-1,), (2, 4)),
      (27, 1, 'İi', 'giller', (-1,), (2, 7, 13)),
      (28, 1, 'İi', 'c[ae][kğ]', (-1,), (1, 5)),
      (29, 1, 'İe1t', 'm', (-1, 1, 19, 24, 27), (1, 9)),
      (30, 1, 'İe1t', 'n', (-1, 1, 19, 24, 27), (1, 9)),
      (31, 1, 'İe1t', '[gk][ıiuü]', (-1,), (0,)),
      (32, 1, 'Yv-İi', '[cç][ıiuü]', (-1,), (2, 4)))

ifi = (5,
       (1, 1, 'İf', 's[ae]', (-1,), (2, 10)),
       (2, 1, 'İf', 'l[ae]', (-1,), (2, 10)),
       (3, 1, 'İf', 'l', (-1,), (1,)),
       (4, 1, 'İf', 'd[ae]', (-1,), (2, 10)),
       (5, 1, 'İf', 'l[ae][ştn]', (-1,), (2,)),
       (6, 1, 'İf', 'e[dt]', (-1,), (2, 5, 7)),
       (7, 1, 'İf', 'ol', (-1,), (2, 7)),
       (8, 1, 'İf', 'l[ıiuü]', (-1,), (2, 8)),
       (9, 1, 'İf', '[ae]l', (-1,), (0,)),
       (10, 1, 'İf', 's[ıiuü]', (-1,), (2, 8)),
       (12, 1, 'İf', 'd[ıiuü]', (-1,), (2, 8)),
       (13, 1, 'İf', '[ıiuü]ms[ae]', (-1,), (0, 10)),
       (14, 1, 'İf', 'ms[ae]', (-1,), (1,)),
       (15, 1, 'İf', '[ıiuü]ms[ıiuü]', (-1,), (0, 8)),
       (16, 1, 'İf', 'ms[ıiuü]', (-1,), (1, 8)),
       (17, 1, 'İf', 'eyle', (-1,), (0, 7)))

ff = (6,
      (1, 1, 'Ff', '[ae]l[ae]', (-1,), (0, 10)),
      (2, 1, 'Ff', '[ıiuü]n', (-1, 11), (0,)),
      (3, 1, 'Ff', 'n', (-1,), (1,)),
      (4, 1, 'Ff', '[ıiuü]l', (-1,), (0,)),
      (5, 1, 'Ff', '[ıiuü]ş', (-1,), (0,)),
      (6, 1, 'Ff', 'ş', (-1,), (1,)),
      (7, 1, 'Ff', '[aeıiuü]r', (-1,), (0,)),
      (8, 1, 'Ff', 't', (-1, 4), (2,)),
      (9, 1, 'Ff', '[ıiuü]t', (-1,), (0,)),
      (10, 1, 'Ff', '[dt][ıiuü]r', (-1, 4, 8), (2, 4)),
      (11, 1, 'Ff', '[ıiuü]ms[ae]', (-1,), (0, 10)),
      (12, 1, 'Ff', '[ae]l[ıiuü]', (-1,), (0, 8)),
      (13, 1, 'Ff', '[ıiuü]ms[ıiuü]', (-1,), (0, 8)),
      (14, 1, 'Ff', 'l', (-1,), (1,)))

fi = (7,
      (1, 1, 'Fi', 'm[ae]', (-1,), (2,)),
      (2, 1, 'Fi', 'm[ae]k', (-1,), (2,)),
      (3, 1, 'Fi', '[ıiuü]c[ıiuü]', (-1,), (0,)),
      (4, 1, 'Fi', 'y[ıiuü]c[ıiuü]', (-1,), (1, 3)),
      (5, 1, 'Fi', '[ıiuü]ş', (-1,), (2,)),
      (6, 1, 'Fi', 'y[ıiuü]ş', (-1,), (1, 3)),
      (7, 1, 'Fi', '[ıiuü]m', (-1,), (0,)),
      (8, 1, 'Fi', 'm[ae]n', (-1,), (0,)),
      (9, 1, 'Fi', 'g[ıiuü]n', (-1,), (0,)),
      (10, 1, 'Fi', 'k[ıiuü]n', (-1,), (0,)),
      (11, 1, 'Fi', '[ıiuü][kğ]', (-1,), (0,)),
      (12, 1, 'Fi', 'k', (-1,), (1,)),
      (13, 1, 'Fi', 'a', (-1,), (0,)),
      (14, 1, 'Fi', '[gk][ae]n', (-1,), (0, 4)),
      (15, 1, 'Fi', 't[ıiuü]', (-1,), (0,)),
      (16, 1, 'Olz', 'm[ae]', (-1, 1, 2, 4, 6), (2, 9)),
      (17, 1, 'Ytsz', 'y[ae]m[ae]', (-1, 1, 2, 4, 6), (1, 3, 9)),
      (18, 1, 'Ytsz', '[ae]m[ae]', (-1, 1, 2, 4, 6), (0, 9)),
      (19, 1, 'Fi', '[ıiuü]k', (-1,), (0,)),
      (20, 1, 'Fi', '[ae][çc]', (-1,), (0, 5)),
      (21, 1, 'Fi', 'g[ae]', (-1,), (0,)),
      (22, 1, 'Fi', '[gk][ae]ç', (-1,), (0, 4)),
      )

fs = (8,
      (1, 1, 'Fs', 'y[ae]n', (-1,), (1, 3)),
      (2, 1, 'Fs', '[ae]n', (-1,), (0,)),
      (3, 1, 'Fs', 'y[ae]s[ıi]', (-1,), (1, 3)),
      (4, 1, 'Fs', '[ae]s[ıi]', (-1,), (0,)),
      (5, 1, 'Fs', 'm[ea]z', (-1,), (2,)),
      (6, 1, 'Fs', '[ea]r', (-1,), (2,)),
      (7, 1, 'Fs', '[dt][ıiuü][kğ]', (-1,), (2, 4, 5)),
      (8, 1, 'Fs', 'y[ae]c[ae][kğ]', (-1,), (1, 3, 5)),
      (9, 1, 'Fs', '[ae]c[ae][kğ]', (-1,), (0, 5)),
      (10, 1, 'Fs', 'm[ıiuü]ş', (-1,), (2,)),
      (11, 1, 'Fs', '[ıiuü]r', (-1,), (0,)),
      (12, 1, 'Fs', 'r', (-1,), (1,)),
      (13, 1, 'Olz', 'm[ae]', (-1, 1, 7, 8, 10), (2, 9)),
      (14, 1, 'Ytsz', 'y[ae]m[ae]', (-1, 1, 7, 8, 10), (1, 3, 9)),
      (15, 1, 'Ytsz', '[ae]m[ae]', (-1, 1, 7, 8, 10), (0, 9)))

fz = (9,
      (1, 1, 'Fz', 'ken', (-1,), (0, 7)),
      (2, 1, 'Fz', 'y[ae]l[ıi]', (-1,), (1, 3)),
      (3, 1, 'Fz', '[ae]l[ıi]', (-1,), (0,)),
      (4, 1, 'Olz', 'm[ea]d[ea]n', (-1,), (2,)),
      (5, 1, 'Fz', 'y[ıiuü]nc[ae]', (-1,), (1, 3)),
      (6, 1, 'Fz', '[ıiuü]nc[ae]', (-1,), (0,)),
      (7, 1, 'Fz', 'y[ıiuü]p', (-1,), (1, 3)),
      (8, 1, 'Fz', '[ıiuü]p', (-1,), (0,)),
      (9, 1, 'Fz', 'y[ae]r[ae]k', (-1,), (1, 3)),
      (10, 1, 'Fz', '[ae]r[ae]k', (-1,), (0,)),
      (11, 1, 'Fz', '[dt][ıiuü]kç[ae]', (-1,), (2, 4)),
      (12, 1, 'Fz', 'c[ae]s[ıi]n[ae]', (-1,), (2,)),
      (13, 1, 'Fz', 'm[ae]ks[ıi]z[ıi]n', (-1,), (2,)),
      (14, 1, 'Fz', '[dt][ıiuü]ğ[ıiuü]nd[ae]', (-1,), (2, 4)),
      (15, 1, 'Ytsz', '[ea]m[ea]d[ea]n', (-1,), (0,)),
      (16, 1, 'Ytsz', 'y[ea]m[ea]d[ea]n', (-1,), (1,)),
      (17, 1, 'Olz', 'm[ae]', (-1, 2, 5, 7, 9, 11, 13, 14, 26), (2, 9)),
      (18, 1, 'Ytsz', 'y[ae]m[ae]', (-1, 2, 5, 7, 9, 11, 13, 14, 26), (1, 3, 9)),
      (19, 1, 'Ytsz', '[ae]m[ae]', (-1, 2, 5, 7, 9, 11, 13, 14, 26), (0, 9)),
      (20, 1, 'Ytsz', 'y[ae]m[ae]z', (-1, 1, 12), (1, 3, 9)),
      (21, 1, 'Ytsz', '[ae]m[ae]z', (-1, 1, 12), (0, 9)),
      (22, 1, 'Olz', 'm[ae]z', (-1, 1, 12), (2,)),
      (23, 1, 'Fz', 'yken', (-1,), (1, 7)),
      (24, 1, 'Fz', '[ae]s[ıi]y[ae]', (-1,), (0,)),
      (25, 1, 'Fz', 'y[ae]s[ıi]y[ae]', (-1,), (1,)),
      (26, 1, 'Olz', 'm[ae]z', (-1, 1, 12), (2, 11))
      )

soru = (10,
        (1, 1, 'EfGçDi', 'yd[ıiuü]', (-1, 4, 6, 9, 11, 12), (1, 3)),
        (2, 1, 'EfGçMiş', 'ym[ıiuü]ş', (-1, 3, 5, 7, 10, 12), (1, 3)),
        (3, 1, 'EfKe1t', '[ıiuü]m', (0,), (0, 6)),
        (4, 1, 'EfKe1t', 'm', (-1,), (0,)),
        (5, 1, 'EfKe2t', 's[ıiuü]n', (-1,), (0, 3, 6)),
        (6, 1, 'EfKe2t', 'n', (-1,), (0,)),
        (7, 1, 'EfKe1ç', '[ıiuü]z', (0,), (0,)),
        (8, 1, 'EfKe1ç', 'y[ıiuü]z', (-1,), (0,)),
        (9, 1, 'EfKe1ç', 'k', (0,), (1,)),
        (10, 1, 'EfKe2ç', 's[ıiuü]n[ıiuü]z', (-1,), (0, 3, 6)),
        (11, 1, 'EfKe2ç', 'n[ıiuü]z', (0,), (1,)),
        (12, 1, 'EfKe3ç', 'l[ae]r', (-1,), (2,)))

SUFFIX_SHORTLIST = {'EfGçDi' : 'Ek Fiil Görülen Geçmiş Zaman / -dili Geçmiş Zaman',
                    'EfGçMiş': 'Ek Fiil Öğrenilen Geçmiş Zaman / -mişli Geçmiş Zaman',
                    'EfGz'   : 'Ek Fiil Geniş Zaman',
                    'EfKŞrt' : 'Ek fiilin şart kipi',
                    'EfKe1t' : 'Ek Fiil 1. Tekil Kişi Eki',
                    'EfKe2t' : 'Ek Fiil 2. Tekil Kişi Eki',
                    'EfKe3t' : 'Ek Fiil 3. Tekil Kişi Eki',
                    'EfKe1ç' : 'Ek Fiil 1. Çoğul Kişi Eki',
                    'EfKe2ç' : 'Ek Fiil 2. Çoğul Kişi Eki',
                    'EfKe3ç' : 'Ek Fiil 3. Çoğul Kişi Eki',
                    'Çe'     : 'Çokluk Eki',
                    'İe1t'   : '1. Tekil Kişi İyelik Eki',
                    'İe2t'   : '2. Tekil Kişi İyelik Eki',
                    'İe3t'   : '3. Tekil Kişi İyelik Eki',
                    'İe1ç'   : '1. Çoğul Kişi İyelik Eki',
                    'İe2ç'   : '2. Çoğul Kişi İyelik Eki',
                    'İe3ç'   : '3. Çoğul Kişi İyelik Eki',
                    'HeBlrt' : 'Belirtme/Yükleme Hal Eki',
                    'HeTyn'  : 'İlgi Hal Eki/Tamlayan Eki',
                    'HeYak'  : 'Yaklaşma Hal Eki',
                    'HeBul'  : 'Bulunma Hal Eki',
                    'HeUzk'  : 'Ayrılma/Uzaklaşma Hal Eki',
                    'HeVas'  : 'Vasıta/Birliktelik Hal Eki',
                    'Ait'    : 'Aitlik Eki',
                    'HeGör'  : 'Eşitlik/HeGörecelilik Eki',
                    'GçDi'   : 'Görülen Geçmiş Zaman / -dili Geçmiş Zaman',
                    'GçMiş'  : 'Öğrenilen Geçmiş Zaman / -mişli Geçmiş Zaman',
                    'Şz'     : 'Şimdiki Zaman',
                    'Gkz'    : 'Gelecek Zaman',
                    'Gz'     : 'Geniş Zaman',
                    'Grlk'   : 'Gereklilik Kipi',
                    'KŞrt'   : 'Dilek-Şart Kipi',
                    'Kİtk'   : 'İstek Kipi',
                    'Ke1t'   : '1. Tekil Kişi Eki',
                    'Ke2t'   : '2. Tekil Kişi Eki',
                    'Ke1ç'   : '1. Çoğul Kişi Eki',
                    'Ke2ç'   : '2. Çoğul Kişi Eki',
                    'Ke3ç'   : '3. Çoğul Kişi Eki',
                    'KEmr'   : 'Emir Kipi',
                    'Olz'    : 'Olumsuzluk Eki',
                    'Ytsz'   : 'Yetersizlik Eki',
                    'BfBil'  : 'Yeterlilik Birleşik Fiil Eki',
                    'BfVer'  : 'Tezlik Birleşik Fiil Eki',
                    'BfGel'  : 'Sürerlik (Süreklilik) Birleşik Fiil Eki',
                    'BfDur'  : 'Sürerlik (Süreklilik) Birleşik Fiil Eki',
                    'BfGör'  : 'Çabukluk/Tezlik Birleşik Fiil Eki',
                    'BfKal'  : 'Sürerlik (Süreklilik) Birleşik Fiil Eki',
                    'BfKoy'  : 'Çabukluk/Tezlik Birleşik Fiil Eki',
                    'BfYaz'  : 'Yaklaşma Birleşik Fiil Eki',
                    'İi'     : 'İsimden İsim Yapım Eki',
                    'İf'     : 'İsimden Fiil Yapım Eki',
                    'Ff'     : 'Fiilden Fiil Yapım Eki',
                    'Fi'     : 'Fiilden İsim Yapım Eki',
                    'Fs'     : 'Fiilden Sıfat Yapım Eki',
                    'Fz'     : 'Fiilden Zarf Yapım Eki',
                    'Ye-Fz'  : 'Fiilden Zarf Yapım Eki',
                    }

SUFFIX_SHORTLIST2 = {'EfGçDi' : 'CV+Past',
                     'EfGçMiş': 'CV+Narr',
                     'EfGz'   : 'CV+Aor',
                     'EfKŞrt' : 'CV+Cond',
                     'EfKe1t' : 'CV+A1sg',
                     'EfKe2t' : 'CV+A2sg',
                     'EfKe3t' : 'CV+A3sg',
                     'EfKe1ç' : 'CV+A1pl',
                     'EfKe2ç' : 'CV+A2pl',
                     'EfKe3ç' : 'CV+A3pl',
                     'Çe'     : 'Much',
                     'İe1t'   : 'P1sg',
                     'İe2t'   : 'P2sg',
                     'İe3t'   : 'P3sg',
                     'İe1ç'   : 'P1pl',
                     'İe2ç'   : 'P2pl',
                     'İe3ç'   : 'P3pl',
                     'HeBlrt' : 'Deting',
                     'HeTyn'  : 'Deted',
                     'HeYak'  : 'Dat',
                     'HeBul'  : 'Loc',
                     'HeUzk'  : 'Abl',
                     'HeVas'  : 'Ins',
                     'Ait'    : 'Rel',
                     'HeGör'  : 'Equ',
                     'GçDi'   : 'Past',
                     'GçMiş'  : 'Narr',
                     'Şz'     : 'Prog1',
                     'Gkz'    : 'Fut',
                     'Gz'     : 'Aor',
                     'Grlk'   : 'Neces',
                     'KŞrt'   : 'Cond',
                     'Kİtk'   : 'Opt',
                     'Ke1t'   : 'A1sg',
                     'Ke2t'   : 'A2sg',
                     'Ke1ç'   : 'A1pl',
                     'Ke2ç'   : 'A2pl',
                     'Ke3ç'   : 'A3pl',
                     'KEmr'   : 'Imp',
                     'Olz'    : 'Neg',
                     'Ytsz'   : 'NotEnough',
                     'BfBil'  : 'Able',
                     'BfVer'  : 'Hastily',
                     'BfGel'  : 'EverSince',
                     'BfDur'  : 'Repeat',
                     'BfGör'  : 'Repeat',
                     'BfKal'  : 'Stay',
                     'BfKoy'  : 'Start',
                     'BfYaz'  : 'Almost',
                     'İi'     : 'NtN',
                     'İf'     : 'NtV',
                     'Ff'     : 'VtV',
                     'Fi'     : 'VtN',
                     'Fs'     : 'VtAdj',
                     'Fz'     : 'VtAdv',
                     'Ye-Fz'  : 'VtAdv',
                     }

st_dict = {1: ice,
           2: fce,
           3: bfe,
           4: ii,
           5: ifi,
           6: ff,
           7: fi,
           8: fs,
           9: fz}

st_str_dict = {'ice': 1,
               'fce': 2,
               'bfe': 3,
               'ii' : 4,
               'ifi': 5,
               'ff' : 6,
               'fi' : 7,
               'fs' : 8,
               'fz' : 9}

verb_tables = {2, 3, 6, 7, 8, 9}

terminal_devoicing = {'ğ': 'k',
                      'd': 't'}

der_type = {'İi', 'İf', 'Ff', 'Fi', 'Fs', 'Fz'}

daf_type = {3: 'fiil',
            6: 'fiil',
            7: 'isim',
            8: 'isim,sıfat',
            9: 'isim,zarf',
            5: 'fiil',
            4: 'isim'}

tti = {'isim'   : 'Noun',
       'fiil'   : 'Verb',
       'özel'   : 'Prop',
       'sıfat'  : 'Adj',
       'zamir'  : 'Pron',
       'edat'   : 'Part',
       'zarf'   : 'Adv',
       'ünlem'  : 'Interj',
       'bağlaç' : 'Conj',
       'yansıma': 'Onom'}
