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

from trnlp.data.suffix_tables import *
from trnlp.controler import *
from trnlp.helper import *

__all__ = ['BaseFinder',
           'Derivational',
           'Inflections',
           'TrnlpWord',
           'writeable']


def writeable(inf_dict: dict, long=False) -> str:
    """
    Ek bulma fonksiyonu ile üretilen sözlük eklerin kısaltma isimleri kullanılarak yazdırılır.
    :param long: True olması durumunda, kısaltma isimler yerine uzun açıklamalar kullanılır
    :param inf_dict: Ek bulma fonksiyonu ile üretilen sözlük
    :return: arka(isim,sıfat)+daş{İi}[4_26]+lar{EfKe3ç}[1_52]
    """
    if not inf_dict:
        return ''

    if long:
        inf_dict['suffixTypes'] = [SUFFIX_SHORTLIST[x] for x in inf_dict['suffixTypes']]

    fadding = "{}({})".format(inf_dict['verifiedBase'], ','.join(inf_dict['baseType']))
    zip1 = zip(inf_dict['suffixes'], inf_dict['suffixTypes'])
    zip1 = [a + '{' + b + '}' for a, b in zip1]
    sfx_plc = ['[' + '_'.join((str(a), str(b))) + ']' for a, b in inf_dict['suffixPlace']]
    zip2 = list(zip(zip1, sfx_plc))

    if not zip2:
        return fadding
    elif len(zip2) > 1:
        return "{}+{}".format(fadding, '+'.join([a + b for a, b in zip2]))
    else:
        return "{}+{}{}".format(fadding, zip2[0][0], zip2[0][1])


class BaseFinder:
    _mainDict = {}  # Ana Sözlük
    _pronDict = {}  # Özel İsim Sözlüğü
    _abbrDict = {}  # Kısaltmalar Sözlüğü

    def __init__(self):
        self.__useMain = True  # Kök aramada ana sözlük kullanılsın mı?
        self.__usePron = True  # Kök aramada özel isimler sözlüğü kullanılsın mı?
        self.__useAbbr = False  # Kök aramada kısaltmalar sözlüğü kullanılsın mı?
        self._orgWord = ""  # Girilen kelimenin orjinal hali
        self._sorting = dict()
        self._word = ""  # Girilen kelimenin işlem görmüş hali
        self.__load_lexicons()

    def __dir__(self):
        return self.__dict__.keys()

    @property
    def usemain(self) -> bool:
        return self.__useMain

    @property
    def usepron(self) -> bool:
        return self.__usePron

    @property
    def useabbr(self) -> bool:
        return self.__useAbbr

    @usemain.setter
    def usemain(self, isuse: bool):
        self.__useMain = isuse

    @usepron.setter
    def usepron(self, isuse: bool):
        self.__usePron = isuse

    @useabbr.setter
    def useabbr(self, isuse: bool):
        self.__useAbbr = isuse

    @classmethod
    def __load_lexicons(cls):
        if not cls._mainDict:
            cls._mainDict = decompress_pickle(package_path() + 'data/gen_tr_lex.pbz2')
        if not cls._pronDict:
            cls._pronDict = decompress_pickle(package_path() + 'data/prop_tr_lex.pbz2')
        if not cls._abbrDict:
            cls._abbrDict = decompress_pickle(package_path() + 'data/short_tr_lex.pbz2')

    def setword(self, string_word: str):
        self._orgWord = ""
        self._word = ""
        self.__load_lexicons()
        self._orgWord = change_punch(string_word.strip())
        self._word = repa(repc(to_lower(string_word.strip())))

    @staticmethod
    def _splitter(string: str) -> list:
        """
        Kelimeyi parçalar. Örneğin 'deneme' -> ['deneme', 'denem', 'dene', 'den', 'de', 'd']
        :param string: Kök bulmak için parçalanacak string veri
        :return: Liste içerisinde parçalanmış string değerler döndürür.
        """
        result = [string[:x] for x in range(1, len(string) + 1)]
        result.reverse()
        return result

    def pos_bases(self) -> list:
        """
        'self.word' değişkeni ile tanımlanan kelimenin olası köklerini bulur.
        :return: Liste içerisinde sözlük(dict) olarak döndürür.
        """
        if any((self.__useMain, self.__useAbbr, self.__usePron)):
            return self._find_in_lexicon()
        else:
            self.__useMain = True
            return self._find_in_lexicon()

    def _find_in_lexicon(self) -> list:
        """
        Parçalanmış kelime listesindeki her bir kelimeyi genel sözlük(cls._mainDict) içerisinde arar.
        :return: Sözlük içerisinde bulunan sonuçları liste halinde döndürür.
        """

        org = to_lower(self._orgWord)
        splited_string = self._splitter(self._word)
        result = []
        sorting = dict()

        if "." in self._orgWord:
            pword = re.sub(r"\W", "", org[:org.rfind(".")])
            residual = org[org.rfind(".") + 1:]
            if self.useabbr and (pword in self._abbrDict):
                for a2 in self._abbrDict[pword]:
                    result.append((a2, residual))
        elif "'" in self._orgWord:
            pword = re.sub(r"\W", "", org[:org.rfind("'")])
            residual = org[org.rfind("'") + 1:]
            if residual and self.usepron and (pword in self._pronDict):
                for a2 in self._pronDict[pword]:
                    result.append((a2, residual))
            if self.useabbr and (pword in self._abbrDict):
                for a2 in self._abbrDict[pword]:
                    result.append((a2, residual))
            if word_to_number(pword):
                result.append(({'base'        : pword,
                                'verifiedBase': pword,
                                'baseType'    : ['isim,sayı'],
                                'baseProp'    : [''],
                                'etymon'      : 'Türkçe',
                                'event'       : 0,
                                'currentType' : ['isim'],
                                'purview'     : '0'}, residual))
        elif isCap(self._orgWord):
            if self.usepron:
                for a1 in splited_string:
                    if a1 in self._pronDict:
                        for a2 in self._pronDict[a1]:
                            result.append((a2, None))
            if self.__useMain:
                for a1 in splited_string:
                    if a1 in self._mainDict:
                        for a2 in self._mainDict[a1]:
                            result.append((a2, None))
            if self.useabbr:
                for a1 in splited_string:
                    if a1 in self._abbrDict:
                        for a2 in self._abbrDict[a1]:
                            result.append((a2, None))
            if word_to_number(self._word):
                result.append(({'base'        : self._word,
                                'verifiedBase': self._word,
                                'baseType'    : ['isim,sayı'],
                                'baseProp'    : [''],
                                'etymon'      : 'Türkçe',
                                'event'       : 0,
                                'currentType' : ['isim'],
                                'purview'     : '0'}, None))
        else:
            if self.__useMain:
                for a1 in splited_string:
                    if a1 in self._mainDict:
                        for a2 in self._mainDict[a1]:
                            result.append((a2, None))
            if word_to_number(self._word):
                result.append(({'base'        : self._word,
                                'verifiedBase': self._word,
                                'baseType'    : ['isim,sayı'],
                                'baseProp'    : [''],
                                'etymon'      : 'Türkçe',
                                'event'       : 0,
                                'currentType' : ['isim'],
                                'purview'     : '0'}, None))
            if self.usepron:
                for a1 in splited_string:
                    if a1 in self._pronDict:
                        for a2 in self._pronDict[a1]:
                            result.append((a2, None))
            if self.useabbr:
                for a1 in splited_string:
                    if a1 in self._abbrDict:
                        for a2 in self._abbrDict[a1]:
                            result.append((a2, None))

        result = [self.__update_dict(a1) for a1 in result]
        result = unrepeated_list(result)

        if result:
            counter = 0
            for a1 in result:
                counter += 1
                factor = 1

                if any(char in self._orgWord for char in ["â", "û", "î"]):
                    if any(char in a1['verifiedBase'] for char in ["â", "û", "î"]):
                        factor = 0.01

                adding = (a1['verifiedBase'], ",".join(a1['baseType']))

                if adding not in sorting:
                    sorting[adding] = counter * factor

            self._sorting = sorting

        return result

    def __update_dict(self, tpl: tuple) -> dict:
        """
        Bulunan kök sözlüğündeki bilinmeyen(None) değerleri doldurur ve geri döndürür.
        :param tpl: Bulunan kök sözlüğü ve kalan ek yada None
        :return: Kök sözlüğünün düzenlenmiş halini döndürür.
        """
        dl = tpl[0]
        residual = tpl[1]

        dl['orgWord'] = self._orgWord
        dl['word'] = self._word
        dl['suffixes'] = []
        dl['suffixPlace'] = []
        dl['suffixTypes'] = []
        dl['suffixProp'] = []

        if residual is None:
            ext_base = re.sub(r"\W", "", dl['base'])
            dl['residual'] = self._word[len(ext_base):]
        else:
            dl['residual'] = residual

        return dl


class Derivational(BaseFinder):
    _dafVerbDict = {}  # Fiile eklenebilecek yapım ekleri sözlüğü
    _dafNounDict = {}  # İsme eklenebilecek yapım ekleri sözlüğü

    def __init__(self):
        super().__init__()
        self.__load_daf_dict()

    def __dir__(self):
        return self.__dict__.keys()

    @classmethod
    def __load_daf_dict(cls):
        if not cls._dafVerbDict:
            cls._dafVerbDict = decompress_pickle(package_path() + 'data/dafVerb.pbz2')
        if not cls._dafNounDict:
            cls._dafNounDict = decompress_pickle(package_path() + 'data/dafNoun.pbz2')

    def _dfn(self, abc: str) -> list:
        """
        Arta kalan eki parçalar ve her bir parçayı isme eklenebilen yapım ekleri(_dafNoun)
        sözlüğü içerisinde arar ve sonucu döndürür.
        :param abc: aranacak arta kalan ek
        :return: sözlükte bulunan sonuçları liste halinde döndürür.
        """
        return [a2 for a1 in self._splitter(abc) if a1 in self._dafNounDict for a2 in self._dafNounDict[a1]]

    def _dfv(self, abc: str) -> list:
        """
        Arta kalan eki parçalar ve her bir parçayı fiile eklenebilen yapım ekleri(_dafVerb)
        sözlüğü içerisinde arar ve sonucu döndürür.
        :param abc: aranacak arta kalan ek
        :return: sözlükte bulunan sonuçları liste halinde döndürür.
        """
        return [a2 for a1 in self._splitter(abc) if a1 in self._dafVerbDict for a2 in self._dafVerbDict[a1]]

    @staticmethod
    def _der_type(sfx_place: list, sfx_types: list) -> list:
        """
        Kelimeye eklenen eklerin kelimeyi dönüştürdüğü kelime tipini bulur.
        :param sfx_place: Eklerin tablo ve satır numaralarının listesi
        :param sfx_types: Eklerin tanımları
        :return: Liste içerisinde kelime tiplerini döndürür.
        """
        result = []
        for i, place in enumerate(sfx_place, 0):
            if (place[0] == 2) and (sfx_types[i] in {'Olz', 'Ytsz'}):
                result.append('fiil')
            else:
                result.append(daf_type[sfx_place[i][0]])
        return result

    def derivational_lr(self) -> list:
        """
        Soldan sağa kelimeye eklenmiş olan olası yapım eklerini arar.
        :return: Liste içerisinde sözlük olarak sonuç döndürür.
        """
        main_dict_list = self.pos_bases()

        if not main_dict_list:
            return []

        for main_dict in main_dict_list:
            if not main_dict['residual']:
                continue

            if self._abbrDict and (main_dict['baseType'] == ['kısaltma']):
                continue

            if 'fiil' in main_dict['currentType'][-1]:
                pos_der = self._dfv(main_dict['residual'])
            else:
                pos_der = self._dfn(main_dict['residual'])

            for piece in pos_der:
                temp_dict = dict(main_dict)
                add_type = self._der_type(piece[1], piece[2])
                temp_dict['currentType'] = temp_dict['currentType'] + add_type
                temp_dict['suffixes'] = main_dict['suffixes'] + piece[0]
                temp_dict['suffixPlace'] = main_dict['suffixPlace'] + piece[1]
                temp_dict['suffixTypes'] = main_dict['suffixTypes'] + piece[2]
                temp_dict['suffixProp'] = main_dict['suffixProp'] + piece[3]
                temp_dict['residual'] = temp_dict['residual'][len(''.join(piece[0])):]

                if (temp_dict not in main_dict_list) and (bsc(temp_dict)) and (ssc(temp_dict, 1)):
                    main_dict_list.append(temp_dict)
        return main_dict_list


class Inflections(Derivational):
    _infNounDict = {}  # İsme eklenebilecek çekim ekleri sözlüğü
    _infVerbDict = {}  # Fiile eklenebilecek çekim ekleri sözlüğü

    def __init__(self):
        super().__init__()
        self.__load_inf_dict()

    def __dir__(self):
        return self.__dict__.keys()

    @classmethod
    def __load_inf_dict(cls) -> None:
        if not cls._infNounDict:
            cls._infNounDict = decompress_pickle(package_path() + 'data/infNoun.pbz2')
        if not cls._infVerbDict:
            cls._infVerbDict = decompress_pickle(package_path() + 'data/infVerb.pbz2')

    @staticmethod
    def _current_type(table_no: int, row_no: int) -> str:
        """
        Bulunan ekin kelimeye eklendiğindeki kelime tipini bulur
        :param table_no: Ekin tablo numarası
        :param row_no: Ekin satır numarası
        :return: isim, fiil vb. şekilde kelime tipini döndürür.
        """
        if table_no == 1:
            if 58 > row_no > 54:
                return 'isim,zarf'
            elif 34 < row_no < 55:
                return 'fiil'
            else:
                return 'isim'
        elif table_no == 2:
            if 62 > row_no > 59:
                return 'isim,zarf'
            else:
                return 'fiil'

    def _ifn(self, abc: str) -> list or None:
        """
        Arta kalan eki isme eklenebilen çekin ekleri(inf_noun)
        sözlüğü içerisinde arar ve sonucu döndürür.
        :param abc: aranacak arta kalan ek
        :return: sözlükte bulunan sonuçları liste halinde döndürür.
        """
        if abc in self._infNounDict:
            return [a1 for a1 in self._infNounDict[abc]]
        else:
            return None

    def _ifv(self, abc: str) -> list or None:
        """
        Arta kalan eki fiile eklenebilen çekin ekleri(inf_verb)
        sözlüğü içerisinde arar ve sonucu döndürür.
        :param abc: aranacak arta kalan ek
        :return: sözlükte bulunan sonuçları liste halinde döndürür.
        """
        if abc in self._infVerbDict:
            return [a1 for a1 in self._infVerbDict[abc]]
        else:
            return None

    def _inflection_lr(self, base_list=None) -> list:
        """
        Soldan sağa kelimeye eklenmiş olan olası çekim eklerini arar.
        :return: Liste içerisinde sözlük olarak sonuç döndürür.
        """
        result = []

        if base_list is None:
            main_dict_list = self.derivational_lr()
        else:
            main_dict_list = base_list

        if not main_dict_list:
            return []

        for main_dict in main_dict_list:
            if not main_dict['residual']:
                if (main_dict not in result) and bsc(main_dict) and ssc(main_dict):
                    result.append(main_dict)
                continue

            if 'fiil' in main_dict['currentType'][-1]:
                available = self._ifv(main_dict['residual'])
            else:
                available = self._ifn(main_dict['residual'])

            if available is None:
                continue

            for x in available:
                temp_dict = dict(main_dict)
                add_type = [self._current_type(j[0], j[1]) for j in x[1]]
                temp_dict['currentType'] = temp_dict['currentType'] + add_type
                temp_dict['suffixes'] = main_dict['suffixes'] + x[0]
                temp_dict['suffixPlace'] = main_dict['suffixPlace'] + x[1]
                temp_dict['suffixTypes'] = main_dict['suffixTypes'] + x[2]
                temp_dict['suffixProp'] = main_dict['suffixProp'] + x[3]
                temp_dict['residual'] = ''

                if temp_dict['baseType'] == ['kısaltma']:
                    temp_dict = abbr_control(temp_dict)
                    if temp_dict:
                        [result.append(tmp) for tmp in temp_dict if tmp not in result]
                else:
                    if temp_dict not in result:
                        src_ = general_control(temp_dict)
                        [result.append(x) for x in src_ if x not in result]
        return result

    def inflection_lr(self) -> list:
        return self._inflection_lr()

    def inflection_rl(self) -> list:
        result = []
        if "'" in self._orgWord:
            splited_word = [0, repc(to_lower(self._orgWord.split("'")[0]))]
        else:
            splited_word = self._splitter(self._word)

        temp_dict = {'base'        : "",
                     'verifiedBase': "",
                     'baseType'    : [],
                     'baseProp'    : ['0'],
                     'purview'     : '0',
                     'etymon'      : 'Türkçe',
                     'event'       : 0,
                     'currentType' : [],
                     'orgWord'     : self._orgWord,
                     'word'        : self._word,
                     'suffixes'    : [],
                     'suffixPlace' : [],
                     'suffixTypes' : [],
                     'suffixProp'  : [],
                     'residual'    : ""}

        for root in splited_word[1:]:
            residual = self._word[len(root):]
            temp_dict['base'] = root
            temp_dict['verifiedBase'] = root
            temp_dict['residual'] = residual

            if ("'" in self._orgWord) or (isCap(self._orgWord)):
                temp_dict['baseType'] = ['özel,kısaltma']
                temp_dict['currentType'] = ['özel,kısaltma']
                result = result + self._inflection_lr([temp_dict])

            temp_dict['baseType'] = ['fiil']
            temp_dict['currentType'] = ['fiil']
            result = result + self._inflection_lr([temp_dict])

            temp_dict['baseType'] = ['isim']
            temp_dict['currentType'] = ['isim']
            result = result + self._inflection_lr([temp_dict])

        if not result:
            temp_dict['base'] = self._word
            temp_dict['verifiedBase'] = self._word
            temp_dict['baseType'] = ['isim']
            temp_dict['currentType'] = ['isim']
            temp_dict['residual'] = ""
            result.append(temp_dict)
        return result


class TrnlpWord(Inflections):

    def __init__(self):
        super().__init__()
        self.__inf = []
        self.__morphology = {}
        self.__getBase = ""
        self.__getBaseType = ""
        self.__getStem = ""
        self.__getStemType = ""

    def __dir__(self):
        return self.__dict__.keys()

    def __str__(self):
        return writeable(self.__morphology)

    def setword(self, string_word: str) -> None:
        self.__morphology = {}
        self.__getBase = ""
        self.__getBaseType = ""
        self.__getStem = ""
        self.__getStemType = ""
        self._orgWord = string_word.strip()
        self._word = repa(repc(to_lower(string_word.strip())))
        self.__inf = self.inflection_lr()

        if self.__inf:
            self._arr_args()

    @property
    def get_base(self) -> str:
        return self.__getBase

    @property
    def get_base_type(self) -> str:
        return self.__getBaseType

    @property
    def get_stem(self) -> str:
        return self.__getStem

    @property
    def get_stem_type(self) -> str:
        return self.__getStemType

    @property
    def get_morphology(self) -> dict:
        return self.__morphology

    @property
    def get_inf(self) -> list:
        return self.__inf

    def _arr_args(self) -> None:
        self.__morphology = self._arr_infs()[0]
        self.__getBase = self.__morphology['verifiedBase']
        self.__getBaseType = ','.join(self.__morphology['baseType'])
        stem, stem_type = self._find_stem()
        self.__getStem = stem
        self.__getStemType = stem_type

    def _arr_infs(self) -> list:
        def nv_counter(arg):
            return self._sorting[(arg['verifiedBase'], ",".join(arg['baseType']))]

        temp1 = [x for x in self.__inf if 'kısaltma' in x['baseType']]
        temp2 = [x for x in self.__inf if 'özel' in x['baseType']]
        temp3 = [x for x in self.__inf if ('özel' not in x['baseType']) and ('kısaltma' not in x['baseType'])]
        if temp1:
            temp1.sort(key=lambda x: len(x['suffixes']))
        if temp2:
            temp2.sort(key=lambda x: len(x['suffixes']))
        if temp3:
            temp3.sort(key=lambda x: nv_counter(x))

        if "." in self._orgWord:
            result = temp1 + temp3 + temp2
        elif "'" in self._orgWord:
            result = temp2 + temp1 + temp3
        elif isCap(self._orgWord):
            result = temp2 + temp3 + temp1
        else:
            result = temp3 + temp2 + temp1

        return result

    def _find_stem(self) -> tuple:
        last_list = list()
        morph = self.__morphology['base']
        current_type = self.__getBaseType
        i = -1
        for table, m_row in self.__morphology['suffixPlace']:
            i += 1
            if (table > 2) or (self.__morphology['suffixTypes'][i] in der_type):
                morph = morph + self.__morphology['suffixes'][i]
                current_type = self.__morphology['currentType'][i + 1]
                last_list = (table, m_row)
            elif table < 3:
                break

        if last_list:
            table, m_row = last_list
            if (5 in st_dict[table][m_row][5]) and (morph[-1] in terminal_devoicing):
                morph = morph[:-1] + terminal_devoicing[morph[-1]]
        else:
            morph = self.__morphology['verifiedBase']

        return morph, current_type

    def s_base(self, rlist=None) -> list:
        if not self.__inf:
            return []
        if rlist is None:
            rlist = self.__inf
        sbase_len = min(len(x['verifiedBase']) for x in rlist)
        return [x for x in rlist if len(x['verifiedBase']) == sbase_len]

    def l_base(self, rlist=None) -> list:
        if not self.__inf:
            return []
        if rlist is None:
            rlist = self.__inf
        lbase_len = max(len(x['verifiedBase']) for x in rlist)
        return [x for x in rlist if len(x['verifiedBase']) == lbase_len]

    def s_suffix(self, rlist=None) -> list:
        if not self.__inf:
            return []
        if rlist is None:
            rlist = self.__inf
        ssuffix_len = min(len(x['suffixes']) for x in rlist)
        return [x for x in rlist if len(x['suffixes']) == ssuffix_len]

    def l_suffix(self, rlist=None) -> list:
        if not self.__inf:
            return []
        if rlist is None:
            rlist = self.__inf
        lsuffix_len = max(len(x['suffixes']) for x in rlist)
        return [x for x in rlist if len(x['suffixes']) == lsuffix_len]

    def stemming(self):
        return self.inflection_rl()

    def is_negative(self) -> float:
        if not self.__inf:
            return False
        isneg = 0
        for x in self.__inf:
            if ('Olz' in x['suffixTypes']) or ('Ytsz' in x['suffixTypes']) or ((4, 4) in x['suffixPlace']) or (
                    'NEG' in x['baseProp']):
                isneg += 1
        if len(self.__inf) == 0:
            return 0
        return isneg / len(self.__inf)

    def is_plural(self) -> float:
        if not self.__inf:
            return 0
        isplu = 0
        for x in self.__inf:
            if 'TPL' in x['baseProp']:
                isplu += 1
                continue
            for _prop in x['suffixProp']:
                if 13 in _prop:
                    isplu += 1
                    break
        return isplu / len(self.__inf)

    def spelling(self) -> list:
        return syllabification(re.sub(r"\W", "", self._orgWord))

    def correct_form(self, arg=None):
        if arg is None:
            bdict = self.__morphology
        else:
            bdict = arg

        if not bdict:
            return ""

        if 'özel' in bdict['baseType']:
            if bdict['suffixes']:
                appl = bdict['verifiedBase']
                for i in range(len(bdict['suffixes'])):
                    if ("Ye-" in bdict['suffixTypes'][i]) or (bdict['suffixPlace'][i][0] > 2):
                        appl = appl + bdict['suffixes'][i]
                    else:
                        appl = appl + "'" + "".join(bdict['suffixes'][i:])
                        break
                return appl
            else:
                return bdict['verifiedBase']
        elif 'kısaltma' in bdict['baseType']:
            if 'SN' in bdict['baseProp']:
                return "{}{}".format(bdict['verifiedBase'], ''.join(bdict['suffixes']))
            else:
                return "{}'{}".format(bdict['verifiedBase'], ''.join(bdict['suffixes']))
        else:
            if bdict['event'] == 0:
                return "{}{}".format(bdict['verifiedBase'], ''.join(bdict['suffixes']))
            else:
                return "{}{}".format(bdict['base'], ''.join(bdict['suffixes']))


if __name__ == '__main__':
    pass
