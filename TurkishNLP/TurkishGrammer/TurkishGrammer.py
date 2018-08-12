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
from TurkishNLP.helpers import to_lower, wordtoten

# ////////////////////////////Türkçe bir sözcüğün başında “c, ğ, l, m, n, r, v, z” sesleri bulunmaz. Kısmı yapılacak.

All_lower_char = 'aâeêıîioôöuûübcçdfgğhjklmnprsştvyzqwx'
All_upper_char = 'AÂEÊIÎİOÔÖUÛÜBCÇDFGĞHJKLMNPRSŞTVYZQWX'
lower_vowel = 'aâeêıîioôöuûü'
upper_vowel = 'AÂEÊIÎİOÔÖUÛÜ'
lower_quiet = 'bcçdfgğhjklmnprsştvyzqwx'
upper_quiet = 'BCÇDFGĞHJKLMNPRSŞTVYZQWX'

clean_punch = re.compile('[^aâeêıîioôöuûübcçdfgğhjklmnprsştvyzAÂEÊIÎİOÔÖUÛÜBCÇDFGĞHJKLMNPRSŞTVYZ]')
clean_quiet = re.compile('[^aâeêıîioôöuûü]')

digits = '0123456789'
punc = """!"#$%&'()*+,-./:;<=>?@[\]^_{|}~"""
spec = '\n\t'


# Kelimenin harflerinin n'li durumunu çıkarır.
# Örneğin; char_gram('deneme', 2) ==> ['de', 'en', 'ne', 'em', 'me']
def char_gram(word, n=2):
    len_word = len(word)
    ngram_list = []

    if len_word == n:
        ngram_list.append(word)
    elif len_word < n:
        return []
    else:
        for i, char in enumerate(word):
            if i < len_word - (n - 1):
                ngram_list.append(word[i:i + n])

    return ngram_list


# Kelimelerin n'li durumunu çıkarır.
# Kelimeler liste olarak verilmelidir. Bir yazı içerisindeki kelimelerin listesini elde etme için TextStatistic'teki
# wordlist komutu kullanılabilir.
def word_gram(word_list: list, n=2):
    len_word = len(word_list)
    ngram_list = []

    if len_word == n:
        ngram_list.append(word_list)
    elif len_word < n:
        return []
    else:
        for i, char in enumerate(word_list):
            if i < len_word - (n - 1):
                ngram_list.append(word_list[i:i + n])

    return ngram_list


# Türkçe heceleme algoritması. Heceleme sonucunda elde edilen hece sayısı, kelime içerisindeki sesli harf sayısına
# eşit değilse False döndürür. Heceleme doğru şekilde tamamlandıysa heceleri bir liste içerisinde geri döndürür.
def spellword(word: str):
    """

    :type word: str
    """
    # Kaynak TDK; Türkçede kelime içinde iki ünlü arasındaki ünsüz, kendinden sonraki ünlüyle hece kurar:
    # a-ra-ba, bi-çi-mi-ne, in-sa-nın, ka-ra-ca vb. Kelime içinde yan yana gelen iki ünsüzden ilki kendinden
    # önceki ünlüyle, ikincisi kendinden sonraki ünlüyle hece kurar: al-dı, bir-lik, sev-mek vb. Kelime içinde
    # yan yana gelen üç ünsüz harften ilk ikisi kendinden önceki ünlüyle, üçüncüsü kendinden sonraki ünlüyle hece
    #  kurar: alt-lık, Türk-çe, kork-mak vb. İlk heceden sonraki heceler ünsüzle başlar. Bitişik yazılan
    # kelimelerde de bu kurala uyulur: ba-şöğ-ret-men, il-ko-kul, Ka-ra-os-ma-noğ-lu vb. Batı kökenli kelimeler,
    # Türkçenin hece yapısına göre hecelere ayrılır: band-rol, kont-rol, port-re, prog-ram, sant-ral, sürp-riz,
    # tund-ra, volf-ram vb.
    clean_word = re.sub(clean_quiet, '', word)
    num_cut = [('100001', 3), ('001000', 5), ('00101', 3), ('10001', 3), ('01001', 3), ('0100', 4), ('1001', 2),
               ('1000', 2), ('0101', 2), ('101', 1), ('010', 2), ('011', 2), ('110', 1), ('100', 3), ('0010', 4)]

    syllable_list = []
    syllable = ""
    wton = wordtoten(word)

    for i in range(wton.count('1') + 1):
        for start_wton, word_cut in num_cut:
            if wton.count('1') == 1:
                syllable_list.append(word)
                word = ""
                wton = ""
            elif wton.startswith(start_wton):
                syllable = syllable + word[:word_cut]
                word = word[word_cut:]
                wton = wton[word_cut:]
                syllable_list.append(syllable)
                syllable = ""
                break

    if word:
        syllable_list.append(word)
    # print(incoming_word, " : ", "-".join(syllable_list))
    if len(syllable_list) == len(clean_word):
        return syllable_list
    else:
        return False


# Küçük sesli uyumu kontrolü. True yada False döndürür.
def trmi_ksucontrol(word):
    # Düz Sesliler: a, e, ı, i
    # Yuvarlak Sesliler: o, ö, u, ü
    # Dar Sesli Harfler: ı, i, u, ü
    # Geniş Sesli Harfler: a, e, o, ö
    # Bir sözcükte düz ünlü harflerden  (a, e, ı, i) sonra yine düz ünlü harfler(a, e, ı, i) gelebilir.
    # Bir sözcükte yuvarlak ünlü harflerden (o, ö, u, ü) sonra düz/geniş (a, e) ve dar/yuvarlak (u, ü) sesli
    #  harfler gelebilir.
    # Küçük ünlü uyumunda her bir sesli harf kendinden önceki sesli harften sorumludur.
    # Küçük sesli uyumu kontrolü
    # sonu “ol” ya da “alp” ile biten
    # yabancı sözcüklere getirilen ekler bu kurala uymaz ve ince sesli içerirler. Bu
    # duruma örnek olarak “kalp” ve “gol” sözcükleri verilebilir.
    # • -yor, -ken , -ki, -leyin, -imtrak, -gil ekleri sesli uyumuna uymazlar.
    if not word:
        return True

    duz_sesliler = 'aâeêıîi'
    yuvarlak_sesliler = 'oôöuûü'
    duz_genis_dar_yuvarlak = 'aâeêuûü'

    lower_word = to_lower(word).strip()
    clr_word = clean_quiet.sub('', lower_word)
    lenght_vow = len(clr_word)

    i = 1
    ksu = True
    while i < lenght_vow:
        i += 1
        if (clr_word[i - 2] in duz_sesliler) and (clr_word[i - 1] not in duz_sesliler):
            ksu = False
            break

        if (clr_word[i - 2] in yuvarlak_sesliler) and (clr_word[i - 1] not in duz_genis_dar_yuvarlak):
            ksu = False
            break

    return ksu


# Büyük sesli uyumu kontrolü. True yada False döndürür.
def trmi_bsucontrol(word):
    # Kural olarak; ince seslilerden sonra ince sesliler, kalın seslilerden sonra kalın sesliler gelir
    # ince sesliler = e,i,ö,ü
    # kalın sesliler = a,ı,o,u
    # Büyük sesli uyumu kontrolü
    # sonu “ol” ya da “alp” ile biten
    # yabancı sözcüklere getirilen ekler bu kurala uymaz ve ince sesli içerirler. Bu
    # duruma örnek olarak “kalp” ve “gol” sözcükleri verilebilir.
    # • -yor, -ken , -ki, -leyin, -imtrak, -gil ekleri sesli uyumuna uymazlar.
    if not word:
        return True

    kalin_unlu_harfler = 'aâıîoôuû'
    ince_unlu_harfler = 'eêiöü'

    lower_word = to_lower(word)
    clr_word = clean_quiet.sub('', lower_word)
    lenght_vow = len(clr_word)

    if not clr_word:
        return True

    bsu = True
    if (clr_word[0] in kalin_unlu_harfler) and (lenght_vow > 1):
        for i in clr_word[1:]:
            if i not in kalin_unlu_harfler:
                bsu = False
                break

    if (clr_word[0] in ince_unlu_harfler) and (lenght_vow > 1):
        for i in clr_word[1:]:
            if i not in ince_unlu_harfler:
                bsu = False
                break
    return bsu


def trmi_nb_uyumu(word):
    # Türkçe’de birleşik sözcük ve yer adları dışında n ve b sessizleri yan yana bulunmaz.
    if 'nb' in word:
        nb = False
    else:
        nb = True
    return nb


def trmi_son_sessiz_uyumu(word):
    iword = to_lower(word)
    # Türkçe bir sözcüğün sonunda süreksiz yumuşak sessiz (b, c, d, g) bulunmaz, böyle sesler süreksiz sert
    # sessizlere (p, ç, t, k) dönüşür.
    sys = ('b', 'c', 'd', 'g')
    if iword[-1] in sys:
        sys = False
    else:
        sys = True
    return sys


def trmi_ilk2_sessiz_uyumu(word):
    iword = to_lower(word)
    nword = wordtoten(iword)
    # Türkçe’de sözcük iki sessiz harf ile başlayamaz.
    if nword[:2] == '00':
        first_two_letters = False
    else:
        first_two_letters = True

    return first_two_letters


def trmi_son3_sessiz_uyumu(word):
    iword = to_lower(word)
    nword = wordtoten(iword)
    # Türkçe’de sözcük üç sessiz harf ile bitemez.
    if nword[-3:] == '000':
        last_three_letters = False
    else:
        last_three_letters = True

    return last_three_letters


def trmi_son2_sessiz_uyumu(word):
    iword = to_lower(word)
    nword = wordtoten(iword)
    # Türkçe’de sözcük ve hece sonlarında bulunabilecek sessiz çiftleri
    last_two_letters = {'l': 'çkpt',
                        'n': 'çkt',
                        'r': 'çkpst',
                        's': 't',
                        'ş': 't'}

    if nword.endswith('00') and (iword[-2] in last_two_letters):
        second_letter = iword[-2]
        if iword[-1] in last_two_letters[second_letter]:
            last_two = True
        else:
            last_two = False
    else:
        last_two = True

    return last_two


def sessiz_uyumu(word):
    iword = to_lower(word)
    nword = wordtoten(iword)

    # Bu kurala göre, sert sessizlerden
    # sonra sert sessiz veya sert karşılığı bulunmayan yumuşak sessiz gelebilir. “ç - f - h - k
    # - p - s - ş – t” harflerinden sonra “ç - f - h - k - p - s - ş - t - l - m - n - r – y” harfleri
    # gelmelidir.
    #
    # Sert karşılığı bulunmayan yumuşak sessizlerden sonra tüm sessizler
    # gelebilir. “l - m - n - r – y” harflerinden sonra bütün sessiz harfler gelebilir. Sert
    # karşılığı bulunan yumuşak sessizlerden sonra yumuşak sessizler gelebilir. “b - c - d -
    # g - ğ - j - v – z” harflerinden sonra “b - c - d - g - ğ - j - v - z - l - m - n - r – y”
    # harfleri gelmelidir.

    sert_sessiz = ('ç', 'f', 'h', 'k', 'p', 's', 'ş', 't')
    sert_sessiz_kar = ('ç', 'f', 'h', 'k', 'p', 's', 'ş', 't', 'l', 'm', 'n', 'r', 'y')
    yum_sessiz = ('b', 'c', 'd', 'g', 'ğ', 'j', 'v', 'z')
    yum_sessiz_kar = ('b', 'c', 'd', 'g', 'ğ', 'j', 'v', 'z', 'l', 'm', 'n', 'r', 'y')
    sksiz_yumusak_sessiz = ('l', 'm', 'n', 'r', 'y')

    ss_sessiz = False
    if '00' in nword:
        nnword = nword
        iiword = iword
        while '00' in nnword:
            mt = re.search('00', nnword)
            x, y = mt.span()
            iiword = iiword[x:]

            if iiword[0] in sksiz_yumusak_sessiz:
                iiword = iiword[y:]
                nnword = nnword[y:]
                ss_sessiz = True
                continue

            if iiword[0] in sert_sessiz and iiword[1] in sert_sessiz_kar:
                iiword = iiword[y:]
                nnword = nnword[y:]
                ss_sessiz = True
                continue

            if iiword[0] in yum_sessiz and iiword[1] in yum_sessiz_kar:
                iiword = iiword[y:]
                nnword = nnword[y:]
                ss_sessiz = True
                continue

            if ss_sessiz is not True:
                ss_sessiz = False
                break
    return ss_sessiz


if __name__ == '__main__':
    print(spellword('enstrümanımı'))
    # with open('C:/Users/bilgisayar/PycharmProjects/NLP/Yedek/sayilmis_kelimeler.txt', 'r', encoding='utf8') as fl:
    #     lines = [(line.strip()).split('\t')[0] for line in fl if (line.strip()).split('\t')[1] != '1']
    # del fl
    # for i in lines:
    #     hecele = spellword(i)
    #     if hecele and (len(hecele) > 1) and (i[0] == 'o'):
    #         print(i, '\t\t', hecele)
