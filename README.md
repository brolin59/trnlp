# PYTHON TURKÇE DOĞAL DİL İŞLEME - TURKISH NLP
## TÜRKÇE İÇİN DOĞAL DİL İŞLEME ARAÇLARI
  
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
from Morphological.MorphologicalLR import ClsEkBul as cb
kelime = cb.('oğlumun')
print('Kelime kök/gövdesi : ', kelime.stems)
print('Eklere ayrılmış hali : ', kelime.result)
  
Kelime kök/gövdesi : ['oğul(isim)']
Eklere ayrılmış hali : ['oğul(isim)+um(2-1. tekil kişi){içe}+un(17-Tamlama eki){içe}']
```
  
***Kelime ve kural*** tabanlı bir yapı oluşturduğumuz için çoğu zaman birden fazla sonuç dönecektir. Örneğin;
  
``` python
from Morphological.MorphologicalLR import ClsEkBul as cb
kelime = cb.('aldım')
print('Kelime kök/gövdesi : ', kelime.stems)
print('Eklere ayrılmış hali : ', kelime.result)
  
Kelime kök/gövdesi : ['al(isim)', 'al(fiil)']
Eklere ayrılmış hali : ['al(fiil)+dı(1-Bilinen Geçmiş Zaman){fçe}+m(26-1. tekil kişi){fçe}', 'al(isim)+dı(2-Hikaye){iefe}+m(9-1. tekil kişi){iefe}']
```
  
### SentenceTokenization.py
  
Kural tabanlı çalışan basit bir cümle bulma algoritmasıdır. Halen geliştirme aşamasında olduğum için aklımdaki birkaç özelliği eksik şu anda. Yine de birçok dökümanda iş görür diye düşünüyorum. Örnek kodu ve sonucu aşağıdaki gibidir.
  
``` python
from Tokenization.SentenceTokenization import cumle_ayir as ca
from Auxiliary.AuxiliaryCommands import print_list_item

yazi = """
Türkçe Tümcelerin Yüklem Odaklı Anlam Ve Dilbilgisi Çözümlemesi
Çalışmamız tümcelerin anlamsal ve dilbilgisi çözümlemesini içermek-
tedir. Tümcenin anlamsal ve dilbilgisi açısından çözümlenmesi Doğal 
Dil İşleme (DDİ)’nin ana konulardan biridir. Ayrıca yüklem, o tüm-
cenin hangi öbeklerden oluşabileceği konusunda da belirleyicidir. 
örneğin, "büyümek'' yüklemi tümce içinde nesne almazken, "-de'' e-
kiyle biten dolaylı tümleç öbeğini alır. Örneğin "Ayşeyi büyüdü.'' 
tümcesi sorunluyken, "Sokakta büyüdü.'' tümcesi doğrudur.
URL: http://hdl.handle.net/11527/12366
Dönmez, İlknur
"""
yazi = ca(yazi)
print_list_item(yazi)
```
  
Kodun çıktısı şu şekildedir:
  
*Türkçe Tümcelerin Yüklem Odaklı Anlam Ve Dilbilgisi Çözümlemesi:  
Çalışmamız tümcelerin anlamsal ve dilbilgisi çözümlemesini içermektedir.  
Tümcenin anlamsal ve dilbilgisi açısından çözümlenmesi Doğal Dil İşleme (DDİ) 'nin ana konulardan biridir.  
Ayrıca yüklem, o tümcenin hangi öbeklerden oluşabileceği konusunda da belirleyicidir.  
örneğin, "büyümek" yüklemi tümce içinde nesne almazken, "-de" ekiyle biten dolaylı tümleç öbeğini alır.  
Örneğin "Ayşeyi büyüdü." tümcesi sorunluyken, "Sokakta büyüdü." tümcesi doğrudur.  
URL:  
http://hdl.handle.net/11527/12366  
Dönmez, İlknur*  
  
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
