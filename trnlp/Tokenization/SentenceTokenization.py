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
from trnlp.helpers import *
from trnlp import Ceb

# ('([:|B|8|;][=|-]*[\)|D])', 'EMOJİ GÜLEN'),
# ('([:|B|8|;][=|-]*[\(])', 'EMOJİ SOMURTAN'),

shortlist = load_shortlist()
taninan_duzenler = [('([\d{1,3}\.]*\d{3}\s*[TL|€|\$]+)', 'PARA'),
                    ('(\d+-\d+\s[yüz|bin|milyon|milyar|trilyon]+)', 'SAYI'),
                    ('(\d+\s[yüz|bin|milyon|milyar|trilyon]+)', 'SAYI'),
                    ('(\(.*?\))|(".*?")|(\[.*?\])|({.*?})', 'AÇIKLAMA'),
                    ('(\d{1,2}[\.|/|-]\d{1,2}[\.|/|-]\d{2,4})', 'TARİH F1'),
                    ('(\d{1,2}\s[a-zA-ZŞşİıÜüĞğ]+\s\d{2,4})', 'TARİH F2'),
                    ('(\d{1,2}:\d{1,2}:\d{1,2})', 'SAAT F1'),
                    ('(\d{1,2}:\d{1,2})', 'SAAT F2'),
                    ('(\d{1,2}\s*a[m\.]+)', 'SAAT F3'),
                    ('(\d{1,2}\s*p[m\.]+)', 'SAAT F4'),
                    ('(https?://www\.[a-zA-Z0-9]+[\.a-zA-Z0-9]+)', 'WEB ADRES F1'),
                    ('(www\.[a-zA-Z0-9]+[\.a-zA-Z0-9]+)', 'WEB ADRES F2'),
                    ('([a-zA-Z0-9+_\-\.]+@[a-zA-Z]+[\.a-zA-Z]+)', 'EPOSTA'),
                    ('(\d+\.|[XVI]+\.)', 'INCI'),
                    ('([\d{1,3}][\.\d{3}]+,*\d*)', 'SAYI'),
                    ('(\d+)', 'SAYI'),
                    ('\s', '')]

duzen_regex = ''
for duzen in taninan_duzenler:
    if duzen_regex:
        duzen_regex = duzen_regex + '|' + duzen[0]
    else:
        duzen_regex = duzen_regex + duzen[0]

eol_punch = ('...', '!..', '?..', '.', ':', '!', '?')
punch = '.\',;?"'
ayrilacak_ifadeler = '()[]"{}'


def satir_duzenle(str_grp: str):
    str_row_list = str_grp.split('\n')
    genel_liste = []
    satir_listesi = []
    for row in str_row_list:
        row = row.strip()

        if not row:
            genel_liste.append('')
            continue

        if row[-1] == '-':
            satir_listesi.append(row[:-1])
        else:
            if satir_listesi:
                satir_listesi.append(row)
                genel_liste.append(''.join(satir_listesi))
                satir_listesi = []
            else:
                genel_liste.append(row)

    str_row_list = genel_liste
    genel_liste = []
    satir_listesi = []
    for row in str_row_list:
        row = row.strip()

        if not row:
            if not satir_listesi:
                genel_liste.append('\\n')
            continue

        if satir_listesi:
            sl = ''.join(satir_listesi) + row
            row_kontrol = pr_tr_kontrol(sl)
        else:
            row_kontrol = pr_tr_kontrol(row)

        if False in row_kontrol:
            satir_listesi.append(row + ' ')
            continue
        else:
            if satir_listesi:
                satir_listesi.append(row)
                genel_liste.append(''.join(satir_listesi))
                satir_listesi = []
            else:
                genel_liste.append(row)

    return genel_liste


def eol_kontrol(kelime_parcasi):
    for eol in eol_punch:
        if eol in kelime_parcasi:
            return True
    return False


def arr_row(row_pr):
    arr_list = []
    for z in row_pr:
        if not z:
            continue

        z = z.strip()

        if z == '':
            continue

        if z[0] in ayrilacak_ifadeler:
            arr_list.append(z)
            continue
        else:
            split_row = z.split(' ')

        for x in split_row:
            if x.strip() != '':
                arr_list.append(x)
    return arr_list


def pr_tr_ayir(cumleler):
    _pr_tr_ayir = re.split('(\(.*?\))|(".*?")|(\[.*?\])|({.*?})', cumleler)
    return list(filter(None, _pr_tr_ayir))


def prop_tokenize(str_grp: str):
    split_txt = satir_duzenle(str_grp)
    gen_list = []

    for row in split_txt:
        row_pr = pr_tr_ayir(row)
        gen_list.append(row_pr)
    return gen_list


def baslik_kontrol(row: str):
    def baglac_mi(_word):
        stem_sonuc = False
        for stem in Ceb(_word).stems:
            if 'bağlaç' in stem:
                stem_sonuc = True
        return stem_sonuc

    if not row:
        return False

    if row.isupper():
        return 'ÜB'

    row = row.strip()
    split_row = row.split(' ')
    sonuc = True

    for word in split_row:
        word = word.strip()

        if not word:
            continue

        if word[0].isupper():
            continue
        else:
            if baglac_mi(word):
                continue
            else:
                sonuc = False
                break

    if sonuc is True:
        return 'AB'
    else:
        return False


def pr_tr_kontrol(str_grp: str):
    def parantez_kontrolu():
        if str_grp.count('(') == str_grp.count(')'):
            return True
        else:
            return False

    def tirnak_kontrol():
        if str_grp.count('"') % 2 == 0:
            return True
        else:
            return False

    def koseli_kontrol():
        if str_grp.count('[') == str_grp.count(']'):
            return True
        else:
            return False

    return parantez_kontrolu(), tirnak_kontrol(), koseli_kontrol()


def token(str_grp: str):
    split_txt = str_grp.split('\n')
    gen_list = []
    for row in split_txt:
        gen_list.append('\\n')
        tlist = []
        ttxt = ''
        for char in row:
            if char.isspace():
                if ttxt:
                    tlist.append(ttxt)
                    ttxt = ''
                continue

            if char.isalpha():
                ttxt = ttxt + char
                continue
            else:
                if ttxt:
                    tlist.append(ttxt)
                    ttxt = ''
                tlist.append(char)

        if ttxt:
            tlist.append(ttxt)
        gen_list = gen_list + tlist
    return gen_list[1:]


def word_tokenize(str_grp: str):
    return list(filter(None, re.split('[^A-Za-zçÇğĞıİöÖşŞüÜâÂêÊîÎôÔûÛ]', str_grp)))


def tr_word_tokenize(str_grp: str):
    tr_liste = []
    none_tr_liste = []
    liste = word_tokenize(str_grp)
    for kelime in liste:
        tr_mi = Ceb(kelime).stems
        if tr_mi:
            tr_liste.append(kelime)
        else:
            none_tr_liste.append(kelime)
    return tr_liste, none_tr_liste


def sentence_token_wsign(str_grp: str):
    str_grp = noktalama_degistir(str_grp)
    prop_list = satir_duzenle(str_grp)
    gen_list = []
    gecici = ['{CÜMLE}']
    for part in prop_list:
        if part == '\\n':
            gen_list.append(part)
            continue

        baslik_mi = baslik_kontrol(part)
        part_list = [x.strip() for x in part.split(' ') if x.strip()]

        if baslik_mi:
            baslik = ' '.join(part_list)
            gen_list.append('{' + baslik_mi + '}' + baslik + '{/' + baslik_mi + '}')
            continue

        if gecici != ['{CÜMLE}']:
            pass
        else:
            gecici = ['{CÜMLE}']
        part_list = list(filter(None, re.split(duzen_regex, part)))
        # print(part_list)
        # exit()
        regbul = False

        for kisim in part_list:
            kisim = kisim.strip()

            if to_lower(kisim) in shortlist:
                gecici.append('{KI}' + kisim + '{/KI}')
                continue

            for regexim in taninan_duzenler:
                dfind = re.search(regexim[0], kisim)
                if dfind:
                    gecici.append('{' + regexim[1] + '}' + dfind.group() + '{/' + regexim[1] + '}')
                    regbul = True
                    break
                else:
                    regbul = False

            if regbul is True:
                regbul = False
                continue

            if eol_kontrol(kisim) is False:
                gecici.append(kisim)
                continue
            else:
                if len(kisim) == 2:
                    if kisim[0].isalpha() and (kisim[1] == '.'):
                        gecici.append(kisim)
                        continue
                if kisim in eol_punch or kisim[-1] in eol_punch:
                    gecici.append(kisim)
                    gecici.append('{/CÜMLE}')
                    gecici = ' '.join(gecici)
                    gen_list.append(gecici)
                    gecici = ['{CÜMLE}']
                    continue
                feol = kisim.find('.')
                if -1 < feol < len(kisim):
                    gecici.append(kisim[:feol + 1])
                    gecici.append('{/CÜMLE}')
                    gecici = ' '.join(gecici)
                    gen_list.append(gecici)
                    gecici = ['{CÜMLE}', kisim[feol + 1:]]
                    continue
    if gecici:
        gen_list.append(' '.join(gecici) + '{/CÜMLE}')

    return gen_list


def sentence_token(str_grp: str):
    str_grp = noktalama_degistir(str_grp)
    prop_list = satir_duzenle(str_grp)
    gen_list = []
    gecici = []
    for part in prop_list:
        if part == '\\n':
            continue

        baslik_mi = baslik_kontrol(part)
        part_list = [x.strip() for x in part.split(' ') if x.strip()]

        if baslik_mi:
            baslik = ' '.join(part_list)
            gen_list.append(baslik)
            continue

        if gecici:
            pass
        else:
            gecici = []

        part_list = list(filter(None, re.split(duzen_regex, part)))
        # print(part_list)
        # exit()
        regbul = False

        for kisim in part_list:
            kisim = kisim.strip()

            if to_lower(kisim) in shortlist:
                gecici.append(kisim)
                continue

            for regexim in taninan_duzenler:
                dfind = re.search(regexim[0], kisim)
                if dfind:
                    gecici.append(dfind.group())
                    regbul = True
                    break
                else:
                    regbul = False

            if regbul is True:
                regbul = False
                continue

            if eol_kontrol(kisim) is False:
                gecici.append(kisim)
                continue
            else:
                if len(kisim) == 2:
                    if kisim[0].isalpha() and (kisim[1] == '.'):
                        gecici.append(kisim)
                        continue
                if kisim in eol_punch or kisim[-1] in eol_punch:
                    gecici.append(kisim)
                    gecici = ' '.join(gecici)
                    gen_list.append(gecici)
                    gecici = []
                    continue
                feol = kisim.find('.')
                if -1 < feol < len(kisim):
                    gecici.append(kisim[:feol + 1])
                    gecici = ' '.join(gecici)
                    gen_list.append(gecici)
                    gecici = [kisim[feol + 1:]]
                    continue
    if gecici:
        gen_list.append(' '.join(gecici))

    return gen_list


if __name__ == '__main__':
    a = """Chomsky Öncesi Zihinci-Dilsel Yaklaşımlar
Chomsky’nin kuramını hazırlayan felsefi arka plan “zihinci” geleneğe dayanır.
Bu gelenek “var olan her şeyin zihinsel terimlerle açıklanabileceğini öne süren görüş”
(Cevizci 2012: 466) olarak tanımlanır. Zihinci yaklaşımlarda dil düşüncelerin
iletilmesinde bir araç durumundadır. Dil felsefesinde de anlamın kullanımdan önce
geldiğini varsayan yaklaşımlar zihincilik tarafında durur.
Zihinci geleneğin ilk varsayımları Platon’a dayandırılabilir Ancak dile dair
modern zihinci perspektifin tarihi arka planı, “seslerin ruhtaki düşüncelerin sembolleri
olduğunu” söyleyen Aristoteles’ten başlayıp sonraları belirgin biçimde Descartes’ın,
Port-Royal Okulu’nun düşünceleriyle devam eden bir çizgi olarak tasvir edilebilir
(Altınörs 2012). Bu isimlere Humboldt da eklenebilir.
Chomsky, klasik zihinci yaklaşımın Platon’dan beri var olan – insanda bazı
becerilerin doğuştan geldiği vb. – varsayımlarının çağdaş bir yorumunu yapar:
“Bilgimizin ve kavrayışımızın bir bölümü doğuştan vardır, bu biyolojik özelliğimizin
bir bölümüdür, genetik olarak belirlenmiştir, tıpkı kanatlı olmak yerine, kol ve bacaklı
olmamıza neden olan ortak özelliklerimizin unsurları gibi.” (2009: 15). Dolayısıyla
Chomsky, deneyciliğin doğuştan “boş levha” iddiasına karşılık zihinci öğretilerin
“doğuştancı” tarafında durur.
Platon’da düşünce bir içsel konuşma, dilse gerçeğin bilgisini anlatmada yetersiz
bir araçtır. Aristoteles’te konuşma yine düşüncelerin göstergesi durumundadır.
Yeniçağda Descartes’ın ruh ve bedeni iki ayrı töz olarak gören felsefesinde dil, sadece
insana özgü bir yeti olarak “akıllı ruh”un düşüncesinin bir ifadesidir. Descartes’a göre,
hayvanlar “hiçbir zaman, bizim düşüncelerimizi başkalarına bildirmek için yaptığımız
gibi, sözleri ve diğer işaretleri birleştirerek kullanmaz” (2015: 54), dolayısıyla
konuşamazlar. Bunun nedeni onların dil yetisinden tamamen mahrum olmalarıdır. """
    # print(a)
    print_list_item(sentence_token(a))
    # sentence_token(a)
    # print(re.search('www\.[a-zA-Z0-9]+\.[a-zA-Z0-9]+', "yeni paragraf başlıyor.internet sitesinin linki, www.google.com'dur.").group())
