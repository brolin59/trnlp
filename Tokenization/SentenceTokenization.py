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
from Auxiliary.TurkishGrammer import to_lower
from Auxiliary.AuxiliaryCommands import load_shortlist
# Madde işaretleri aktif değil. Tüm yazı taranarak öncelikle satır başı ve satır sonu olabilecek kısımlar işaretlenmeli.

# Türkçe kısalmalar listesi.
shortlist = load_shortlist()

# haric listesindeki düzenli ifadeler satır sonu olarak değerlendirilmez.
haric = ('\d+\.', '\d+\.\d+', '\d+\.\d+\.\d+', '[A-ZÇĞİÖŞÜ]\.', '[XVI]+\.', '.*?w+?\.?\w+\.\w+.*', '.*@\w+\..*^[\']',
         '\w?\.?\w?\.?\w\.\w\.', '\w?\.?\w?\.?\w\.\w\.\'\w+', '\d+:\d+:?\d+?', '\d+-\d+.', '\d+-\d+-\d+.', 'https://.*')

# Satır Sonu İfadeler
eol_punch = ('...', '.', ':', '!', '?')

# Satır Başı İfadeler
bol_punch = ('-', '*', '\d+\.')

ayrilacak_ifadeler = '()[]"{}'

madde_isaretleri = ('\d+\.', '\d+ \.', '\d+-', '\d+ -', '\w+\.', '\w+ \.', '\w+-', '\w+ -','[XVI]+\.', '[XVI]+ \.',
                    '[XVI]+-', '[XVI]+ -', '\*', '-')


def noktalama_degistir(satir):
    rep_text = satir
    char_rep_dict = {'”': '"',
                     '“': '"',
                     '’': "'",
                     '‘': "'",
                     "`": "'",
                     "..": "...",
                     '…': '...',
                     'ș': 'ş',
                     '""': '"',
                     '\'\'': '"'}

    for old, new in char_rep_dict.items():
        rep_text = rep_text.replace(old, new)
    return rep_text


def parcala(cumleler):
    parca = re.split('[ \n]', cumleler)
    parca = [x for x in parca if x != '']
    return parca


def eol_kontrol(kelime_parcasi):
    for eol in eol_punch:
        if eol in kelime_parcasi:
            return True
    return False


def pr_tr_kontrol(cumleler):
    pr_tr_ayir = re.split('(\(.*?\))|(".*?")|(\[.*?\])|({.*?})', cumleler)
    return pr_tr_ayir


def cumle_sonu_mu(klm):
    kontrolcu = True
    # Eğer içinde eol_punch bulunan "kelime" hariç listesinde mevcut ise cumle sonunu ifade etmez.
    for reg in haric:
        regex = re.match(reg, klm)
        if regex and (regex.group() == klm):
            kontrolcu = False
            break
    # Eğer içinde eol_punch bulunan "kelime" kısaltmalar içerisinde mevcut ise cumle sonunu ifade etmez.
    if to_lower(klm) in shortlist:
        kontrolcu = False
    return kontrolcu


def baslik_bul(cmller):
    satirlar = []
    satir_ayir = cmller.split('\n')
    for satir in satir_ayir:
        if satir:
            satir_split = satir.split(' ')
        else:
            continue

        satir_split = [x.strip() for x in satir_split if x]
        baslik = False
        for kelime in satir_split:
            if kelime.isalpha() and (kelime[0].isupper()):
                baslik = True
            else:
                baslik = False
                break
        if baslik is True:
            satir = '{{B' + ' '.join(satir_split) + '\B}'
        satirlar.append(satir)
    return satirlar


def tire_kontrol(cml):
    len_cml = len(cml) - 1
    gecici_liste = []
    genel_liste = []
    for i, satir in enumerate(cml):
        satir = satir.strip()
        if (satir[-1] == '-') and (i < len_cml):
            if cml[i + 1].strip()[0].isalpha():
                gecici_liste.append(satir.strip()[:-1])
                continue

        if gecici_liste:
            gecici_liste.append(satir)
            gecici = ''.join(gecici_liste)
            genel_liste.append(gecici)
            gecici_liste = []
        else:
            genel_liste.append(satir)

    return '\n'.join(genel_liste)


# Kural tabanlı cümle ayırıcı
def cumle_ayir(cumleler: str):
    # Tanınmayan karakterleri bilinen hallerine çeviriyoruz. char_rep_dict sözlüğü genişletilerek
    # daha kapsamlı hale getirilebilir.
    cumleler = noktalama_degistir(cumleler)
    # Yazı dizisi içerisinde başlık olabilecek kısımları işaretliyoruz.
    cumleler = baslik_bul(cumleler)
    # Yazı dizisinde sonu '-' ile biten satırlar hece ayırması olarak değerlendirilir.
    cumleler = tire_kontrol(cumleler)
    kelimeler = [x.strip() for x in pr_tr_kontrol(cumleler) if (x is not None) and (x.strip() != '')]
    parca_listesi = []
    for parcalar in kelimeler:
        if parcalar.startswith('{{B'):
            if parcalar.endswith(eol_punch):
                baslik = parcalar[3:-3]
            else:
                baslik = parcalar[3:-3] + ':'
            parca_listesi.append(baslik)
            continue
        if parcalar[0] not in ayrilacak_ifadeler:
            parcalar = parcala(parcalar)
            parca_listesi.extend(parcalar)
        else:
            parca_listesi.append(parcalar)

    cumlecik = []
    cumle = []
    for parcalar in parca_listesi:
        if cumlecik and (parcalar[0] in ayrilacak_ifadeler):
            cumlecik.append(parcalar)
            continue
        if (eol_kontrol(parcalar) is True) and (cumle_sonu_mu(parcalar) is True):
            cumlecik.append(parcalar)
            join_add = ' '.join(cumlecik)
            cumle.append(join_add.replace(' .', '.'))
            cumlecik = []
        else:
            cumlecik.append(parcalar)
    if cumlecik:
        cumle.append(' '.join(cumlecik))
    return cumle


if __name__ == '__main__':
    pass
