# PYTHON TÜRKÇE DOĞAL DİL İŞLEME - TURKISH NLP

## NATURAL LANGUAGE PROCESSING TOOLS FOR TURKISH

(English translation made by google translate.)

> You can check the [Natural Language Processing Wiki page](https://github.com/brolin59/PHYTON-TURKCE-DOGAL-DIL-ISLEME---TURKISH-NLP/wiki) for the folder structure and all the commands that can be used.

It is enough to copy the TurkisNLP folder into the \Lib\site-packages\ directory in the directory where Python is installed.
  
I wanted to share with you a few codes that I wrote as ***hobby*** , although neither Python nor Turkish language is very good. In fact at first I was interested to learn a software language. After some research I decided to learn Python. My curiosity about natural language processing was when researching machine learning studies. I started a project like this because I thought that it would be useful to start a project while learning the software language. Actually, there are studies on this subject. As I have just mentioned, my intention is to improve myself. What if a couple of people touch a little with you ...
I'm sure friends who are much better at this stuff can help me get those shares up to the next level.
I started out as a hobby and wished that this would be useful ...

### MorphologicalLR.py:
  
***MorphologicalLR dictionary and rule-based*** is an algorithm I have prepared to find the suffixes of running root / stem and lamb.
I am still in the test phase ***misses can be mistakes***. We can still say we're at work.
   
I have not identified the construction inserts for the moment. Creating the dictionary was a bit of a hassle and took a lot of time. Still missing
and the dictionary file is still in the works if it is wrong. The dictionary file is in **Data / tr_NLP.sqlite**
you can find.
  
The example usage of the algorithm I wrote to find the word stem/body and its suffixes is as follows:

``` python
from TurkishNLP import Ceb
kelime = Ceb('oğlumun')
print('Kelime kök/gövdesi : ', kelime.stems)
print('Eklere ayrılmış hali : ', kelime.result)
  
Kelime kök/gövdesi : ['oğul(isim)']
Eklere ayrılmış hali : ['oğul(isim)+um(2-1. tekil kişi){içe}+un(17-Tamlama eki){içe}']
```

We will have more than one result often because we have built a structure with ***words and rules***. For example;

``` python
from TurkishNLP import Ceb
kelime = Ceb('aldım')
print('Kelime kök/gövdesi : ', kelime.stems)
print('Eklere ayrılmış hali : ', kelime.result)
  
Kelime kök/gövdesi : ['al(isim)', 'al(fiil)']
Eklere ayrılmış hali : ['al(fiil)+dı(1-Bilinen Geçmiş Zaman){fçe}+m(26-1. tekil kişi){fçe}', 'al(isim)+dı(2-Hikaye){iefe}+m(9-1. tekil kişi){iefe}']
```

### SentenceTokenization.py
  
It is a simple rule-based sentence matching algorithm. Now that I'm in the development phase, I'm missing a few features in my mind. Nevertheless, I think it will work in many dumps. The sample code and the result is as follows.

``` python
from TurkishNLP import cumle_ayir as ca

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
yazi = ca(yazi)
print(yazi)
```

Each item in the list represents a line. The output of the code is as follows

``` python
["Türkçe karakterler 'ş, ı, ö, ç, ğ, ü' kullanmadan yazılmış yazıları doğru Türkçe karakter karşılıkları ile değiştirmek için Doç. Dr. Deniz Yüret'in geliştirdiği altyapıyı kullanan ve Emre Sevinç tarafından Python koduna çevrilmiş https://github.com/emres/turkish-deasciifier adresindeki kod kullanılabilir.",  
'Türkçe Tümcelerin Yüklem Odaklı Anlam Ve Dilbilgisi Çözümlemesi:',  
'Çalışmamız tümcelerin anlamsal ve dilbilgisi çözümlemesini içermektedir.',  
"Tümcenin anlamsal ve dilbilgisi açısından çözümlenmesi Doğal Dil İşleme (DDİ) 'nin ana konulardan biridir.",  
'Ayrıca yüklem, o tümcenin hangi öbeklerden oluşabileceği konusunda da belirleyicidir.',  
'örneğin, "büyümek" yüklemi tümce içinde nesne almazken, "-de" ekiyle biten dolaylı tümleç öbeğini alır.',  
'Örneğin "Ayşeyi büyüdü." tümcesi sorunluyken, "Sokakta büyüdü." tümcesi doğrudur.',  
'URL:',  
'http://hdl.handle.net/11527/12366']  
```
My ultimate goal is to be able to do *** sentence analysis ***.
  
### Project Content:
  
- Dictionary preparation. (Contains the glossary_text.txt file dictionary information in the Data folder.)
- Spelling algorithm (done in Auxiliary / SpellWord function available in TurkishGrammer.py).
- English audio compliance check (done in Auxiliary / TurkishGrammer.py with audio compatibility functions)
- Word based root / stem and attachment (Morphological / MorphologicalLR.py ClsEkBulk is available.)
- Sentence separation. (I did something simple, but I have not posted it yet, so I'll share it after a few tests.) - Added.
- Text statistic (I have a study on this part, I will post it after editing a bit.) - Added.
- Finding misspelled words and correcting for correct spelling suggestions.
- Sentence analysis and censorship of the items to be separated.

### Ideas:
  
* The SentenceTokenization.py file I wrote for sentence separation works with rule-based and simple logic. I think that sentence analysis and sentence separation algorithm should work integrated. In other words, with sentence analysis, it is more logical to distinguish each of the sentences in a text. To simplify a complex sentence structure into multiple sentences.

* Finding misspelled words:
Situation Analysis:
By examining a word in two parts as a stem / body and appendages, the misspelling can be at the root / stem attachment part. Yada may be wrong in both parts. In this case, it seems that we need to evaluate the root and supplements separately. In this case the following question arises:
"How do we distinguish between the root and attachments of a misspelled belly?"
The MorphologicalLR.py algorithm I wrote at this point is correct in a big way, provided that the pen is written correctly. I can not get a misspelled word into the root and its suffixes with the same algorithm. If we can not get a return on the result of this algorithm, we can just say that the word is misspelled.

* Solution ideas for correcting misspelled words:
It is obvious that your first problem will be the prediction of a root and appendages of a misspelled word. Perhaps machine learning can be done in this way with statistics. There is also basic knowledge about these two subjects. I can get help from more professional friends.

Even if it is misspelled, if we can separate a word into a misspelled root and suffixes, we can reach the "right word" by introducing a correct sequence of suffixes with a root-based approach with a proximity algorithm after this step.

For example, suppose that the word "fridge" is written as "from the fridge".

* Estimated root part: "bzdolpa"
* Estimated additional part: "dan"

If we can make the above estimates and arrive at the root of the "refrigerator" with the affinity algorithm, we can find that it must be in the form of "after" with a rule-based addition algorithm. So we can come to the conclusion that the correct writing should be "from the fridge". In some cases more than one result may be returned.

### Contact :
esatmahmutbayol@gmail.com

***

## TÜRKÇE İÇİN DOĞAL DİL İŞLEME ARAÇLARI
  
Klasör yapısı ve kullanılabilecek tüm komutlar için [Türkçe Doğal Dil işleme Wiki sayfasını inceleyebilirsiniz.](https://github.com/brolin59/PHYTON-TURKCE-DOGAL-DIL-ISLEME---TURKISH-NLP/wiki)

> You can check the [Turkish Natural Language Processing Wiki page](https://github.com/brolin59/PHYTON-TURKCE-DOGAL-DIL-ISLEME---TURKISH-NLP/wiki) for the folder structure and all the commands that can be used.

TurkisNLP klasörünü Python'un kurulu olduğu dizin içerisinde \Lib\site-packages\ dizinin içine kopyalamanız yeterlidir.
  
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
from TurkishNLP import Ceb
kelime = Ceb('oğlumun')
print('Kelime kök/gövdesi : ', kelime.stems)
print('Eklere ayrılmış hali : ', kelime.result)
  
Kelime kök/gövdesi : ['oğul(isim)']
Eklere ayrılmış hali : ['oğul(isim)+um(2-1. tekil kişi){içe}+un(17-Tamlama eki){içe}']
```
  
***Kelime ve kural*** tabanlı bir yapı oluşturduğumuz için çoğu zaman birden fazla sonuç dönecektir. Örneğin;
  
``` python
from TurkishNLP import Ceb
kelime = Ceb('aldım')
print('Kelime kök/gövdesi : ', kelime.stems)
print('Eklere ayrılmış hali : ', kelime.result)
  
Kelime kök/gövdesi : ['al(isim)', 'al(fiil)']
Eklere ayrılmış hali : ['al(fiil)+dı(1-Bilinen Geçmiş Zaman){fçe}+m(26-1. tekil kişi){fçe}', 'al(isim)+dı(2-Hikaye){iefe}+m(9-1. tekil kişi){iefe}']
```
  
### SentenceTokenization.py
  
Kural tabanlı çalışan basit bir cümle bulma algoritmasıdır. Halen geliştirme aşamasında olduğum için aklımdaki birkaç özelliği eksik şu anda. Yine de birçok dökümanda iş görür diye düşünüyorum. Örnek kodu ve sonucu aşağıdaki gibidir.
  
``` python
from TurkishNLP import cumle_ayir as ca

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
yazi = ca(yazi)
print(yazi)
```
  
Listenin her bir öğesi bir satırı ifade eder. Kodun çıktısı şu şekildedir:
``` python
["Türkçe karakterler 'ş, ı, ö, ç, ğ, ü' kullanmadan yazılmış yazıları doğru Türkçe karakter karşılıkları ile değiştirmek için Doç. Dr. Deniz Yüret'in geliştirdiği altyapıyı kullanan ve Emre Sevinç tarafından Python koduna çevrilmiş https://github.com/emres/turkish-deasciifier adresindeki kod kullanılabilir.",  
'Türkçe Tümcelerin Yüklem Odaklı Anlam Ve Dilbilgisi Çözümlemesi:',  
'Çalışmamız tümcelerin anlamsal ve dilbilgisi çözümlemesini içermektedir.',  
"Tümcenin anlamsal ve dilbilgisi açısından çözümlenmesi Doğal Dil İşleme (DDİ) 'nin ana konulardan biridir.",  
'Ayrıca yüklem, o tümcenin hangi öbeklerden oluşabileceği konusunda da belirleyicidir.',  
'örneğin, "büyümek" yüklemi tümce içinde nesne almazken, "-de" ekiyle biten dolaylı tümleç öbeğini alır.',  
'Örneğin "Ayşeyi büyüdü." tümcesi sorunluyken, "Sokakta büyüdü." tümcesi doğrudur.',  
'URL:',  
'http://hdl.handle.net/11527/12366']  
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
  
### Fikirler :
  
* Cümle ayırma için yazdığım SentenceTokenization.py dosyası kural tabanlı ve basit bir mantık ile çalışır durumda. Cümle analizi ile cümle ayırma algoritmasının entegre çalışması gerektiğini düşünüyorum. Yani cümle analizi ile bir yazı metni içerisindeki yan cümleler de tespit edilerek her birinin ayrılması daha mantıklı geliyor. Bir nevi karmaşık cümle yapılarını birden fazla cümleler haline getirerek basitleştirmek diyebileriz.

* Yanlış yazılan kelimelerin bulunması:
Durum Analizi:
Bir kelimeyi kök/gövde ve ekler olarak iki kısımda incelersek, yazım hatası kök/gövde yada ekler kısmında olabilir. Yada her iki kısımda da yazım yanlışı olabilir. Bu durumda yapmamız gereken kök ve ekler kısmını ayrı değerlendirmek gibi görünüyor. Bu durumda da şu soru akla geliyor: 
"Peki yanlış yazılmış bir kelimenin kök ve ekler kısmını nasıl ayırt edeceğiz?"
Şu anda yazmış olduğum MorphologicalLR.py algoritması büyük oranda doğru sonuç veriyor fakat kelimenin tam olarak doğru yazılması şartıyla. Yanlış yazılmış bir kelimeyi aynı algoritma ile kök ve eklerine ayıramam. Bu algoritma sonucunda bir geri dönüş alamazsak kelime yanlış yazılmış diyebiliriz sadece. 

* Yanlış yazılan kelimelerin düzeltilmesi için çözüm fikirleri: 
İlk sorunumuzun yanlış yazılmış bir kelimenin kök ve eklerinin tahmin edilmesi olacağı ortada. Belki makine öğrenmesi yada istatistik ile bu şekilde bir tahmin yapılabilir. Bu iki konu hakkında da temel düzeyde bilgim var. Daha profesyönel arkadaşlardan yardım alabilirim.

Yanlış yazılmış olsa da bir kelimeyi yanlış yazılmış haldeki kökü ve eklerine ayırabilirsek bu aşamadan sonrasında yakınlık algoritması ile kökü, kural tabanlı bir yaklaşım ile ekleri doğru dizilime getirerek "doğru kelime"ye ulaşabiliriz.

Örneğin "buzdolabından" kelimesinin "bzdolabıdan" şeklinde yazıldığını düşünelim.

* Tahmin edilen kök kısmı : "bzdolabı"
* Tahmin edilen ek kısmı : "dan"

Yukarıdaki tahminleri yapabildiysek ve yakınlık algoritması ile "buzdolabı" köküne ulaştıysak kural tabanlı bir ek ekleme algoritması ile devamında "ndan" şeklinde olması gerektiğini bulabiliriz. Böylece doğru yazımın "buzdolabından" olması gerektiği sonucuna varabiliriz. Bazı durumlarda birden fazla sonuç dönebilir.

### İletişim :
esatmahmutbayol@gmail.com
