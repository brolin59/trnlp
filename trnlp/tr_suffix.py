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

# Ek listeleri. Yeni ek listesi eklenir ise ek_tipleri ve ek_max_per sözlüğüne ekleme yapılmalıdır.
# Ek tablolarında;
# 0. sütun : Ekin numarası
# 1. sütun : Ekin grup numarası (Şu anda kullanılmıyor.)
# 2. sütun : Ekin adı/tanımı (Herhangi bir veri olarak kullanılmıyor. Sadece anlaşılırlık daha iyi olsun diye bu
# sütun var.)
# 3. sütun : Ekin tanımı
# 4. sütun : Ekin regex kodu
# 5. sütun : Bu ekten önce gelebilecek eklerin numaraları. -1 ise kökü/gövdeyi ifade eder.
# 6. sütun : Ekten önce gelebilecek harfin türü. 0 ise sessiz harf, 1 ise sesli harf, 2 ise her ikisi de gelebilir.
# (Şu anda kullanılmıyor.)
isim_ek_fiil_ekleri = [['1', '0', 'XDU', 'Hikaye', '(y[dt][ıiuü])', (-1, 9, 11, 15, 17, 18), 1],
                       ['2', '0', 'DU', 'Hikaye', '([dt][ıiuü])', (-1, 9, 11, 15, 17, 18), 0],
                       ['3', '0', 'XmUş', 'Rivayet', '(ym[ıiuü]ş)', (-1, 8, 10, 12, 14, 16, 18, 19, 20), 1],
                       ['4', '0', 'mUş', 'Rivayet', '(m[ıiuü]ş)', (-1, 8, 10, 12, 14, 16, 18, 19, 20), 0],
                       ['5', '0', 'XsE', 'Şart', '(ys[ea])', (-1, 9, 11, 15, 17, 18), 1],
                       ['6', '0', 'sE', 'Şart', '(s[ea])', (-1, 9, 11, 15, 17, 18), 0],
                       ['7', '1', 'XUm', '1. Tekil Kişi', '(y[ıiuü]m)', (-1,), 1],
                       ['8', '1', 'Um', '1. Tekil Kişi', '([ıiuü]m)', (-1,), 0],
                       ['9', '1', 'm', '1. Tekil Kişi', '(m)', (0,), 1],
                       ['10', '1', 'sUn', '2. Tekil Kişi', '(s[ıiuü]n)', (-1,), 2],
                       ['11', '1', 'n', '2. Tekil Kişi', '(n)', (0,), 1],
                       ['12', '1', 'DUr', 'Bildirme eki', '([dt][ıiuü]r)', (-1,), 2],
                       ['13', '1', 'XUz', '1. Çoğul Kişi', '([y][ıiuü]z)', (-1,), 1],
                       ['14', '1', 'Uz', '1. Çoğul Kişi', '([ıiuü]z)', (-1,), 0],
                       ['15', '1', 'k', '1. Çoğul Kişi', '(k)', (0,), 1],
                       ['16', '1', 'sUnUz', '2. Çoğul Kişi', '(s[ıiuü]n[ıiuü]z)', (-1,), 2],
                       ['17', '1', 'nUz', '2. Çoğul Kişi', '(n[ıiuü]z)', (0,), 1],
                       ['18', '1', 'lEr', '3. Çoğul Kişi', '(l[ae]r)', (0,), 2],
                       ['19', '1', 'lErDIr', '3. Çoğul Kişi', '(l[ae]r[dt][ıi]r)', (-1,), 2],
                       ['20', '1', 'DUrlEr', '3. Çoğul Kişi', '([dt][ıiuü]rl[ae]r)', (-1,), 2]]

isim_cekim_ekleri = [['1', '0', 'lEr', 'Çokluk Eki', '(l[ae]r)', (-1, 2, 4, 6, 8, 11, 14, 17, 20, 21, 23, 26, 28), 2],
                     ['2', '1', 'Um', '1. Tekil Kişi İyelik Eki', '([ıiuü]m)', (-1, 14, 17, 20, 21, 23, 26, 28), 0],
                     ['3', '1', 'm', '1. Tekil Kişi İyelik Eki', '(m)', (-1, 14, 17, 20, 21, 23, 26, 28), 1],
                     ['4', '1', 'UmUz', '1. Çoğul Kişi İyelik Eki', '([ıiuü]m[ıiuü]z)',
                      (-1, 14, 17, 20, 21, 23, 26, 28), 0],
                     ['5', '1', 'mUz', '1. Çoğul Kişi İyelik Eki', '(m[ıiuü]z)', (-1, 14, 17, 20, 21, 23, 26, 28), 1],
                     ['6', '1', 'Un', '2. Tekil Kişi İyelik Eki', '([ıiuü]n)', (-1, 14, 17, 20, 21, 23, 26, 28), 0],
                     ['7', '1', 'n', '2. Tekil Kişi İyelik Eki', '(n)', (-1, 14, 17, 20, 21, 23, 26, 28), 1],
                     ['8', '1', 'UnUz', '2. Çoğul Kişi İyelik Eki', '([ıiuü]n[ıiuü]z)',
                      (-1, 14, 17, 20, 21, 23, 26, 28), 0],
                     ['9', '1', 'nUz', '2. Çoğul Kişi İyelik Eki', '(n[ıiuü]z)', (-1, 14, 17, 20, 21, 23, 26, 28), 1],
                     ['10', '1', 'XU', '3. Tekil Kişi İyelik Eki', '(s[ıiuü])', (-1, 15, 16, 18, 22, 24, 25, 29), 1],
                     ['11', '1', 'U', '3. Tekil Kişi İyelik Eki', '([ıiuü])', (-1, 15, 16, 18, 22, 24, 25, 29), 0],
                     ['12', '1', 'lErI', '3. Çoğul Kişi İyelik Eki', '(l[ae]r[ıi])', (-1, 15, 16, 18, 22, 24, 25, 29),
                      2],
                     ['13', '2', 'XU', 'Belirtme/Yükleme Hal Eki', '(y[ıiuü])', (-1,), 1],
                     ['14', '2', 'U', 'Belirtme/Yükleme Hal Eki', '([ıiuü])', (-1,), 0],
                     ['15', '2', 'nU', 'Belirtme/Yükleme Hal Eki', '(n[ıiuü])', (0,), 1],
                     ['16', '2', 'XUn', 'İlgi Hal Eki/Tamlayan Eki', '(n[ıiuü]n)', (-1,), 1],
                     ['17', '2', 'Un', 'İlgi Hal Eki/Tamlayan Eki', '([ıiuü]n)', (-1,), 0],
                     ['18', '2', 'XE', 'Yaklaşma Hal Eki', '(n[ae])', (0,), 1],
                     ['19', '2', 'XE', 'Yaklaşma Hal Eki', '(y[ae])', (-1,), 1],
                     ['20', '2', 'E', 'Yaklaşma Hal Eki', '([ae])', (-1,), 0],
                     ['21', '2', 'DE', 'Bulunma Hal Eki', '([dt][ae])', (-1, 27), 2],
                     ['22', '2', 'XDE', 'Bulunma Hal Eki', '(n[dt][ae])', (27,), 1],
                     ['23', '2', 'DEn', 'Ayrılma/Uzaklaşma Hal Eki', '([dt][ae]n)', (-1,), 2],
                     ['24', '2', 'XDEn', 'Ayrılma/Uzaklaşma Hal Eki', '(n[dt][ae]n)', (0,), 1],
                     ['25', '2', 'XlE', 'Vasıta/Birliktelik Hal Eki', '(yl[ae])', (-1,), 1],
                     ['26', '2', 'lE', 'Vasıta/Birliktelik Hal Eki', '(l[ae])', (-1,), 0],
                     ['27', '3', 'ki', 'Aitlik Eki', '(ki)', (-1, 30, 15, 16, 18, 22, 24), 2],
                     ['28', '2', 'CE', 'Eşitlik/Görecelilik Eki', '([cç][ae])', (-1,), 2],
                     ['29', '2', 'XCE', 'Eşitlik/Görecelilik Eki', '(n[cç][ae])', (0,), 2],
                     ['30', '4', 'lEr', 'Çokluk Eki', '(l[ae]r)', (14, 17, 20, 21, 23, 26, 28), 1]]

x_fiil_ekleri = [
    ['1', '0', 'mE', 'İsim Fiil Eki', '(m[ea])', (-1, 2, 4, 6, 8, 10, 12, 13, 15, 17, 20, 22, 24, 26, 29), 2],
    ['2', '0', 'Xış', 'İsim Fiil Eki', '([yn][ıiuü]ş)', (-1,), 1],
    ['3', '0', 'ış', 'İsim Fiil Eki', '([ıiuü]ş)', (-1,), 2],
    ['4', '0', 'mEk', 'İsim Fiil Eki', '(m[ea]k)', (-1,), 2],
    ['5', '1', 'mE', 'Olumsuzluk Eki', '(m[ea])', (-1,), 2],
    ['6', '0', 'XEn', 'Sıfat Fiil Eki', '([yn][ae]n)', (-1,), 1],
    ['7', '0', 'En', 'Sıfat Fiil Eki', '([ae]n)', (-1,), 0],
    ['8', '1', 'XEsI', 'Sıfat Fiil Eki', '([yn][ae]s[ıi])', (-1,), 1],
    ['9', '1', 'EsI', 'Sıfat Fiil Eki', '([ae]s[ıi])', (-1,), 0],
    ['10', '2', 'mEz', 'Sıfat Fiil Eki', '(m[ea]z)', (-1,), 2],
    ['11', '3', 'Er', 'Sıfat Fiil Eki', '([ea]r)', (-1,), 2],
    ['12', '4', 'dUk', 'Sıfat Fiil Eki', '([dt][ıiuü][kğ])', (-1,), 2],
    ['13', '5', 'XEcEk', 'Sıfat Fiil Eki', '([yn][ae]c[ae][kğ])', (-1,), 1],
    ['14', '5', 'EcEk', 'Sıfat Fiil Eki', '([ae]c[ae][kğ])', (-1,), 0],
    ['15', '6', 'mUş', 'Sıfat Fiil Eki', '(m[ıiuü]ş)', (-1,), 2],
    ['16', '0', 'ken', 'Zarf Fiil Eki', '(ken)', (-1,), 2],
    ['17', '1', 'XElI', 'Zarf Fiil Eki', '([yn][ae]l[ıi])', (-1,), 1],
    ['18', '1', 'ElI', 'Zarf Fiil Eki', '([ae]l[ıi])', (-1,), 0],
    ['19', '2', 'mEdEn', 'Zarf Fiil Eki', '(m[ea]d[ea]n)', (-1,), 2],
    ['20', '3', 'XUncE', 'Zarf Fiil Eki', '([yn][ıiuü]nc[ae])', (-1,), 1],
    ['21', '3', 'UncE', 'Zarf Fiil Eki', '([ıiuü]nc[ae])', (-1,), 0],
    ['22', '4', 'XUp', 'Zarf Fiil Eki', '([yn][ıiuü]p)', (-1,), 1],
    ['23', '4', 'Up', 'Zarf Fiil Eki', '([ıiuü]p)', (-1,), 0],
    ['24', '5', 'XErEk', 'Zarf Fiil Eki', '([yn][ae]r[ae]k)', (-1,), 1],
    ['25', '5', 'ErEk', 'Zarf Fiil Eki', '([ae]r[ae]k)', (-1,), 0],
    ['26', '6', 'DUkçE', 'Zarf Fiil Eki', '([dt][ıiuü]kç[ae])', (-1,), 2],
    ['27', '7', 'cEsInE', 'Zarf Fiil Eki', '(c[ae]s[ıi]n[ae])', (-1,), 2],
    ['28', '8', 'mEksIzIn', 'Zarf Fiil Eki', '(m[ae]ks[ıi]z[ıi]n)', (-1,), 2],
    ['29', '9', 'dUğUndE', 'Zarf Fiil Eki', '(d[ıiuü]ğ[ıiuü]nd[ae])', (-1,), 2],
    ['30', '1', 'EmE', 'Yetersizlik Eki', '([ea]m[ea])', (-1, 2, 4, 6, 8, 10, 12, 13, 15, 17, 20, 22, 24, 26, 29), 2],
    ['31', '1', 'XEmE', 'Yetersizlik Eki', '(y[ea]m[ea])', (-1, 2, 4, 6, 8, 10, 12, 13, 15, 17, 20, 22, 24, 26, 29), 1]]

fiil_cekim_ekleri = [['1', '0', 'DU', 'Bilinen Geçmiş Zaman', '([dt][ıiuü])', (-1, 24, 26, 30, 32, 33), 2],
                     ['2', '0', 'mUş', 'Öğrenilen Geçmiş Zaman', '(m[ıiuü]ş)', (-1, 23, 25, 27, 31, 33), 2],
                     ['3', '0', '(U)yor', 'Şimdiki Zaman', '([ıiuü]yor)', (-1, 23, 25, 27, 31, 33), 0],
                     ['4', '0', 'yor', 'Şimdiki Zaman', '(yor)', (-1, 23, 25, 27, 31, 33), 1],
                     ['5', '0', 'XEcEK', 'Gelecek Zaman', '(y[ae]c[ae][kğ])', (-1, 23, 25, 27, 31, 33), 1],
                     ['6', '0', 'EcEK', 'Gelecek Zaman', '([ae]c[ae][kğ])', (-1, 23, 25, 27, 31, 33), 0],
                     ['7', '0', 'Ar', 'Geniş Zaman', '([aeıiuü]r)', (-1, 23, 25, 27, 31, 33), 0],
                     ['8', '0', 'r', 'Geniş Zaman', '(r)', (-1, 23, 25, 27, 31, 33), 1],
                     ['9', '1', 'mElI', 'Gereklilik Kipi', '(m[ae]l[ıi])', (-1, 22, 25, 28, 31, 33), 2],
                     ['10', '1', 'XsE', 'Dilek Şart Kipi', '(ys[ae])', (-1, 24, 26, 30, 32, 33), 1],
                     ['11', '1', 'sE', 'Dilek Şart Kipi', '(s[ae])', (-1, 24, 26, 30, 32, 33), 0],
                     ['12', '1', 'XE', 'İstek Kipi', '(y[ae])', (-1, 22, 25, 29, 31, 33), 1],
                     ['13', '1', 'E', 'İstek Kipi', '([ae])', (-1, 22, 25, 29, 31, 33), 0],
                     ['14', '1', 'sUn', 'Emir Kipi', '(s[ıiuü]n)', (-1,), 2],
                     ['15', '1', 'XUnUz', 'Emir Kipi', '([yns][ıiuü]n[ıiuü]z)', (-1,), 1],
                     ['16', '1', 'UnUz', 'Emir Kipi', '([ıiuü]n[ıiuü]z)', (-1,), 0],
                     ['17', '1', 'XUn', 'Emir Kipi', '(y[ıiuü]n)', (-1,), 1],
                     ['18', '1', 'Un', 'Emir Kipi', '([ıiuü]n)', (-1,), 0],
                     ['19', '1', 'sUnlEr', 'Emir Kipi', '(s[ıiuü]nl[ae]r)', (-1,), 2],
                     ['20', '3', 'mU', 'Olumsuzluk Eki', '(m[ıiuü])', (-1, 4), 2],
                     ['21', '3', 'mE', 'Olumsuzluk Eki', '(m[ea])', (-1, 1, 2, 5, 9, 11, 14, 15, 17, 19), 2],
                     ['22', '4', 'XUm', '1. tekil kişi', '(y[ıiuü]m)', (0,), 1],
                     ['23', '4', 'Um', '1. tekil kişi', '([ıiuü]m)', (0,), 0],
                     ['24', '4', 'm', '1. tekil kişi', '(m)', (0,), 2],
                     ['25', '4', 'sUn', '2. tekil kişi', '(s[ıiuü]n)', (0,), 2],
                     ['26', '4', 'n', '2. tekil kişi', '(n)', (0,), 2],
                     ['27', '4', 'Uz', '1. çoğul kişi', '([ıiuü]z)', (0,), 0],
                     ['28', '4', 'XUz', '1. çoğul kişi', '(y[ıiuü]z)', (0,), 1],
                     ['29', '4', 'lIm', '1. çoğul kişi', '(l[ıi]m)', (0,), 2],
                     ['30', '4', 'k', '1. çoğul kişi', '(k)', (0,), 2],
                     ['31', '4', 'sUnUz', '2. çoğul kişi', '(s[ıiuü]n[ıiuü]z)', (0,), 2],
                     ['32', '4', 'nUz', '2. çoğul kişi', '(n[ıiuü]z)', (0,), 2],
                     ['33', '4', 'lEr', '3. çoğul kişi', '(l[ae]r)', (0,), 2],
                     ['34', '3', 'mEz', 'Olumsuzluk Eki', '(m[ea]z)', (-1, 1, 2, 23, 25, 31, 33), 2]]

fiil_ek_fiil_ekleri = [['1', '0', 'XDU', 'Hikaye', '(y[dt][ıiuü])', (-1, 8, 10, 13, 15, 16), 1],
                       ['2', '0', 'DU', 'Hikaye', '([dt][ıiuü])', (-1, 8, 10, 13, 15, 16), 0],
                       ['3', '0', 'XmUş', 'Rivayet', '(ym[ıiuü]ş)', (-1, 7, 9, 12, 14, 16), 1],
                       ['4', '0', 'mUş', 'Rivayet', '(m[ıiuü]ş)', (-1, 7, 9, 12, 14, 16), 0],
                       ['5', '0', 'XsE', 'Şart', '(ys[ea])', (-1, 8, 10, 13, 15, 16), 1],
                       ['6', '0', 'sE', 'Şart', '(s[ea])', (-1, 8, 10, 13, 15, 16), 0],
                       ['7', '1', 'Um', '1. tekil kişi', '([ıiuü]m)', (0,), 0],
                       ['8', '1', 'm', '1. tekil kişi', '(m)', (0,), 1],
                       ['9', '1', 'sUn', '2. tekil kişi', '(s[ıiuü]n)', (0,), 0],
                       ['10', '1', 'n', '2. tekil kişi', '(n)', (0,), 1],
                       ['11', '1', 'DUr', 'Bildirme eki', '([dt][ıiuü]r)', (-1, 16), 0],
                       ['12', '1', 'Uz', '1. çoğul kişi', '([ıiuü]z)', (0,), 0],
                       ['13', '1', 'k', '1. çoğul kişi', '(k)', (0,), 1],
                       ['14', '1', 'sUnUz', '2. çoğul kişi', '(s[ıiuü]n[ıiuü]z)', (0,), 0],
                       ['15', '1', 'nUz', '2. çoğul kişi', '(n[ıiuü]z)', (0,), 1],
                       ['16', '1', 'lEr', '3. çoğul kişi', '(l[ae]r)', (11,), 2]]

yardimci_fiiller = [['1', '3', 'eyle', '1. tekil kişi', '(eyle)', (-1,), 2],
                    ['2', '4', 'eD', '2. tekil kişi', '(e[dt])', (-1,), 2],
                    ['3', '3', 'ol', '3. tekil kişi', '(ol)', (-1,), 2]]

birlesik_fiil_ekleri = [['1', '4', 'yEbil', 'Yeterlik Bileşik Eylem Kipi', '([y][ae]bil)', (-1,), 1],
                        ['2', '4', 'Ebil', 'Yeterlik Bileşik Eylem Kipi', '([ae]bil)', (-1,), 0],
                        ['3', '4', 'yEmE', 'Olumsuzluk/Yetersizlik', '([y][ae]m[ae])', (-1, 1, 8, 10), 1],
                        ['4', '4', 'EmE', 'Olumsuzluk/Yetersizlik', '([ae]m[ae])', (-1, 1, 8, 10), 0],
                        ['5', '4', 'yEmEz', 'Olumsuzluk/Yetersizlik', '([y][ae]m[ae]z)', (-1,), 1],
                        ['6', '4', 'EmEz', 'Olumsuzluk/Yetersizlik', '([ae]m[ae]z)', (-1,), 0],
                        ['7', '4', 'mE', 'Olumsuzluk', '(m[ae])', (-1, 1, 8, 10), 2],
                        ['8', '4', 'yUver', 'Tezlik Bileşik Eylem Kipi', '([y][ıiuü]ver)', (-1,), 1],
                        ['9', '4', 'Uver', 'Tezlik Bileşik Eylem Kipi', '([ıiuü]ver)', (-1,), 0],
                        ['10', '4', 'yEgel', 'Tezlik Bileşik Eylem Kipi', '([y][ae]gel)', (-1,), 1],
                        ['11', '4', 'Egel', 'Tezlik Bileşik Eylem Kipi', '([ae]gel)', (-1,), 0],
                        ['12', '4', 'yEdur', 'Sürerlik Bileşik Eylem Kipi', '([y][ae]dur)', (-1,), 1],
                        ['13', '4', 'Edur', 'Sürerlik Bileşik Eylem Kipi', '([ae]dur)', (-1,), 0],
                        ['14', '4', 'yEgör', 'Sürerlik Bileşik Eylem Kipi', '([y][ae]gör)', (-1,), 1],
                        ['15', '4', 'Egör', 'Sürerlik Bileşik Eylem Kipi', '([ae]gör)', (-1,), 0],
                        ['16', '4', 'yEkal', 'Sürerlik Bileşik Eylem Kipi', '([y][ae]kal)', (-1,), 1],
                        ['17', '4', 'Ekal', 'Sürerlik Bileşik Eylem Kipi', '([ae]kal)', (-1,), 0],
                        ['18', '4', 'yEkoy', 'Sürerlik Bileşik Eylem Kipi', '([y][ae]koy)', (-1,), 1],
                        ['19', '4', 'Ekoy', 'Sürerlik Bileşik Eylem Kipi', '([ae]koy)', (-1,), 0],
                        ['20', '4', 'yEyaz', 'Yaklaşma Bileşik Eylem Kipi', '([y][ae]yaz)', (-1,), 1],
                        ['21', '4', 'Eyaz', 'Yaklaşma Bileşik Eylem Kipi', '([ae]yaz)', (-1,), 0]]

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
