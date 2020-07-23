# TRNLP(***TR Natural Language Processing***)
Türkçe Doğal dil işleme Python kütüphanesi

Klasör yapısı ve kullanılabilecek tüm komutlar için [Türkçe Doğal Dil işleme Wiki sayfasını inceleyebilirsiniz.](https://github.com/brolin59/PHYTON-TURKCE-DOGAL-DIL-ISLEME---TURKISH-NLP/wiki)

### İletişim :
trnlp2020@gmail.com

### Proje Sponsoru:
[Patreon](https://www.patreon.com/trnlp)

### Kurulum :

```$ pip install trnlp```

ya da;

trnlp klasörünü Python'un kurulu olduğu dizin içerisinde `\Lib\site-packages\` dizininin içine kopyalamanız yeterlidir.

Kod ve dilbilgisi kuralları ile ilgili yaptığım yanlışlar için öneri ve uyarılarınızı bekliyorum.

trnlp GNU Genel Kamu Lisansı v3.0 ile lisanslanmıştır. Yani kısaca Lisans ve telif hakkı bildirimi yapılması, kodda yapılan değişikliklerin belgelendirilmesi, kaynak kodunun açık ve kullanılabilir olması ve aynı lisans altında yayınlanması şartları ile her şekilde kullanımı serbesttir ve yazılım ile ilgili hiçbir garanti verilmez. Gerekli tüm bilgiler zaten LICENSE.txt dosyasında ayrıntılı bir şekilde yazılmıştır.

Eminim bu konularda bilgisi benden çok daha iyi olan arkadaşlar bu paylaşımları bir üst seviyeye çıkarmamda bana yardımcı olabilirler. 
Hobi olarak başladığım bu projenin faydalı olması dileği ile...

* [Kelime kök ve gövdesi bulma (Base, stem)](https://github.com/brolin59/PYTHON-TURKCE-DOGAL-DIL-ISLEME-TURKISH-NLP/wiki/2.-Morfolojik-Analiz)
* [Kelime ve kural tabanlı morfolojik analiz (Lemmatization)](https://github.com/brolin59/PYTHON-TURKCE-DOGAL-DIL-ISLEME-TURKISH-NLP/wiki/2.-Morfolojik-Analiz)
* [Yanlış ya da Ascii karakterler kullanılarak yazılan kelimeler için öneri listesi (Spelling Corrector)](https://github.com/brolin59/PYTHON-TURKCE-DOGAL-DIL-ISLEME-TURKISH-NLP/wiki/5.-Kelime-Kontrol%C3%BC)
* [Metin parçalama ve sayma işlemleri (Tokenization)](https://github.com/brolin59/PYTHON-TURKCE-DOGAL-DIL-ISLEME-TURKISH-NLP/wiki/3.-Par%C3%A7alama-(Tokenization))
* [Faydalı olabilecek ek fonksiyonlar.(levenshtein_distance, number_to_word, word_to_number vb.)](https://github.com/brolin59/PYTHON-TURKCE-DOGAL-DIL-ISLEME-TURKISH-NLP/wiki/4.-Ek-Fonksiyonlar)


trnlp her işlem için bir sözlüğe ihtiyaç duyar. trnlp'yi indirdiğinizde bu sözlüklerde beraberinde gelmiş olacaktır. Şu an için sözlüklerde bir değişiklik yapma ya da sözlüğe ekleme yapma özelliği bulunmamaktadır. Tüm sözlükler .pickle dosyası olarak kaydedilmiş ve erişime açıktır. Gelecek versiyonda sözlüğe veri ekleme özelliğini de eklemeyi düşünüyorum. Yine de gerekli sözlük formatına bağlı kalmak kaydı ile manuel değişiklikler yapılabilir.

Her bölüm için ayrıntılı anlatımlar ilgili wiki sayfasında mevcuttur.

Benim bilgisayarımda (İntel i5-2450M işlemci 4GB Bellek) kelime uzunluklarına bağlı olarak 1 saniyede yapılabilen analiz sayısı 2250 ile 3000 arasında değişmektedir.

### Proje İlerlemesi:
  
- [x] Sözlük hazırlanması (Testler sırasında düzenlemeler yapılacak)
- [x] Heceleme algoritması.
- [x] Türkçe ses uyumları kontrolü.
- [x] Kelime bazlı kök/gövde ve eklerin bulunması (Testler sırasında düzenlemeler yapılacak).
- [x] Cümle ayırma. (Testler sırasında düzenlemeler yapılacak).
- [x] Yanlış yazılan kelimelerin bulunması ve doğru yazımına dair öneride bulunulması ya da otomatik olarak düzeltilmesi (Testler sırasında düzenlemeler yapılacak).
- [ ] Eklerin ve ek kontrollerinin düzeltilmesi.
- [x] Paket oluşturma (Testler sırasında düzenlemeler yapılacak).
- [ ] Cümle analizi yapılması ve cümlenin öğelerine ayrılması.

### Sıkça Sorulan Sorular :

* Morfolojik analizde aradığım sonuç tüm analizler içerisinde olmasına rağmen tek sonuç istediğimde farklı çözüm yapıyor. Bunun sebebi nedir?

Türkçenin yapısından dolayı bir kelime için, ek almış ya da almamış olsun, birden fazla çözümleme yapılabilmektedir. Örneğin "kanat" kelimesini değerlendirirsek;

```python
from trnlp import TrnlpWord

obj = TrnlpWord()
obj.setword("kanat")

for analiz in obj.get_inf:
    print(writeable(analiz))
        
>> kanat(isim)
   Kanat(özel) # TDK'ya göre erkek ismi
   kan(isim)+a{İf}[5_17]+t{Ff}[6_8] # -a isimden fiil yapma eki bir süreliğine eklerden çıkarıldı. Şu anda analiz sonucu "kana(fiil)+t{Ff}[6_8]" şeklinde dönecektir.
   
print(obj)

>> kan(isim)+a{İf}[5_17]+t{Ff}[6_8]
   
```

Üç çözüm de doğrudur. "print(obj)" dediğimizde tek sonuç döndürmesini hedeflediğimiz için aralarından bir tanesini seçmek zorundayız. trnlp belirli kriterler çerçevesinde bir seçim yaparak tek sonucu döndürür. Sizin elde etmek istediğiniz sonuç `"kanat(isim)"` olsa da trnlp `kan(isim)+a{İf}[5_17]+t{Ff}[6_8]` sonucunu döndürecek ve kelimenin kökünü `"kan"`, kök türünü `"isim"`, gövdesini `"kanat"` ve gövde türünü `"fiil"` olarak döndürecektir. 

* Kriterlerimizi tam tersine çevirsek ve önceliği fiillere değil de isimlere versek olmaz mı?

Bu durumda yukarıda bahsettiğim sonucun tersi yaşanacağından yine çözüm sağlanamayacaktır. Bu sefer de "kanat-" fiilini bulmak isteyen bir kişi için yanlış sonuç dönmüş olacaktır. Bunun tek çözümü cümle analizi yapabilmek ve kelimeyi cümle içerisindeki görevine göre tahlil etmek olacaktır.
