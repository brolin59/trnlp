# PYTHON TÜRKÇE DOĞAL DİL İŞLEME - TURKISH NLP

## TÜRKÇE İÇİN DOĞAL DİL İŞLEME ARAÇLARI

Klasör yapısı ve kullanılabilecek tüm komutlar için [Türkçe Doğal Dil işleme Wiki sayfasını inceleyebilirsiniz.](https://github.com/brolin59/PHYTON-TURKCE-DOGAL-DIL-ISLEME---TURKISH-NLP/wiki)

### İletişim :
trnlp2020@gmail.com

***trnlp klasörünü Python'un kurulu olduğu dizin içerisinde \Lib\site-packages\ dizininin içine kopyalamanız yeterlidir.*** Kısa süre içerisinde paket haline gitirilecektir.

Ne Python ne de Türkçe dilbigim çok iyi olmamasına rağmen ***hobi*** olarak yazdığım birkaç kodu sizlerle paylaşmak istedim. ***Kod ve dilbilgisi kuralları ile ilgili yaptığım yanlışlar için öneri ve uyarılarınızı bekliyorum.*** İlk başta ilgim bir yazılım dili öğrenmek üzerineydi. Biraz araştırmadan sonra Python öğrenmeye karar verdim. Doğal dil işleme konusuna merakım ise makine öğrenmesi çalışmalarını araştırırken oluştu. Yazılım dili öğrenirken bir projeye başlamanın faydalı olacağı fikrini benimsediğim için böyle bir projeye başladım. Bu konuda yapılmış iyi çalışmalar var. Az önce de belirttiğim gibi benim niyetim kendimi geliştirmek. Yanında az da olsa birkaç kişiye faydam dokunursa ne ala...

Lisans olarak GNU Genel Kamu Lisansı v3.0 kullanmayı tercih ettim. Yani kısaca Lisans ve telif hakkı bildirimi yapılması, kodda yapılan değişikliklerin belgelendirilmesi, kaynak kodunun açık ve kullanılabilir olması ve aynı lisans altında yayınlanması şartları ile her şekilde kullanımı serbesttir ve yazılım ile ilgili hiçbir garanti verilmez. Gerekli tüm bilgiler zaten LICENSE.txt dosyasında ayrıntılı bir şekilde yazılmıştır.

Eminim bu konularda bilgisi benden çok daha iyi olan arkadaşlar bu paylaşımları bir üst seviyeye çıkarmamda bana yardımcı olabilirler. 
Hobi olarak başladığım bu işin faydalı olması dileği ile...

* [Kelime kök ve gövdesi bulma (Base, stem)](https://github.com/brolin59/PYTHON-TURKCE-DOGAL-DIL-ISLEME-TURKISH-NLP/wiki/2.-Morfolojik-Analiz)
* [Kelime ve kural tabanlı morfolojik analiz (Lemmatization)](https://github.com/brolin59/PYTHON-TURKCE-DOGAL-DIL-ISLEME-TURKISH-NLP/wiki/2.-Morfolojik-Analiz)
* [Yanlış yada Ascii karakterler kullanılarak yazılan kelimeler için öneri listesi (Spelling Corrector) - Yapım aşamasında](https://github.com/brolin59/PYTHON-TURKCE-DOGAL-DIL-ISLEME-TURKISH-NLP/wiki/5.-Kelime-Kontrol%C3%BC)
* [Metin parçalama ve sayma işlemleri (Tokenization)](https://github.com/brolin59/PYTHON-TURKCE-DOGAL-DIL-ISLEME-TURKISH-NLP/wiki/3.-Par%C3%A7alama-(Tokenization))
* [Faydalı olabilecek ek fonksiyonlar.(levenshtein_distance, number_to_word, word_to_number vb.)](https://github.com/brolin59/PYTHON-TURKCE-DOGAL-DIL-ISLEME-TURKISH-NLP/wiki/4.-Ek-Fonksiyonlar)


trnlp her işlem için bir sözlüğe ihtiyaç duyar. trnlp'yi indirdiğinizde bu sözlüklerde beraberinde gelmiş olacaktır. Şu an için sözlüklerde bir değişiklik yapma ya da sözlüğe ekleme yapma özelliği bulunmamaktadır. Tüm sözlükler .pickle dosyası olarak kaydedilmiş ve erişime açıktır. Gelecek versiyonda sözlüğe veri ekleme özelliğini de eklemeyi düşünüyorum. Yine de gerekli sözlük formatına bağlı kalmak kaydı ile manuel değişiklikler yapılabilir.

Her bölüm için ayrıntılı anlatımlar ilgili wiki sayfasında mevcuttur.

Benim bilgisayarımda (İntel i5-2450M işlemci 4GB Bellek) kelime uzunluklarına bağlı olarak 1 saniyede yapılabilen analiz sayısı 2250 ile 3000 arasında değişmektedir.

### Projenin İçeriği :
  
- Sözlük hazırlanması. + YAPILDI (Testler sırasında düzenlemeler yapılacak)
- Heceleme algoritması + YAPILDI
- Türkçe ses uyumları kontrolü + YAPILDI
- Kelime bazlı kök/gövde ve eklerin bulunması + YAPILDI (Testler sırasında düzenlemeler yapılacak)
- Cümle ayırma. + YAPILDI (Testler sırasında düzenlemeler yapılacak)
- Yanlış yazılan kelimelerin bulunması ve doğru yazımına dair öneride bulunulması yada otomatik olarak düzeltilmesi. (Yapım aşamasında. Kısa sürede eklenecek.)
- Eklerin ve ek kontrollerinin düzeltilmesi.
- Paket oluşturma. (Düzeltmeler yapıldıktan sonra yapılacak.)
- Cümle analizi yapılması ve cümlenin öğelerine ayrılması.
