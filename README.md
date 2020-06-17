# PYTHON TÜRKÇE DOĞAL DİL İŞLEME - TURKISH NLP

## TÜRKÇE İÇİN DOĞAL DİL İŞLEME ARAÇLARI

Klasör yapısı ve kullanılabilecek tüm komutlar için [Türkçe Doğal Dil işleme Wiki sayfasını inceleyebilirsiniz.](https://github.com/brolin59/PHYTON-TURKCE-DOGAL-DIL-ISLEME---TURKISH-NLP/wiki)

***trnlp klasörünü Python'un kurulu olduğu dizin içerisinde \Lib\site-packages\ dizininin içine kopyalamanız yeterlidir.*** Kısa süre içerisinde paket haline gitirlecektir.

Ne Python ne de Türkçe dilbigim çok iyi olmamasına rağmen ***hobi*** olarak yazdığım birkaç kodu sizlerle paylaşmak istedim. ***Kod ve dilbilgisi kuralları ile ilgili yaptığım yanlışlar için öneri ve uyarılarınızı bekliyorum.*** İlk başta ilgim bir yazılım dili öğrenmek üzerineydi. Biraz araştırmadan sonra Python öğrenmeye karar verdim. Doğal dil işleme konusuna merakım ise makine öğrenmesi çalışmalarını araştırırken oluştu. Yazılım dili öğrenirken bir projeye başlamanın faydalı olacağı fikrini benimsediğim için böyle bir projeye başladım. Bu konuda yapılmış iyi çalışmalar var. Az önce de belirttiğim gibi benim niyetim kendimi geliştirmek. Yanında az da olsa birkaç kişiye faydam dokunursa ne ala...

Lisans olarak GNU Genel Kamu Lisansı v3.0 kullanmayı tercih ettim. Yani kısaca Lisans ve telif hakkı bildirimi yapılması, kodda yapılan değişikliklerin belgelendirilmesi, kaynak kodunun açık ve kullanılabilir olması ve aynı lisans altında yayınlanması şartları ile her şekilde kullanımı serbesttir ve yazılım ile ilgili hiçbir garanti verilmez. Gerekli tüm bilgiler zaten LICENSE.txt dosyasında ayrıntılı bir şekilde yazılmıştır.

Eminim bu konularda bilgisi benden çok daha iyi olan arkadaşlar bu paylaşımları bir üst seviyeye çıkarmamda bana yardımcı olabilirler. 
Hobi olarak başladığım bu işin faydalı olması dileği ile...

* Kelime kök ve gövdesi bulma (Base, stem)
* Kelime ve kural tabanlı morfolojik analiz (Lemmatization)
* Yanlış yada Ascii karakterler kullanılarak yazılan kelimeler için öneri listesi (Spelling Corrector) - Yapım aşamasında
* Metin parçalama ve sayma işlemleri (Tokenization)

trnlp her işlem için bir sözlüğe ihtiyaç duyar. trnlp'yi indirdiğinizde bu sözlüklerde beraberinde gelmiş olacaktır. Şu an için sözlüklerde bir değişiklik yapma ya da sözlüğe ekleme yapma özelliği bulunmamaktadır. Tüm sözlükler .pickle dosyası olarak kaydedilmiş ve erişime açıktır. Gelecek versiyonda sözlüğe veri ekleme özelliğini de eklemeyi düşünüyorum. Yine de gerekli sözlük formatına bağlı kalmak kaydı ile manuel değişiklikler yapılabilir.

Her bölüm için ayrıntılı anlatımlar ilgili wiki sayfasında mevcuttur.

Benim bilgisayarımda (İntel i5-2450M işlemci 4GB Bellek) kelime uzunluklarına bağlı olarak 1 saniyede yapılabilen analiz sayısı 2250 ile 3000 arasında değişmektedir.
  
***Kelime kök/gövde ve eklerini*** bulmak için yazdığım algoritmanın örnek kullanımı şu şekildedir:

``` python
from trnlp import TrnlpWord

obj = TrnlpWord()
obj.setword("arkadaşlar")
print(obj)

>> "arka(isim,sıfat)+daş{İi}[4_26]+lar{Çe}[1_1]"

obj.setword("Muvaffakiyetsizleştiricileştiriveremeyebileceklerimizdenmişsiniz")
print(obj)

>> muvaffakiyet(isim)+siz{İi}[4_4]+leş{İf}[5_5]+tir{Ff}[6_11]+ici{Fi}[7_3]+leş{İf}[5_5]+tir{Ff}[6_11]+iver{BfVer}[3_4]+eme{Ytsz}[3_19]+yebil{BfBil}[3_1]+ecek{Fs}[8_9]+ler{Çe}[1_1]+imiz{İe1ç}[1_4]+den{HeUzk}[1_23]+miş{EfGçMiş}[1_38]+siniz{EfKe2ç}[1_50]

```

``` python
from trnlp import TrnlpWord

obj = TrnlpWord()
obj.setword("arkadaşlar")
print(obj.get_base)

>> "arka"

print(obj.get_base_type)

>> "isim,sıfat"
```

``` python
from trnlp import TrnlpWord

obj = TrnlpWord()
obj.setword("arkadaşlar")
print(obj.get_stem)

>> "arkadaş"

print(obj.get_stem_type)

>> "isim"
```

### Projenin İçeriği :
  
- Sözlük hazırlanması. +
- Heceleme algoritması +
- Türkçe ses uyumları kontrolü +
- Kelime bazlı kök/gövde ve eklerin bulunması +
- Cümle ayırma. +
- Yanlış yazılan kelimelerin bulunması ve doğru yazımına dair öneride bulunulması yada otomatik olarak düzeltilmesi. (Yapım aşamasında. Kısa sürede eklenecek.)
- Paket oluşturma. (Düzeltmeler yapıldıktan sonra yapılacak.)
- Cümle analizi yapılması ve cümlenin öğelerine ayrılması.

### İletişim :
esatmahmutbayol@gmail.com
