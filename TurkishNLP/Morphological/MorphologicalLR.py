# -*- coding: utf-8 -*-

__version__ = '0.1'
__author__ = 'Esat Mahmut Bayol'

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

# Eğer bu kadar yazı da ne böyle! Diyorsanız silmek için derleyicinizin 'find and replace' kısmına #+.* regex kodunu
# yazarak temizleyebirsiniz.
# Yazılımın açıklamalarını kodların içinde yapmayı daha uygun gördüm. İleride yeterli vakti bulabilirsem belki bir
# döküman hazırlarım. Kodun içerisinde gerekli gödüğüm yerlerde dilbilgisi kurallarını da paylaşmayı düşünüyorum.
# Kısacası kitap gibi bir kod olacak :)
# Çok iyi Python bildiğimi söyleyemem. Bildiğim kadarı ile kafamdaki şablonu yazılama dökmeye çalışacağım.
# Amacım bir kelimeyi kök/gövde ve eklerine doğru şekilde ayırabilmek olacak. Allah'ın izni ve yardımı ile yaparız
# inşallah.
# Her işe besmele ile başlanır diyerek kodlamaya başlıyorum. Hayırlara vesile olur inşallah.

# ########## Bismillahirrahmanirrahim ##########

from re import compile
from TurkishNLP import trmi_bsucontrol, trmi_ksucontrol, spellword
from TurkishNLP.helpers import to_lower, unrepeated_list, tr_sozluk_yukle, son_sesli_bul, replace_cap_letter, lddistance
from TurkishNLP.Auxiliary.Tr_Suffix_to_Vt import *
from operator import itemgetter

# Gerekli kütüphaneleri yüklüyoruz. Zaten çoğu benim yazdığım yan yazılımlar diyebiliriz.
# (AuxiliaryCommands, TurkishGrammer, Auxiliary.Tr_Suffix_to_Vt)

vt_table_name = ek_tipleri
# vt_table_name değişkeni, isim çekim ekleri, ek fiil ekleri gibi ek çeşitlerinin isimlerini barındıran bir
# liste aslında. Bu değişken Auxiliary.Tr_Suffix_to_Vt içerisinde mevcut durumda. Burada da aynı veriyi
# kullanmam gerektiği için direk belirttiğim yoldan aldım değişkeni.
# vt_table_name = ['isim_ek_fiil_ekleri', 'isim_cekim_ekleri', 'x_fiil_ekleri', 'fiil_cekim_ekleri',
#                  'fiil_ek_fiil_ekleri', 'yardimci_fiiller', 'birlesik_fiil_ekleri', 'fiil_catisi']
# Bu değişkendeki ek tipleri veri tabanına aynı isimle yazılıyor. Ekleri veritabanına yazan Tr_Suffix_to_Vt.py
# dosyasında bir değişiklik yaparsam burda da yapmam gerekir diye direk değişkeni buraya aldım ki karışıklık olmasın.
# 17.07.2018 - İlk başta tüm olası ekleri oluşturup veritabanına yazıp her birini tek tek denemek mantıklı gelmişti.
# MorphologicalRL.py kodunu da buna göre yazmıştım fakat kodun çok yavaş çalıştığını düşündüğüm için sistemde
# değişiklik yapmaya karar verdim. Özellikle isim çekim eklerinde 1000'e yakın ihtimal çıkıyor (Gerçekte daha da
# fazladır!) ve her seferinde bunları veritabanından okuyarak denemek sistemi çok yavaşlatıyor diye düşünüyorum.
# Ekleri sıralama kurallarını baştan kontrol ederek tek tek denemeye karar verdim.
# Dilbilgisi kurallarını internetten araştırarak kural tabanlı bir ek ayırıcı yapmaya çalışacağım. Dilbilgisi
# konusunda eksiklerim varsa affola.
# Bazı konularda uzmanların dahi anlaşamadığını gördüğümde doğrusu çok şaşırdım. Bu yüzden bazı yerlerde tercih
# yapmam gerekti. Bence sonuçlar yeterince tatmin edici.

not_get_suffix = ('bağlaç', 'ünlem', 'zarf', '0')
# not_get_suffix demeti ek almayan kelime türlerini içerir. Bu türdeki kelimeler ek aldıklarında isim olurlar.
# '0' zaten kimya sembollerini gösterdiği için ek almaları gibi bir durum olası değil.

sozluk = tr_sozluk_yukle()
# Sözlüğümüzü veri tabanından okuyarak sozluk değişkenine aktarıyoruz.

dstem_temizleyici = compile('(\(.*?\))|({.*?})')
# Eklerine ayırdığımız grupların içerisindeki fazlalık olan ifadeleri temizleyen regex ifadesini tanımladık.

isim_ekler = [('isim_cekim_ekleri',),
              ('isim_ek_fiil_ekleri',),
              ('yardimci_fiiller',),
              ('isim_cekim_ekleri', 'isim_ek_fiil_ekleri')]
# Eğer bulunan kelime kökü 'isim' ise bu liste içerisindeki ekleri alabilir. Şu anda deneme amacı ile hazırladığımdan
# liste dar olabilir fakat genişletilebilir.

fiil_ekler = [('fiil_catisi',),
              ('birlesik_fiil_ekleri',),
              ('fiil_cekim_ekleri',),
              ('x_fiil_ekleri',),
              ('fiil_cekim_ekleri', 'fiil_ek_fiil_ekleri'),
              ('fiil_cekim_ekleri', 'x_fiil_ekleri'),
              ('fiil_catisi', 'fiil_cekim_ekleri'),
              ('birlesik_fiil_ekleri', 'fiil_cekim_ekleri'),
              ('x_fiil_ekleri', 'isim_cekim_ekleri'),
              ('birlesik_fiil_ekleri', 'fiil_cekim_ekleri', 'fiil_ek_fiil_ekleri')]
# Eğer bulunan kelime kökü 'fiil' ise bu liste içerisindeki ekleri alabilir. Şu anda deneme amacı ile hazırladığımdan
# liste dar olabilir fakat genişletilebilir.

tur_dict = {'isim': 'isim_ekler',
            'sıfat': 'isim_ekler',
            'edat': 'isim_ekler',
            'zamir': 'isim_ekler',
            'özel': 'isim_ekler',
            'nsz': 'isim_ekler',
            'fiil': 'fiil_ekler',
            'yardımcı fiil': 'fiil_ekler'}
# Ekin türüne göre hangi ekleri araması gerektiğini gösteren sözlük değişkenini tanımladık. Örneğin bulunan kökün
# türü 'özel' ise 'isim_ekler' listesindeki değerlere göre ek araması yapılacak.

suffix_shortname = {'isim_ek_fiil_ekleri': 'iefe',
                    'isim_cekim_ekleri': 'içe',
                    'x_fiil_ekleri': 'xfe',
                    'fiil_cekim_ekleri': 'fçe',
                    'fiil_ek_fiil_ekleri': 'fefe',
                    'yardimci_fiiller': 'yf',
                    'birlesik_fiil_ekleri': 'bfe',
                    'fiil_catisi': 'fç'}


# Ekler ayrıldığında kullanılacak kısaltılmış isimlerin sözlüğünü tanımladık.


def correct_stem(stemlist: list):
    # Türkçe kelimeler sesli uyumuna uymak zorundadır. Fakat dilimize yabancı dilden girmiş bazı kelimeler
    # sesli uyumlarına uymazlar. Bu gibi sesli uyumuna uymayan kelime kök/gövdeleri olsa da bazı ekler dışında
    # bu kelimelere eklenen ekler sesli uyumuna uymak zorundadır. Bu fonksiyon ile kelimenin EKLERİNİN sesli uyumu
    # kontrolü yapılmakta ve kurala uyan eklere sahip olasılıklar bir listede toplanmaktadır.
    correct_form = []

    bozan_ekler = (
        'yor', 'iyor', 'ıyor', 'uyor', 'üyor', 'ki', 'ken', 'leyin', 'mtırak', 'imtırak', 'ki', 'gil', 'daş', 'taş')
    # Ses uyumunu bozan eklerin listesi.

    wrong_end = ('nd',)
    # Kelime parçası yanlış bitiş listesi.

    for form in stemlist:
        # find_suffix_from_start fonksiyonu tarafından üretilmiş tüm olasılıkları tarıyoruz ve uygun olanları
        # correct_form listesine ekliyoruz.
        rform = dstem_temizleyici.sub('', form)
        lform = rform.split('+')

        if lform[0].endswith(wrong_end):
            continue
        # Eğer kök/gövde yanlış bitiş listesindeki bir harf grubu ile bitiyorsa bu olasılık yanlıştır diyoruz.

        son_sesli = son_sesli_bul(lform[0])
        # Kök/gövde son sesli harfini buluyoruz. Bu köke eklenen ekler eğer sesli uyumunu bozan ekler içerisinde
        # yer almıyorsa son harfe göre sesli uyumuna uymak zorundadır. Sadece son sesliyi alıyoruz çünkü kök sesli
        # uyumuna uymayabilir. Bu durumda bu kelimeyi yanlış kabul etmememiz gerekiyor. Sesli uyumuna uymayan
        # birçok kelime var. Örneğin otomobil, anne, elma vs...

        if not son_sesli:
            continue
        # Eğer son sesli bulunamadıysa bu bir kelime değildir. Kelimeler sesli harf barındırmak zorundadır.
        # Algoritmamız zaten bu tarz bir kök döndürmez. Ben garanti olsun diye bu denetimi yapıyorum.

        ksu_kontrol = True
        bsu_kontrol = True
        # Sesli uyumu kontrol değişkenini 'True' olarak tanımladık.
        ksu_ara = son_sesli
        bsu_ara = ''

        for eki in lform[1:]:
            # Kökün arkasından eklenen tüm ekleri son sesliye ekleyerek sesli uyumunu kontrol edeceğiz.
            if eki not in bozan_ekler:
                # Eğer ek bozan ekler içerisinde değilse ekleyip sesli uyumu kontrolü yapıyoruz.
                ksu_ara = ksu_ara + eki
                bsu_ara = bsu_ara + eki
                ksu_kontrol = trmi_ksucontrol(ksu_ara)
                bsu_kontrol = trmi_bsucontrol(bsu_ara)
                if (ksu_kontrol is False) or (bsu_kontrol is False):
                    break
            else:
                # Eğer ek bozan ekler içerisinde ise bu ekten sonraki ekler bu ekin son seslisine uyacağından
                # değişkenimizi sıfırlayıp son sesli harfi bozan ekin son seslisi olarak değiştiriyoruz.
                son_sesli = son_sesli_bul(eki)
                ksu_ara, bsu_ara = son_sesli, son_sesli
        if (ksu_kontrol is False) or (bsu_kontrol is False):
            # Eğer sesli uyumu 'False' olarak döndüyse bu ek dizilimi yanlıştır diyoruz ve listeye eklemeden
            # döngüye devam ediyoruz.
            continue

        sahis_eki_kontrol = re.findall('(\d\.\s\w+\skişi)', form)
        # ekler içerisindeki şahız eklerini bir listede topluyoruz.
        if sahis_eki_kontrol and (len(sahis_eki_kontrol) > 1):
            # eğer ekler birden fazla şahıs eki içeriyorsa yanlış kabul ederek liste dışı bırakıyoruz.
            continue

        correct_form.append(form)
        # Tüm değerlendirmelerden geçen kök/ek grupları doğru kabul edilerek listeye ekleniyor.
    return correct_form


class ClsEkBul:
    # Bu class ile kelimeyi kök ve eklerine ayıracağız... Doğru mu yapıyorum hiçbir fikrim yok fakat class olarak
    # yazmak mantıklı geldi bir an :)
    # 17.07.2018 - @staticmethod olarak yazdığım fonksiyonları belki class dışına alabilirim. Hatta farklı bir
    # dosyada bile toplayabilirim.
    # 28.07.2018 @staticmethod olarak yazdığım fonksiyonları class dışına aldım.
    def __init__(self, word):
        word = to_lower(word)
        if not word:
            self.result = []
            self.stems = []
        else:
            self.result = []
            self.stems = []
            self.word = word
            # Kök ve eklerine ayıracağımız kelimemiz 'word' değişkeni ile class'a geliyor. Biz bunu class'ın her
            # fonksiyonunda kullanabilmek için global değişken haline getirdik.

            self.stem_list = self.find_stem()
            # kelimenin olası köklerinin listesini 'stem_list' değişkenine atıyoruz.
            # Örneğin 'masalarının' kelimesi için kök listesi şu şekilde geliyor;
            # [('masal', 'isim', 6), ('masa', 'isim', 7), ('mas', 'isim', 8)]
            # Burada liste içerisindeki her bir demet bir olası kökü ifade eder. Demetin birinci nesnesi kökü,
            # ikinci nesnesi kökün türünü, üçüncü nesnesi Levenshtein distance'ı (İki kelime arasındaki uzaklığı
            # hesaplayan bir algoritma) gösterir.

            if self.stem_list:
                self.kok_ek_bul()
                # Eğer kelimede bir yazım yanlışı yoksa yada sözlükte olmayan bir kelime değilse mutlaka kök sonucu
                # dönecektir. Kök sonucu dönmediyse kelimeyi olduğu gibi sonuç listesine ekliyorum.
                self.result = correct_stem(self.result)
                self.result = self.son_kontrol()
                self.result = unrepeated_list(self.result)
                # Sonuç listemizi correct_stem fonksiyonu ile kontrol ederek tekrarsız liste haline getiriyoruz.
                self.stems = unrepeated_list([j.split('+')[0] for j in self.result])
            # Bulunan sonuçlardan kökleri ayırarak ayrı bir listede topluyoruz.

    # ---- OLASI KÖKLERİ BULMA FONKSİYONU ----
    # ----------------------------------------
    def find_stem(self):
        # Kök bulma algoritması sözlük tabanlı çalışır.
        # Sözlük hakkındaki detaylar için bkz. Auxiliary/sozlugu_veritabanina_aktar.py
        temp_stem_list = []
        # Olası ekleri toplamak için temp_stem_list adında boş bir liste oluşturuyoruz.
        word = replace_cap_letter(self.word)
        # Kelimenin içinde şapkalı harf var ise normale çeviriyoruz.
        first_syllable = spellword(word)
        if first_syllable is False:
            return []
        else:
            first_syllable = spellword(word)[0]
        # Kelimenin ilk hecesini buluyoruz.
        search_in_dict = [x for x in sozluk if x[0][:len(first_syllable)] == first_syllable]
        # Sözlük içerisinde kelimenin ilk hecesi ile başlayan kelime ve özelliklerini bir listede topluyoruz.
        if not search_in_dict and first_syllable[-1] in 'bcdgğ':
            yumusama_harfleri = {'b': 'p',
                                 'c': 'ç',
                                 'd': 't',
                                 'g': 'k',
                                 'ğ': 'k'}
            first_syllable = first_syllable[:-1] + yumusama_harfleri[first_syllable[-1]]
            search_in_dict = [x for x in sozluk if x[0][:len(first_syllable)] == first_syllable]
            if not search_in_dict:
                return []
            else:
                word = first_syllable + word[len(first_syllable):]

        if word.startswith('di'):
            temp_stem_list.append(('di', ('de', 'fiil'), 0))
        elif word.startswith('yi'):
            temp_stem_list.append(('yi', ('ye', 'fiil'), 0))
        # de- ve ye- fiilleri tek heceli olduğu için bir ayrıcalık yapmak zorunda kaldık.

        mstem = ''
        _mstem = ''
        yor_bul = re.search('[ıiuü]yor', word)
        if yor_bul:
            x, y = yor_bul.span()
            if x == 0:
                yor_bul = re.search('[ıiuü]*yor', word[x:])
                if yor_bul:
                    x, y = yor_bul.span()
                    mstem = word[:x]
                    if yor_bul.group()[0] in ('ı', 'u'):
                        _mstem = mstem + 'a'
                        mstem = word[:x + 1]
                    elif yor_bul.group()[0] in ('i', 'ü'):
                        _mstem = mstem[:-1] + 'e'
                        mstem = word[:x + 1]
                    else:
                        mstem = ''
            else:
                mstem = word[:x]
                if yor_bul.group()[0] in ('ı', 'u'):
                    _mstem = mstem + 'a'
                    mstem = word[:x + 1]
                elif yor_bul.group()[0] in ('i', 'ü'):
                    _mstem = mstem[:-1] + 'e'
                    mstem = word[:x + 1]
                else:
                    mstem = ''
        # Ünlü Daralması kontrolü yapıyoruz.

        for stem in search_in_dict:
            # Oluşturduğumuz sözlük dosyasını tek tek deniyeceğiz. Yukarıda bu sebeple sadece kelimenin ilk
            # hecesinden oluşan sözlük satırlarını ayrı bir listeye aldık. Aksi halde gereksiz birçok kelimeyi
            # denememiz gerekecekti. Eğer yazım yanlışı yapıldı ise bu algoritmanın düzgün çalışması mümkün değil.
            # Bu sebeple ileride yanlış yazılan kelimeleri düzeltmek üzere birşeyler yazılabilir.

            tlstem = to_lower(stem[0])
            # Sözlükteki kelimeyi küçük harfe çeviriyoruz.
            rpstem = replace_cap_letter(tlstem)
            # Sözlükteki kelimenin içinde şapkalı harf var ise normale çeviriyoruz.

            if stem[1] in not_get_suffix:
                if word == rpstem:
                    temp_stem_list.append((stem[0], stem[1], 0))
                    self.result.append(stem[0] + '(' + stem[1] + ')')
                    continue
                else:
                    continue
            # Eğer sözlük içerisindeki kelimenin türü(stem[1]) ek almayan kelimeler dizisinin (not_get_suffix)
            # içindeyse bu kelime ek alamaz demektir. Bu yüzden sadece aranan kelime, sözlükteki kelime ile tam
            # uyuşuyorsa olası sonuc listesine(sonuc) dahil edilir.
            # (Sözlük sıralaması açıklamaları için bkz. sozlugu_veritabanina_aktar.py)

            if mstem and (stem[1] == 'fiil') and (_mstem == rpstem):
                temp_stem_list.append((mstem, (_mstem, stem[1]), 0))
            # Ünlü Daralması kontrolü yapıyoruz.

            if word == rpstem:
                temp_stem_list.append((stem[0], stem[1], 0))
                self.result.append(stem[0] + '(' + stem[1] + ')')
            # Eğer kelime sözlükteki kelime ile aynı ise listemize ekliyoruz.

            if (word != rpstem) and (word.startswith(rpstem)):
                levenshtein_dist = lddistance(word, rpstem)
                temp_stem_list.append((tlstem, stem[1], levenshtein_dist))
                continue
            # Eğer kelime, sözlükteki kelime ile başlıyorsa
            # Levenshtein distance(İki kelime arasındaki uzaklığı hesaplayan bir algoritma)
            # hesaplası yaparak listemize ekliyoruz.

            letter_harmony = re.findall('\((\w+)\)', stem[2])
            # Sözlük kelimesinin özel bir ses olayı varmı diye sorguluyoruz.
            rp_letter_harmony = letter_harmony

            if letter_harmony:
                rp_letter_harmony = replace_cap_letter(rp_letter_harmony[0])
                if word.startswith(rp_letter_harmony):
                    levenshtein_dist = lddistance(word, rp_letter_harmony)
                    temp_stem_list.append((letter_harmony[0], (stem[0], stem[1]), levenshtein_dist))
            # Ses olayı bulundu ise ve kelimemiz bu ses olayı ile başlıyorsa listemize ekliyoruz.

        organized_list = sorted(unrepeated_list(temp_stem_list), key=itemgetter(2))
        # Tüm olası kök listesini Levenshtein distance değerine göre küçükten, büyüğe sıralıyoruz.
        # (Küçük olması yakın değer anlamına gelir) Gerçek kökümüz muhtemelen listenin en başlarında yer alıyordur.
        # Bu olası köklere ek ekleyerek ilk kelimemizi elde etmeye çalışacağız. Böylece gerçek köke ulaşmaya
        # çalışacağız. Eğer kelimeye ulaşılamazsa ya kelime yanlış yazılmıştır yada sözlükte o kelime ile ilgili bir
        # veri eksiktir. Test aşamasında sözlüğün tam anlamı ile oturacağını düşünüyorum.
        # Aslında Levenshtein distance değerini hiç hesaplamasakta aynı kökleri deneyeceğiz. Ben bunu sadece test
        # amaçlı yaptım. Levenshtein distance yakınlığı ile doğru kökü hesaplama olasılığımı görmek için şimdilik
        # hesaplayarak bu değeri ekliyorum. Eğer gerçek kök ile bu değer arasında bir bağıntı bulabilirsem olası kök
        # sayısını azaltarak işlem sayısını da azaltabilirim.
        return organized_list

    def kok_ek_bul(self):
        search_this_list = []
        for stem_tupple in self.stem_list:
            if type(stem_tupple[1]) is tuple:
                if stem_tupple[1][1] in tur_dict:
                    search_this_list = eval(tur_dict[stem_tupple[1][1]])
            else:
                if stem_tupple[1] in tur_dict:
                    search_this_list = eval(tur_dict[stem_tupple[1]])
            # stem_tupple[1] kökün türünü belirtiyor. tur_dict sözlüğü bu kök türüne göre bakılması gereken listenin
            # adını döndürüyor. Bunu eval ile yazdığımızdan o sitring ile aynı isme sahip değişkeni çağırmış oluyoruz.
            # Örneğin;
            # stem_tupple[1] = 'isim' ise tur_dict[stem_tupple[1]] = 'isim_ekler' oluyor ve isim_ekler değişkenini
            # çağırmış oluyoruz.
            if search_this_list:
                self.search_this_list(stem_tupple, search_this_list)
            # Bulunan her bir kök adayını eklerini bulmak için SearchThisList fonksiyonuna gönderiyoruz.

    def search_this_list(self, stem_tupple, search_this_list):
        for thislist in search_this_list:
            ekli_kok = []
            if len(thislist) == 1:
                ekli_kok = self.find_suffix_from_start(stem_tupple, thislist[0])
                if ekli_kok:
                    self.resulta_ekle(ekli_kok)
            else:
                lenz_this_list = len(thislist) - 1
                for z, _thislist in enumerate(thislist):
                    if z == 0:
                        ekli_kok = self.find_suffix_from_start(stem_tupple, _thislist)
                        if not ekli_kok:
                            break
                    else:
                        _ekli_kok = []
                        for ekli in ekli_kok:
                            _ekli_kok = _ekli_kok + self.find_suffix_from_start(ekli, _thislist)
                        if not _ekli_kok:
                            break
                        else:
                            ekli_kok = _ekli_kok
                            if z == lenz_this_list:
                                ekli_kok = self.resulta_ekle(ekli_kok)

    def resulta_ekle(self, liste):
        son_liste = []
        for sonuc in liste:
            temizlenmis = ''.join(sonuc.split('+'))
            temizlenmis = dstem_temizleyici.sub('', temizlenmis)
            if temizlenmis == self.word:
                self.result.append(sonuc)
            else:
                son_liste.append(sonuc)
        return son_liste

    def find_suffix_from_start(self, stem_tupple, thislist):
        temp_list = []
        if type(stem_tupple) is tuple:
            temp_list = self.ilk_eki_bul(stem_tupple, thislist)
        else:
            temp_list.append(stem_tupple)

        if not temp_list:
            return []

        genel_liste = temp_list
        ek_tipi_listesi = eval(thislist)
        while temp_list:
            aranacak_liste = temp_list
            temp_list = []
            for ekli_kelimeler in aranacak_liste:
                temizlenmis = ''.join(ekli_kelimeler.split('+'))
                temizlenmis = dstem_temizleyici.sub('', temizlenmis)
                kalan_ekler = self.word[len(temizlenmis):]

                if not kalan_ekler:
                    self.result.append(ekli_kelimeler)
                    continue

                ek_no = re.findall('\((\d+)-', ekli_kelimeler)
                ek_no = int(ek_no[-1])
                ek_kisa_adi = suffix_shortname[thislist]
                son_eklenen_ekin_kisa_adi = re.findall('{(\w+)}', ekli_kelimeler)[-1]

                if ek_kisa_adi == son_eklenen_ekin_kisa_adi:
                    ek_tipi_daraltilmis_listesi = [x for x in ek_tipi_listesi if ek_no in x[5]]
                else:
                    ek_tipi_daraltilmis_listesi = [x for x in ek_tipi_listesi if -1 in x[5]]

                for ek_tipi_satiri in ek_tipi_daraltilmis_listesi:
                    regex_code = ek_tipi_satiri[4]
                    regex = re.match(regex_code, kalan_ekler)

                    if regex:
                        ek = regex.group()
                        ek_no = ek_tipi_satiri[0]
                        ek_prop = ek_tipi_satiri[3]
                        comp = ekli_kelimeler + '+' + ek + '(' + ek_no + '-' + ek_prop + ')' + '{' + ek_kisa_adi + '}'
                        temp_list.append(comp)
            genel_liste = genel_liste + temp_list
        genel_liste = correct_stem(genel_liste)
        genel_liste = unrepeated_list(genel_liste)

        return genel_liste

    def ilk_eki_bul(self, stem_tupple, thislist):
        word = self.word
        stem = stem_tupple[0]
        suffixes = word[len(stem):]

        if type(stem_tupple[1]) is tuple:
            stem_type = '-'.join(stem_tupple[1])
        else:
            stem_type = stem_tupple[1]

        list_var = eval(thislist)

        ek_tipi_daraltilmis_listesi = [x for x in list_var if -1 in x[5]]

        temp_list = []
        for ek_tipi_satiri in ek_tipi_daraltilmis_listesi:
            regex_code = ek_tipi_satiri[4]
            regex = re.match(regex_code, suffixes)
            if regex:
                ek = regex.group()
                ek_no = ek_tipi_satiri[0]
                ek_prop = ek_tipi_satiri[3]
                comp = stem + '(' + stem_type + ')' + '+' + ek + '(' + ek_no + '-' + ek_prop + ')' + '{' + \
                       suffix_shortname[thislist] + '}'
                temp_list.append(comp)

        for sonuc in temp_list:
            temizlenmis = ''.join(sonuc.split('+'))
            temizlenmis = dstem_temizleyici.sub('', temizlenmis)
            if temizlenmis == self.word:
                self.result.append(sonuc)
                temp_list.remove(sonuc)

        return temp_list

    def son_kontrol(self):
        klist = []
        for form in self.result:
            form_list = form.split('+')
            if '-' in form_list[0]:
                temp_stem = form_list[0]
                cor_stem = temp_stem[temp_stem.find('(') + 1:temp_stem.find('-')]
                stem_type = temp_stem[temp_stem.find('-') + 1: temp_stem.find(')')]
                form_list[0] = cor_stem + '(' + stem_type + ')'
                form = '+'.join(form_list)
            klist.append(form)
        return klist


if __name__ == '__main__':
    a = ClsEkBul('CÜMLEDE')
    print(a.result)
    print(a.stems)
