# PYTHON TÜRKÇE DOĞAL DİL İŞLEME - TURKISH NLP

## TÜRKÇE İÇİN DOĞAL DİL İŞLEME ARAÇLARI
  
## ÖNEMLİ : trnlp_old.rar dosyasını indirerek kullanmaya devam edebilirsiniz. İşlerimin yoğunluğundan dolayı projeye yeterli vakti ayıramadığım için bir süre ekleme yada düzeltme yapılmayacaktır. Mevcut halinde kodlar düzenlenmemiş olup birçok eksiği ve hatası vardır. Bundan sonraki süreçte her bir özellik ayrı repo olarak yayınlanacak ve geliştirilme süreci tamamlandıktan sonra tüm özellikler bir araya toplanarak paket haline getirilecektir.

Klasör yapısı ve kullanılabilecek tüm komutlar için [Türkçe Doğal Dil işleme Wiki sayfasını inceleyebilirsiniz.](https://github.com/brolin59/PHYTON-TURKCE-DOGAL-DIL-ISLEME---TURKISH-NLP/wiki)

trnlp klasörünü Python'un kurulu olduğu dizin içerisinde \Lib\site-packages\ dizinin içine kopyalamanız yeterlidir.
  
Ne Python ne de Türkçe dilbigim çok iyi olmamasına rağmen ***hobi*** olarak yazdığım birkaç kodu sizlerle paylaşmak istedim. Aslında ilk başta ilgim bir yazılım dili öğrenmek üzerineydi. Biraz araştırmadan sonra Python öğrenmeye karar verdim. Doğal dil işleme konusuna merakım ise makine öğrenmesi çalışmalarını araştırırken oluştu. Yazılım dili öğrenirken bir projeye başlamanın faydalı olacağı fikrini benimsediğim için böyle bir projeye başladım. Aslında bu konuda yapılmış çalışmalar var. Az önce de belirttiğim gibi benim niyetim kendimi geliştirmek. Yanında az da olsa birkaç kişiye faydam dokunursa ne ala...
Eminim bu konulardaki bilgisi benden çok daha iyi olan arkadaşlar bu paylaşımları bir üst seviyeye çıkarmada bana yardımcı olabilirler. 
Hobi olarak başladığım bu işin faydalı olması dileği ile...
  
### MorphologicalLR.py :
  
***MorphologicalLR sözlük ve kural tabanlı*** çalışan kök/gövde ve kelimenin eklerini bulmak için hazırladığım bir algoritmadır. 
Halen test aşamasında olduğum için ***eksikleri yada hataları*** olabilir. Henüz işin başındayız diyebiliriz.
   
Şu an için yapım eklerini tanımlamadım. Sözlüğü oluşturmak baya bir meşakkatli oldu ve çok zamanımı aldı. Halen eksikleri 
ve yanlışları olmasına rağmen yine de iş görür durumda sözlük dosyası. Sözlük dosyasını **Data/tr_NLP.sqlite** içinde 
bulabilirsiniz.
  
***Kelime kök/gövde ve eklerini*** bulmak için yazdığım algoritmanın örnek kullanımı şu şekildedir:
  
``` python
import trnlp
kelime = 'oğlumun'
print('Kelime kök/gövdesi : ', trnlp.find_stems(kelime))
print('Eklere ayrılmış hali : ', trnlp.find_suffix(kelime))
  
>>> Kelime kök/gövdesi : ['oğul(isim)']
>>> Eklere ayrılmış hali : ['oğul(isim)+um(2-1. tekil kişi){içe}+un(17-Tamlama eki){içe}']
```
  
***Kelime ve kural*** tabanlı bir yapı oluşturduğumuz için çoğu zaman birden fazla sonuç dönecektir. Örneğin;
  
``` python
import trnlp
kelime = Ceb('aldım')
print('Kelime kök/gövdesi : ', trnlp.find_stems(kelime))
print('Eklere ayrılmış hali : ', trnlp.find_suffix(kelime))
  
>>> Kelime kök/gövdesi : ['al(isim)', 'al(fiil)']
>>> Eklere ayrılmış hali : ['al(sıfat)+dı(Hikaye){iefe-2}+m(1. Tekil Kişi){iefe-9}', 
                            'al(isim)+dı(Hikaye){iefe-2}+m(1. Tekil Kişi){iefe-9}', 
                            'al(fiil)+dı(Bilinen Geçmiş Zaman){fçe-1}+m(1. tekil kişi){fçe-24}']

```

### Parçalama(Tokenize) :

``` python
import trnlp

yazi = """Power point sunumunu print out yapıp hard copy’sini almış olalım. 
O kadar strong process var ki outsource yapmak must oldu."""
# Bu cümleyi kuran arkadaşın maksadını hala anlayabilmiş değilim!

print(trnlp.token(yazi))

>>> ['Power', 'point', 'sunumunu', 'print', 'out', 'yapıp', 'hard', 'copy', '’', 'sini', 'almış', 'olalım', '.', '\\n', 'O', 
    'kadar', 'strong', 'process', 'var', 'ki', 'outsource', 'yapmak', 'must', 'oldu', '.']

print(trnlp.word_tokenize(yazi))

>>> ['Power', 'point', 'sunumunu', 'print', 'out', 'yapıp', 'hard', 'copy', 'sini', 'almış', 'olalım', 'O', 'kadar', 'strong', 
    'process', 'var', 'ki', 'outsource', 'yapmak', 'must', 'oldu']

print(trnlp.unknown_words(yazi))

>>> ['Power', 'point', 'print', 'out', 'hard', 'copy', 'strong', 'process', 'outsource', 'must']
```

### Cümle Bulma ve İşaretleme:

Bu kısmı halen geliştirmekteyim. Şu andaki durumu şu şekilde;

``` python
import trnlp

cumle = """Saçma ve Gereksiz Bir Yazı
    Bakkaldan 5 TL'lik 2 çikola-
    ta al. 12.02.2018 tarihinde saat tam 15:45'te yap-
    malıyız bu işi. Tamam mı? Benimle esatmahmutbayol@gmail.com 
    adresinden iletişime geçebilirsin. Yarışta 1. oldu. Doç. Dr. 
    Esat Bayol'un(Böyle bir ünvanım yok!) yanından geliyorum.
    12 p.m. mi yoksa 12 a.m. mi? 100 milyon insan gelmiş! www.deneme.com.tr 
    adresinden sitemizi inceleyebilirsin. 24 Eylül 2018 Pazartesi günü ge-
    lecekmiş."""

trnlp.print_list_item(trnlp.sentence_token(cumle))

>>> Saçma ve Gereksiz Bir Yazı
>>> Bakkaldan 5 TL 'lik 2 çikolata al.
>>> 12.02.2018 tarihinde saat tam 15:45 'te yapmalıyız bu işi.
>>> Tamam mı?
>>> Benimle esatmahmutbayol@gmail.com adresinden iletişime geçebilirsin.
>>> Yarışta 1. oldu.
>>> Doç. Dr. Esat Bayol'un (Böyle bir ünvanım yok!) yanından geliyorum.
>>> 12 p.m. mi yoksa 12 a.m. mi?
>>> 100 milyon insan gelmiş!
>>> www.deneme.com.tr adresinden sitemizi inceleyebilirsin.
>>> 24 Eylül 2018 Pazartesi günü gelecekmiş.

trnlp.print_list_item(trnlp.sentence_token_wsign(cumle))

>>> {AB}Saçma ve Gereksiz Bir Yazı{/AB}
>>> {CÜMLE} Bakkaldan {PARA}5 TL{/PARA} 'lik {SAYI}2{/SAYI} çikolata al. {/CÜMLE}
>>> {CÜMLE} {TARİH F1}12.02.2018{/TARİH F1} tarihinde saat tam {SAAT F2}15:45{/SAAT F2} 'te yapmalıyız bu işi. {/CÜMLE}
>>> {CÜMLE} Tamam mı? {/CÜMLE}
>>> {CÜMLE} Benimle {EPOSTA}esatmahmutbayol@gmail.com{/EPOSTA} adresinden iletişime geçebilirsin. {/CÜMLE}
>>> {CÜMLE} Yarışta {INCI}1.{/INCI} oldu. {/CÜMLE}
>>> {CÜMLE} {KISALTMA}Doç.{/KISALTMA} {KISALTMA}Dr.{/KISALTMA} Esat Bayol'un {AÇIKLAMA}(Böyle bir ünvanım yok!){/AÇIKLAMA} yanından geliyorum. {/CÜMLE}
>>> {CÜMLE} {SAAT F4}12 p.m.{/SAAT F4} mi yoksa {SAAT F3}12 a.m.{/SAAT F3} mi? {/CÜMLE}
>>> {CÜMLE} {SAYI}100{/SAYI} {SAYI}milyon{/SAYI} insan gelmiş! {/CÜMLE}
>>> {CÜMLE} {WEB ADRES F2}www.deneme.com.tr{/WEB ADRES F2} adresinden sitemizi inceleyebilirsin. {/CÜMLE}
>>> {CÜMLE} {TARİH F2}24 Eylül 2018{/TARİH F2} Pazartesi günü gelecekmiş. {/CÜMLE}
>>> {CÜMLE}{/CÜMLE}
```

### Heceleme :

``` python
import trnlp

trnlp.spellword('deneme')

>>> ['de', 'ne', 'me']

Bazı deneme sonuçlarını inceleyebilirsiniz :

Kelime :  araba   Heceler :  ['a', 'ra', 'ba']
Kelime :  biçimine   Heceler :  ['bi', 'çi', 'mi', 'ne']
Kelime :  insanın   Heceler :  ['in', 'sa', 'nın']
Kelime :  karaca   Heceler :  ['ka', 'ra', 'ca']
Kelime :  aldı   Heceler :  ['al', 'dı']
Kelime :  birlik   Heceler :  ['bir', 'lik']
Kelime :  sevmek   Heceler :  ['sev', 'mek']
Kelime :  altlık   Heceler :  ['alt', 'lık']
Kelime :  türkçe   Heceler :  ['türk', 'çe']
Kelime :  korkmak   Heceler :  ['kork', 'mak']
Kelime :  bandrol   Heceler :  ['band', 'rol']
Kelime :  kontrol   Heceler :  ['kont', 'rol']
Kelime :  sürpriz   Heceler :  ['sürp', 'riz']
Kelime :  program   Heceler :  ['prog', 'ram']
Kelime :  başöğretmen   Heceler :  ['ba', 'şöğ', 'ret', 'men']
Kelime :  ilkokul   Heceler :  ['il', 'ko', 'kul']
Kelime :  karaosmanoğlu   Heceler :  ['ka', 'ra', 'os', 'ma', 'noğ', 'lu']
Kelime :  krampları   Heceler :  ['kramp', 'la', 'rı']
```

### Türkçe Karakter Dönüşümü :

``` python
import trnlp

yazi = """Sabahin erken saatlerinde gunes nasil da gozumu aliyor!"""

print(trnlp.deascii(yazi))

>>> Sabahın erken saatlerinde güneş nasıl da gözümü alıyor!
```

### İstatistik :
  
``` python
import trnlp

yazi = """
Türkçe karakterler 'ş, ı, ö, ç, ğ, ü' kullanmadan yazılmış yazıları 
doğru Türkçe karakter karşılıkları ile değiştirmek için Doç. Dr. Deniz
Yüret'in geliştirdiği altyapıyı kullanan ve Emre Sevinç tarafından 
Python koduna çevrilmiş https://github.com/emres/turkish-deasciifier 
adresindeki kod kullanılabilir. 

Türkçe Tümcelerin Yüklem Odaklı Anlam Ve Dilbilgisi Çözümlemesi
Çalışmamız tümcelerin anlamsal ve dilbilgisi çözümlemesini içermek-
tedir. Tümcenin anlamsal ve dilbilgisi açısından çözümlenmesi Doğal 
Dil İşleme (DDİ)’nin ana konulardan biridir. Ayrıca yüklem, o tüm-
cenin hangi öbeklerden oluşabileceği konusunda da belirleyicidir. 
örneğin, "büyümek'' yüklemi tümce içinde nesne almazken, "-de'' e-
kiyle biten dolaylı tümleç öbeğini alır. Örneğin "Ayşeyi büyüdü.'' 
tümcesi sorunluyken, "Sokakta büyüdü.'' tümcesi doğrudur.
URL: http://hdl.handle.net/11527/12366
"""
print(trnlp.view_statistic(yazi))

    Yazının İstatistiksel Bilgileri :
    ------------------------------------------
    Toplam Satır Sayısı .....................: 15
    Toplam Boş Satır Sayısı .................: 1 / frq : %6.666666666666667 (Toplam Satır Sayısına Göre)
    Toplam Yazılı Satır Sayısı ..............: 14 / frq : %93.33333333333333 (Toplam Satır Sayısına Göre)
    ------------------------------------------
    Toplam Kelime Sayısı ....................: 114
    Tekrarsız Kelime Sayısı..................: 106
    En Çok Tekrarlanan ilk 5 Kelime .........: [('Türkçe', 3, 2.6315789473684212), ('ve', 3, 2.6315789473684212), ('dilbilgisi', 2, 1.7543859649122806), ('anlamsal', 2, 1.7543859649122806), ('tümcesi', 2, 1.7543859649122806)]
    ------------------------------------------
    Tüm Karakterin Sayısı ...................: 878
    Boşluk Karakteri Sayısı .................: 95 / frq : %10.82004555808656 (Tüm Karakterin Sayısına Göre)
    Toplam Rakam Sayısı .....................: 10 / frq : %1.1389521640091116 (Tüm Karakterin Sayısına Göre)
    Rakamların Listesi ......................: [('1', 3, 0.3416856492027335), ('6', 2, 0.22779043280182232), ('2', 2, 0.22779043280182232), ('3', 1, 0.11389521640091116), ('7', 1, 0.11389521640091116), ('5', 1, 0.11389521640091116)]
    Özel Karakterlerin Sayısı ...............: 31 / frq : %3.530751708428246 (Tüm Karakterin Sayısına Göre)
    Özel Karakterlerin Listesi...............: [(',', 9, 1.0250569476082005), ('.', 8, 0.9111617312072893), ('', 5, 0.5694760820045558), ("'", 5, 0.5694760820045558), ('-', 3, 0.3416856492027335), (':', 1, 0.11389521640091116)]
    ------------------------------------------
    Tüm Harflerin Sayısı ....................: 703 / frq : %80.06833712984054 (Tüm Karakterin Sayısına Göre)
    Sesli Harflerin Sayısı ..................: 287 / frq : %40.82503556187767 (Tüm Harflerin Sayısına Göre)
    Sesli Harflerin Listesi .................: [('e', 72, 8.200455580865604), ('i', 69, 7.85876993166287), ('a', 53, 6.0364464692482915), ('ü', 27, 3.075170842824601), ('ı', 20, 2.277904328018223), ('o', 15, 1.7084282460136675), ('u', 15, 1.7084282460136675), ('ö', 7, 0.7972665148063781), ('A', 3, 0.3416856492027335), ('İ', 2, 0.22779043280182232), ('O', 1, 0.11389521640091116), ('U', 1, 0.11389521640091116), ('Ö', 1, 0.11389521640091116), ('E', 1, 0.11389521640091116)]
    Sessiz Harflerin Sayısı .................: 416 / frq : %59.17496443812233 (Tüm Harflerin Sayısına Göre)
    Sessiz Harflerin Listesi ................: [('l', 56, 6.378132118451025), ('n', 50, 5.694760820045558), ('r', 41, 4.669703872437358), ('m', 33, 3.7585421412300684), ('k', 31, 3.530751708428246), ('d', 30, 3.416856492027335), ('t', 24, 2.733485193621868), ('s', 19, 2.164009111617312), ('y', 17, 1.9362186788154898), ('ç', 14, 1.5945330296127562), ('b', 14, 1.5945330296127562), ('c', 12, 1.366742596810934), ('ğ', 10, 1.1389521640091116), ('ş', 10, 1.1389521640091116), ('h', 8, 0.9111617312072893), ('z', 8, 0.9111617312072893), ('D', 8, 0.9111617312072893), ('g', 6, 0.683371298405467), ('v', 5, 0.5694760820045558), ('T', 5, 0.5694760820045558), ('p', 3, 0.3416856492027335), ('Ç', 2, 0.22779043280182232), ('Y', 2, 0.22779043280182232), ('S', 2, 0.22779043280182232), ('f', 2, 0.22779043280182232), ('V', 1, 0.11389521640091116), ('R', 1, 0.11389521640091116), ('P', 1, 0.11389521640091116), ('L', 1, 0.11389521640091116)]
    ------------------------------------------
    Büyük Harflerin Sayısı ..................: 32 / frq : %4.551920341394026 (Tüm Harflerin Sayısına Göre)
    Büyük Harfle Başlayan Kelimelerin Sayısı : 26 / frq : %22.80701754385965 (Toplam Kelime Sayısına Göre)
    Büyük Harfli ilk 5 Kelime ...............: [('Türkçe', 3, 11.538461538461538), ('Ayşeyi', 1, 3.8461538461538463), ('İşleme', 1, 3.8461538461538463), ('Tümcenin', 1, 3.8461538461538463), ('Çalışmamız', 1, 3.8461538461538463)]
    Küçük Harflerin Sayısı ..................: 671 / frq : %95.44807965860598 (Tüm Harflerin Sayısına Göre)
 ```
 
 ### Sayıyı Yazıya ya da Yazıyı Sayıya Dönüştürme :
 
 ``` python
import trnlp

sayi = '1001587'

sayidan_yaziya_cevrilmis = trnlp.ntow(sayi)
print(sayidan_yaziya_cevrilmis)

>>> birmilyon bin beşyüzseksenyedi 

yazidan_sayiya_cevrilmis = trnlp.wton(sayidan_yaziya_cevrilmis)
print(yazidan_sayiya_cevrilmis)

>>> 1001587
 ```
 
Nihai amacım ***cümle analizi*** yapabilmek olacaktır.
  
### Projenin İçeriği :
  
- Sözlük hazırlanması. (Yapıldı. Data klasörünün içinde sozluk_tekli.txt dosyası sözlük bilgilerini içerir.)
- Heceleme algoritması (Yapıldı. Auxiliary/TurkishGrammer.py içinde spellword fonksiyonu kullanılabilir durumda.)
- Türkçe ses uyumları kontrolü (Yapıldı. Auxiliary/TurkishGrammer.py içinde ses uyumu fonksiyonları var.)
- Kelime bazlı kök/gövde ve eklerin bulunması (Yapıldı. Morphological/MorphologicalLR.py ClsEkBul klası kullanılabilir durumda.)
- Cümle ayırma. (Basit bir şey yaptım fakat daha yayınlamadım. Bir kaç testten sonra paylaşacağım.) - Eklendi.
- Yazı istatistiği (Bu kısımla da ilgili bir çalışmam var. Biraz düzenledikten sonra yayınlayacağım.) - Eklendi.
- Yanlış yazılan kelimelerin bulunması ve doğru yazımına dair öneride bulunulması yada otomatik olarak düzeltilmesi.
- Cümle analizi yapılması ve cümlenin öğelerine ayrılması.

### İletişim :
esatmahmutbayol@gmail.com
