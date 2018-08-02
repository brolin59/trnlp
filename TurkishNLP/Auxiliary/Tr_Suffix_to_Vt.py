# -*- coding: utf-8 -*-
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
import itertools
import re
import sqlite3

# Bu kısım yardımcı yazılım olarak kullanılmaktadır. Tüm ekleri tabloda verilen kurallar çerçevesinde
# permutasyon yapılarak olası tüm ek dizilimlerini veritabanına yazar.
# Yapım ekleri kısmı devre dışı bırakıldı çünkü nihai amacım cümle analizi yapabilmek olduğundan
# kelimenin gövdesine ulaşmak şu anda benim için yeterli.

# Ek listeleri. Yeni ek listesi eklenir ise ek_tipleri ve ek_max_per sözlüğüne ekleme yapılmalıdır.
# Ek tablolarında;
# 0. sütun : Ekin numarası
# 1. sütun : Ekin grup numarası (Şu anda kullanılmıyor.)
# 2. sütun : Ekin adı/tanımı (Herhangi bir veri olarak kullanılmıyor. Sadece anlaşılırlık daha iyi olsun diye bu sütun var.)
# 3. sütun : Ekin tanımı
# 4. sütun : Ekin regex kodu
# 5. sütun : Bu ekten önce gelebilecek eklerin numaraları. -1 ise kökü/gövdeyi ifade eder.
# 6. sütun : Ekten önce gelebilecek harfin türü. 0 ise sessiz harf, 1 ise sesli harf, 2 ise her ikisi de gelebilir. (Şu anda kullanılmıyor.)
isim_ek_fiil_ekleri = [['1', '0', 'XDU', 'Hikaye', '(y[dt][ıiuü])', (-1,), 1],
                       ['2', '0', 'DU', 'Hikaye', '([dt][ıiuü])', (-1,), 0],
                       ['3', '0', 'XmUş', 'Rivayet', '(ym[ıiuü]ş)', (-1,), 1],
                       ['4', '0', 'mUş', 'Rivayet', '(m[ıiuü]ş)', (-1,), 0],
                       ['5', '0', 'XsE', 'Şart', '(ys[ea])', (-1,), 1],
                       ['6', '0', 'sE', 'Şart', '(s[ea])', (-1,), 0],
                       ['7', '1', 'XUm', '1. tekil kişi', '(y[ıiuü]m)', (-1,), 1],
                       ['8', '1', 'Um', '1. tekil kişi', '([ıiuü]m)', (-1, 3, 4), 0],
                       ['9', '1', 'm', '1. tekil kişi', '(m)', (1, 2, 5, 6), 1],
                       ['10', '1', 'sUn', '2. tekil kişi', '(s[ıiuü]n)', (-1, 3, 4), 2],
                       ['11', '1', 'n', '2. tekil kişi', '(n)', (1, 2, 5, 6), 1],
                       ['12', '1', 'DUr', 'Bildirme eki', '([dt][ıiuü]r)', (-1,), 2],
                       ['13', '1', 'XUz', '1. çoğul kişi', '([y][ıiuü]z)', (-1,), 1],
                       ['14', '1', 'Uz', '1. çoğul kişi', '([ıiuü]z)', (-1, 3, 4), 0],
                       ['15', '1', 'k', '1. çoğul kişi', '(k)', (1, 2, 5, 6), 1],
                       ['16', '1', 'sUnUz', '2. çoğul kişi', '(s[ıiuü]n[ıiuü]z)', (-1, 3, 4), 2],
                       ['17', '1', 'nUz', '2. çoğul kişi', '(n[ıiuü]z)', (1, 2, 5, 6), 1],
                       ['18', '1', 'lEr', '3. çoğul kişi', '(l[ae]r)', (-1, 1, 2, 3, 4, 5, 6), 2],
                       ['19', '1', 'lErDUr', '3. çoğul kişi', '(l[ae]r[dt][ıiuü]r)', (-1,), 2],
                       ['20', '1', 'DUrlEr', '3. çoğul kişi', '([dt][ıiuü]rl[ae]r)', (-1,), 2]]

isim_cekim_ekleri = [['1', '0', 'lEr', 'Çokluk eki', '(l[ae]r)', (-1, 3, 7, 26), 2],
                     ['2', '1', 'Um', '1. tekil kişi', '([ıiuü]m)', (-1, 1), 0],
                     ['3', '1', 'm', '1. tekil kişi', '(m)', (-1,), 1],
                     ['4', '1', 'UmUz', '1. çoğul kişi', '([ıiuü]m[ıiuü]z)', (-1, 1), 0],
                     ['5', '1', 'mUz', '1. çoğul kişi', '(m[ıiuü]z)', (-1,), 1],
                     ['6', '1', 'Un', '2. tekil kişi', '([ıiuü]n)', (-1, 1), 0],
                     ['7', '1', 'n', '2. tekil kişi', '(n)', (-1,), 1],
                     ['8', '1', 'UnUz', '2. çoğul kişi', '([ıiuü]n[ıiuü]z)', (-1, 1), 0],
                     ['9', '1', 'nUz', '2. çoğul kişi', '(n[ıiuü]z)', (-1,), 1],
                     ['10', '1', 'XU', '3. tekil kişi', '([ys][ıiuü])', (-1,), 1],
                     ['11', '1', 'U', '3. tekil kişi', '([ıiuü])', (-1, 1), 0],
                     ['12', '1', 'lErI', '3. çoğul kişi', '(l[ae]r[ıi])', (-1,), 2],
                     ['13', '2', 'XU', '-i hali', '([ys][ıiuü])', (-1,), 1],
                     ['14', '2', 'U', '-i hali', '([ıiuü])', (-1, 1, 2, 3, 4, 5, 6, 7, 8, 9), 0],
                     ['15', '2', 'nU', '-i hali', '(n[ıiuü])', (10, 11, 12), 1],
                     ['16', '4', 'XUn', 'Tamlama eki', '([yn][ıiuü]n)', (-1, 10, 11, 12, 13, 14, 15), 1],
                     ['17', '4', 'Un', 'Tamlama eki', '([ıiuü]n)', (-1, 1, 2, 3, 4, 5, 7, 8, 9, 18), 0],
                     ['18', '4', 'XE', '-e hali', '([yn][ae])', (-1, 10, 11, 12), 1],
                     ['19', '4', 'E', '-e hali', '([ae])', (-1, 1, 2, 3, 4, 5, 6, 7, 8, 9), 0],
                     ['20', '4', 'DE', 'Bulunma hal eki', '([dt][ae])', (-1, 1, 2, 3, 4, 5, 6, 7, 8, 9), 0],
                     ['21', '4', 'XDE', 'Bulunma hal eki', '([n][dt][ae])', (10, 11, 12, 26), 1],
                     ['22', '4', 'DEn', 'Ayrılma/Uzaklaşma hal eki', '([dt][ae]n)', (-1, 1, 2, 3, 4, 5, 6, 7, 8, 9), 0],
                     ['23', '4', 'XDEn', 'Ayrılma/Uzaklaşma hal eki', '([n][dt][ae]n)', (10, 11, 12, 26), 1],
                     ['24', '4', 'XlE', 'Vasıta/Birliktelik hal eki', '([y]l[ae])', (-1, 10, 11, 12), 1],
                     ['25', '4', 'lE', 'Vasıta/Birliktelik hal eki', '(l[ae])', (-1, 1, 2, 3, 4, 5, 6, 7, 8, 9), 0],
                     ['26', '3', 'ki', 'Aitlik eki', '(ki)', (-1, 16, 17, 20, 21), 2],
                     ['27', '4', 'XCE', 'Birliktelik/Görecelilik eki', '([n][cç][ae])', (-1,), 1],
                     ['28', '4', 'CE', 'Birliktelik/Görecelilik eki', '([cç][ae])', (-1, 1), 2]]

x_fiil_ekleri = [['0', '0', 'mE', 'İsim Fiil Eki', '(m[ea])', (-1, 4, 29, 30), 2],
                 ['1', '0', 'Xış', 'İsim Fiil Eki', '([yn][ıiuü]ş)', (-1, 4, 29, 30), 2],
                 ['2', '0', 'ış', 'İsim Fiil Eki', '([ıiuü]ş)', (-1,), 2],
                 ['3', '0', 'mEk', 'İsim Fiil Eki', '(m[ea]k)', (-1, 4, 29, 30), 2],
                 ['4', '1', 'mE', 'Olumsuzluk Eki', '(m[ea])', (-1,), 2],
                 ['5', '0', 'XEn', 'Sıfat Fiil Eki', '([yn][ae]n)', (-1, 4, 29, 30), 2],
                 ['6', '0', 'En', 'Sıfat Fiil Eki', '([ae]n)', (-1,), 2],
                 ['7', '1', 'XEsI', 'Sıfat Fiil Eki', '([yn][ae]s[ıi])', (-1, 4, 29, 30), 2],
                 ['8', '1', 'EsI', 'Sıfat Fiil Eki', '([ae]s[ıi])', (-1,), 2],
                 ['9', '2', 'mEz', 'Sıfat Fiil Eki', '(m[ea]z)', (-1, 4, 29, 30), 2],
                 ['10', '3', 'Er', 'Sıfat Fiil Eki', '([ea]r)', (-1,), 2],
                 ['11', '4', 'dUk', 'Sıfat Fiil Eki', '([dt][ıiuü][kğ])', (-1, 4, 29, 30), 2],
                 ['12', '5', 'XEcEk', 'Sıfat Fiil Eki', '([yn][ae]c[ae][kğ])', (-1, 4, 29, 30), 2],
                 ['13', '5', 'EcEk', 'Sıfat Fiil Eki', '([ae]c[ae][kğ])', (-1,), 2],
                 ['14', '6', 'mUş', 'Sıfat Fiil Eki', '(m[ıiuü]ş)', (-1, 4, 29, 30), 2],
                 ['15', '0', 'ken', 'Zarf Fiil Eki', '(ken)', (-1,), 2],
                 ['16', '1', 'XElI', 'Zarf Fiil Eki', '([yn][ae]l[ıi])', (-1, 4, 29, 30), 2],
                 ['17', '1', 'ElI', 'Zarf Fiil Eki', '([ae]l[ıi])', (-1,), 2],
                 ['18', '2', 'mEdEn', 'Zarf Fiil Eki', '(m[ea]d[ea]n)', (-1,), 2],
                 ['19', '3', 'XUncE', 'Zarf Fiil Eki', '([yn][ıiuü]nc[ae])', (-1, 4, 29, 30), 2],
                 ['20', '3', 'UncE', 'Zarf Fiil Eki', '([ıiuü]nc[ae])', (-1,), 2],
                 ['21', '4', 'XUp', 'Zarf Fiil Eki', '([yn][ıiuü]p)', (-1, 4, 29, 30), 2],
                 ['22', '4', 'Up', 'Zarf Fiil Eki', '([ıiuü]p)', (-1,), 2],
                 ['23', '5', 'XErEk', 'Zarf Fiil Eki', '([yn][ae]r[ae]k)', (-1, 4, 29, 30), 2],
                 ['24', '5', 'ErEk', 'Zarf Fiil Eki', '([ae]r[ae]k)', (-1,), 2],
                 ['25', '6', 'DUkçE', 'Zarf Fiil Eki', '([dt][ıiuü]kç[ae])', (-1, 4, 29, 30), 2],
                 ['26', '7', 'cEsInE', 'Zarf Fiil Eki', '(c[ae]s[ıi]n[ae])', (-1,), 2],
                 ['27', '8', 'mEksIzIn', 'Zarf Fiil Eki', '(m[ae]ks[ıi]z[ıi]n)', (-1,), 2],
                 ['28', '9', 'dUğUndE', 'Zarf Fiil Eki', '(d[ıiuü]ğ[ıiuü]nd[ae])', (-1, 4, 29, 30), 2],
                 ['29', '1', 'EmE', 'Yetersizlik Eki', '([ea]m[ea])', (-1,), 2],
                 ['30', '1', 'XEmE', 'Yetersizlik Eki', '(y[ea]m[ea])', (-1,), 2]]

fiil_cekim_ekleri = [['1', '0', 'DU', 'Bilinen Geçmiş Zaman', '([dt][ıiuü])', (-1, 21, 22), 2],
                     ['2', '0', 'mUş', 'Öğrenilen Geçmiş Zaman', '(m[ıiuü]ş)', (-1, 21, 22), 2],
                     ['3', '0', '(U)yor', 'Şimdiki Zaman', '([ıiuü]yor)', (-1,), 2],
                     ['4', '0', 'yor', 'Şimdiki Zaman', '(yor)', (-1, 20), 2],
                     ['5', '0', 'XEcEK', 'Gelecek Zaman', '(y[ae]c[ae][kğ])', (-1, 21), 2],
                     ['6', '0', 'EcEK', 'Gelecek Zaman', '([ae]c[ae][kğ])', (-1,), 2],
                     ['7', '0', 'Ar', 'Geniş Zaman', '([aeıiuü]r)', (-1,), 2],
                     ['8', '0', 'r', 'Geniş Zaman', '(r)', (-1,), 2],
                     ['9', '1', 'mElI', 'Gereklilik Kipi', '(m[ae]l[ıi])', (-1, 21), 2],
                     ['10', '1', 'XsE', 'Dilek Şart Kipi', '(ys[ae])', (-1,), 2],
                     ['11', '1', 'sE', 'Dilek Şart Kipi', '(s[ae])', (-1, 21, 22), 2],
                     ['12', '1', 'XE', 'İstek Kipi', '(y[ae])', (-1, 21), 2],
                     ['13', '1', 'E', 'İstek Kipi', '([ae])', (-1,), 2],
                     ['14', '1', 'sUn', 'Emir Kipi', '(s[ıiuü]n)', (-1, 21), 2],
                     ['15', '1', 'XUnUz', 'Emir Kipi', '([yns][ıiuü]n[ıiuü]z)', (-1, 21), 2],
                     ['16', '1', 'UnUz', 'Emir Kipi', '([ıiuü]n[ıiuü]z)', (-1, 15), 2],
                     ['17', '1', 'XUn', 'Emir Kipi', '(y[ıiuü]n)', (-1, 21), 2],
                     ['18', '1', 'Un', 'Emir Kipi', '([ıiuü]n)', (-1, 15), 2],
                     ['19', '1', 'sUnlEr', 'Emir Kipi', '(s[ıiuü]nl[ae]r)', (-1, 21), 2],
                     ['20', '3', 'mU', 'Olumsuzluk Eki', '(m[ıiuü])', (-1,), 2],
                     ['21', '3', 'mE', 'Olumsuzluk Eki', '(m[ea])', (-1,), 2],
                     ['22', '3', 'mEz', 'Olumsuzluk Eki', '(m[ea]z)', (-1,), 2],
                     ['23', '4', 'XUm', '1. tekil kişi', '(y[ıiuü]m)', (9, 12, 13, 21), 2],
                     ['24', '4', 'Um', '1. tekil kişi', '([ıiuü]m)', (2, 3, 4, 5, 6, 7, 8), 2],
                     ['26', '4', 'm', '1. tekil kişi', '(m)', (1, 10, 11, 22), 2],
                     ['27', '4', 'sUn', '2. tekil kişi', '(s[ıiuü]n)', (2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 21, 22), 2],
                     ['28', '4', 'n', '2. tekil kişi', '(n)', (1, 10, 11), 2],
                     ['29', '4', 'Uz', '1. çoğul kişi', '([ıiuü]z)', (2, 3, 4, 5, 6, 7, 8), 2],
                     ['30', '4', 'XUz', '1. çoğul kişi', '(y[ıiuü]z)', (9, 21), 2],
                     ['31', '4', 'lIm', '1. çoğul kişi', '(l[ıi]m)', (12, 13), 2],
                     ['32', '4', 'k', '1. çoğul kişi', '(k)', (1, 10, 11), 2],
                     ['33', '4', 'sUnUz', '2. çoğul kişi', '(s[ıiuü]n[ıiuü]z)', (2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 22),
                      2],
                     ['34', '4', 'nUz', '2. çoğul kişi', '(n[ıiuü]z)', (1, 10, 11), 2],
                     ['35', '4', 'lEr', '3. çoğul kişi', '(l[ae]r)', (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 22),
                      2]]

fiil_ek_fiil_ekleri = [['1', '0', 'XDU', 'Hikaye', '(y[dt][ıiuü])', (-1,), 1],
                       ['2', '0', 'DU', 'Hikaye', '([dt][ıiuü])', (-1,), 0],
                       ['3', '0', 'XmUş', 'Rivayet', '(ym[ıiuü]ş)', (-1,), 1],
                       ['4', '0', 'mUş', 'Rivayet', '(m[ıiuü]ş)', (-1,), 0],
                       ['5', '0', 'XsE', 'Şart', '(ys[ea])', (-1,), 1],
                       ['6', '0', 'sE', 'Şart', '(s[ea])', (-1,), 0],
                       ['7', '1', 'Um', '1. tekil kişi', '([ıiuü]m)', (3, 4), 0],
                       ['8', '1', 'm', '1. tekil kişi', '(m)', (1, 2, 5, 6), 1],
                       ['9', '1', 'sUn', '2. tekil kişi', '(s[ıiuü]n)', (3, 4), 2],
                       ['10', '1', 'n', '2. tekil kişi', '(n)', (1, 2, 5, 6), 1],
                       ['11', '1', 'DUr', 'Bildirme eki', '([dt][ıiuü]r)', (-1, 16), 2],
                       ['12', '1', 'Uz', '1. çoğul kişi', '([ıiuü]z)', (3, 4), 0],
                       ['13', '1', 'k', '1. çoğul kişi', '(k)', (1, 2, 5, 6), 1],
                       ['14', '1', 'sUnUz', '2. çoğul kişi', '(s[ıiuü]n[ıiuü]z)', (3, 4), 2],
                       ['15', '1', 'nUz', '2. çoğul kişi', '(n[ıiuü]z)', (1, 2, 5, 6), 1],
                       ['16', '1', 'lEr', '3. çoğul kişi', '(l[ae]r)', (1, 2, 3, 4, 5, 6, 11), 2]]

yardimci_fiiller = [['1', '3', 'eyle', '1. tekil kişi', '(eyle)', (-1,), 2],
                    ['2', '4', 'eD', '2. tekil kişi', '(e[dt])', (-1,), 2],
                    ['3', '3', 'ol', '3. tekil kişi', '(ol)', (-1,), 2]]

birlesik_fiil_ekleri = [['1', '4', 'yEbil', 'yeterlik bileşik eylem kipi', '([y][ae]bil)', (-1, 3, 4, 7), 2],
                        ['2', '4', 'Ebil', 'yeterlik bileşik eylem kipi', '([ae]bil)', (-1,), 2],
                        ['3', '4', 'yEmE', 'olumsuzluk/yetersizlik', '([y][ae]m[ae])', (-1,), 2],
                        ['4', '4', 'EmE', 'olumsuzluk/yetersizlik', '([ae]m[ae])', (-1,), 2],
                        ['5', '4', 'yEmEz', 'olumsuzluk/yetersizlik', '([y][ae]m[ae]z)', (-1,), 2],
                        ['6', '4', 'EmEz', 'olumsuzluk/yetersizlik', '([ae]m[ae]z)', (-1,), 2],
                        ['7', '4', 'mE', 'olumsuzluk', '(m[ae])', (-1,), 2],
                        ['8', '4', 'yUver', 'tezlik bileşik eylem kipi', '([y][ıiuü]ver)', (-1, 7), 2],
                        ['9', '4', 'Uver', 'tezlik bileşik eylem kipi', '([ıiuü]ver)', (-1,), 2],
                        ['10', '4', 'yEgel', 'tezlik bileşik eylem kipi', '([y][ae]gel)', (-1, 7), 2],
                        ['11', '4', 'Egel', 'tezlik bileşik eylem kipi', '([ae]gel)', (-1,), 2],
                        ['12', '4', 'yEdur', 'sürerlik bileşik eylem kipi', '([y][ae]dur)', (-1,), 2],
                        ['13', '4', 'Edur', 'sürerlik bileşik eylem kipi', '([ae]dur)', (-1,), 2],
                        ['14', '4', 'yEgör', 'sürerlik bileşik eylem kipi', '([y][ae]gör)', (-1,), 2],
                        ['15', '4', 'Egör', 'sürerlik bileşik eylem kipi', '([ae]gör)', (-1,), 2],
                        ['16', '4', 'yEkal', 'sürerlik bileşik eylem kipi', '([y][ae]kal)', (-1,), 2],
                        ['17', '4', 'Ekal', 'sürerlik bileşik eylem kipi', '([ae]kal)', (-1,), 2],
                        ['18', '4', 'yEkoy', 'sürerlik bileşik eylem kipi', '([y][ae]koy)', (-1,), 2],
                        ['19', '4', 'Ekoy', 'sürerlik bileşik eylem kipi', '([ae]koy)', (-1,), 2],
                        ['20', '4', 'yEyaz', 'yaklaşma bileşik eylem kipi', '([y][ae]yaz)', (-1,), 2],
                        ['21', '4', 'Eyaz', 'yaklaşma bileşik eylem kipi', '([ae]yaz)', (-1,), 2]]

fiil_catisi = [['1', '0', 'Un', 'edilgen/dönüşlü', '([ıiuü]n)', (-1,), 0],
               ['2', '0', 'n', 'edilgen/dönüşlü', '(n)', (-1,), 1],
               ['3', '0', 'Ul', 'edilgen/dönüşlü', '([ıiuü]l)', (-1,), 0],
               ['4', '0', 'l', 'edilgen/dönüşlü', '(l)', (-1,), 1],
               ['5', '0', 'Uş', 'işteş', '([ıiuü]ş)', (-1,), 0],
               ['6', '0', 'ş', 'işteş', '(ş)', (-1,), 1],
               ['7', '0', 'r', 'ettirgen/oldurgan', '(r)', (-1,), 1],
               ['8', '0', 'Er', 'ettirgen/oldurgan', '([ae]r)', (-1,), 0],
               ['9', '0', 't', 'ettirgen/oldurgan', '(t)', (-1,), 2],
               ['10', '0', 'DUr', 'ettirgen/oldurgan', '([dt][ıiuü]r)', (-1,), 2]]

# yapim_ekleri = [['1', '0', 'lU', 'yapım eki', '(l[ıiuü])', (-1,), 2],
#                 ['2', '0', 'lEş', 'yapım eki', '(l[ae]ş)', (-1, 1), 2],
#                 ['3', '0', 'gil', 'yapım eki', '(gil)', (-1,), 2],
#                 ['4', '0', 'giller', 'yapım eki', '(giller)', (-1,), 2],
#                 ['5', '0', 'AcUk', 'yapım eki', '([aeıiuü]?)(c[ıiuü]k)', (-1,), 2]]

ek_tipleri = ['isim_ek_fiil_ekleri', 'isim_cekim_ekleri', 'x_fiil_ekleri', 'fiil_cekim_ekleri', 'fiil_ek_fiil_ekleri',
              'yardimci_fiiller', 'birlesik_fiil_ekleri', 'fiil_catisi']
# ----------------------------- Ek Tipleri Sonu --------------------------------------------------------------- #

# Her ekin max n'li prmutasyon sayısını ifade eder. Örneğin 2 olduğunda max 2'li permutasyon sayısıdır. (5|1)(5|2)
# ek_max_per sözlüğünde belirtilen sayıda permutasyonlar oluşturulur. Ek listelerindeki kurallara uymayanlar liste
# dışı bırakılır ve veritabanına yazılır.
if __name__ == '__main__':
    ek_max_per = {'isim_ek_fiil_ekleri': 2,
                  'isim_cekim_ekleri': 6,
                  'x_fiil_ekleri': 2,
                  'fiil_cekim_ekleri': 2,
                  'fiil_ek_fiil_ekleri': 2,
                  'yardimci_fiiller': 1,
                  'birlesik_fiil_ekleri': 2,
                  'fiil_catisi': 1}

    clear_data = re.compile('({.*?})')

    for ek_tipi in ek_tipleri:
        print(ek_tipi)
        permutation_list = []
        ek_no_reg_data = []
        ekler = eval(ek_tipi)
        print(ek_tipi, 'listesi oluşturuluyor')
        for element in ekler:
            onceki_nolar = ','.join([str(i) for i in element[5]])
            ek_data = '<' + element[0] + '>' + element[4] + '[[' + element[3] + ']]' + '{' + onceki_nolar + '}'
            ek_no_reg_data.append(ek_data)
        # Tekrarsız permutasyonu alınır
        print(ek_tipi, 'listesi permutasyonu hesaplanıyor')
        for i in range(1, ek_max_per[ek_tipi] + 1):
            print(i, 'uzunluğundaki ekler hesaplanıyor')
            if i == 1:
                for data in ek_no_reg_data:
                    regex_end_no = re.findall('{(.*?)}', data)
                    regex_end_no = regex_end_no[0].split(',')
                    if '-1' in regex_end_no:
                        regex_data = clear_data.sub('', data)
                        permutation_list.append(regex_data)
            else:
                permutation_adds = itertools.permutations(ek_no_reg_data, i)
                for data in permutation_adds:
                    for no, noreic in enumerate(data):
                        kontrol = True
                        try:
                            data[no + 1]
                        except:
                            kontrol = False

                        if kontrol is not False:
                            bulunacak_no = re.match('<(\d+)>', noreic).group(1)
                            aranacak_seri = re.findall('{(.*?)}', data[no + 1])[0]
                            aranacak_seri = aranacak_seri.split(',')
                            if bulunacak_no not in aranacak_seri:
                                break
                        else:
                            _data = ''.join(data)
                            regex_data = clear_data.sub('', _data)
                            permutation_list.append(regex_data)

        print('veriler veri tabanına yazılıyor')
        with sqlite3.connect('../Data/tr_NLP.sqlite') as vt:
            im = vt.cursor()
            im.execute("DROP TABLE IF EXISTS {}".format(ek_tipi))
            im.execute("CREATE TABLE IF NOT EXISTS {} (regex_code)".format(ek_tipi))
            for veri in permutation_list:
                im.execute("INSERT INTO {} VALUES (?)".format(ek_tipi), (veri,))
            vt.commit()
