# PYTHON TURKÇE DOĞAL DİL İŞLEME - TURKISH NLP
## TÜRKÇE İÇİN DOĞAL DİL İŞLEME ARAÇLARI

*** Ne Python ne de Türkçe dilbigim çok iyi olmamasına rağmen ***hobi*** olarak yazdığım birkaç kodu sizlerle paylaşmak istedim.
Eminim bu konulardaki bilgisi benden çok daha iyi olan arkadaşlar bu paylaşımları bir üst seviyeye çıkarmada bana yardımcı olabilirler. 
Hobi olarak başladığım bu işin faydalı olması dileği ile...

### MorphologicalLR.py :

***MorphologicalLR sözlük ve kural tabanlı*** çalışan kök/gövde ve kelimenin eklerini bulmak için hazırladığım bir algoritmadır. 
Halen test aşamasında olduğum için ***eksikleri yada hataları*** olabilir. Henüz işin başındayız diyebiliriz.
  
Şu an için yapım eklerini tanımlamadım. Sözlüğü oluşturmak baya bir meşakkatli oldu ve çok zamanımı aldı. Halen eksikleri 
ve yanlışları olmasına rağmen yine de iş görür durumda sözlük dosyası. Sözlük dosyasını **Data/sozluk_tekli.txt** içinde 
bulabilirsiniz.
  
***Kelime kök/gövde ve eklerini*** bulmak için yazdığım algoritmanın örnek kullanımı şu şekildedir:

```
from Morphological.MorphologicalLR import ClsEkBul as cb
kelime = cb.('oğlumun')
print('Kelime kök/gövdesi : ', kelime.stems)
print('Eklere ayrılmış hali : ', kelime.result)
  
Kelime kök/gövdesi : ['oğul(isim)']
Eklere ayrılmış hali : ['oğul(isim)+um(2-1. tekil kişi){içe}+un(17-Tamlama eki){içe}']
```

***Kelime ve kural*** tabanlı bir yapı oluşturduğumuz için çoğu zaman birden fazla sonuç dönecektir. Örneğin;

```
from Morphological.MorphologicalLR import ClsEkBul as cb
kelime = cb.('aldım')
print('Kelime kök/gövdesi : ', kelime.stems)
print('Eklere ayrılmış hali : ', kelime.result)
  
Kelime kök/gövdesi : ['al(isim)', 'al(fiil)']
Eklere ayrılmış hali : ['al(fiil)+dı(1-Bilinen Geçmiş Zaman){fçe}+m(26-1. tekil kişi){fçe}', 'al(isim)+dı(2-Hikaye){iefe}+m(9-1. tekil kişi){iefe}']
```

Nihai amacım ***cümle analizi*** yapabilmek olacaktır.

### Projenin İçeriği :

- Sözlük hazırlanması. (Yapıldı. Data klasörünün içinde sozluk_tekli.txt dosyası sözlük bilgilerini içerir.)
- Heceleme algoritması (Yapıldı. Auxiliary/TurkishGrammer.py içinde spellword fonksiyonu kullanılabilir durumda.)
- Türkçe ses uyumları kontrolü (Yapıldı. Auxiliary/TurkishGrammer.py içinde ses uyumu fonksiyonları var.)
- Kelime bazlı kök/gövde ve eklerin bulunması (Yapıldı. Morphological/MorphologicalLR.py ClsEkBul klası kullanılabilir durumda.)
- Cümle ayırma. (Basit bir şey yaptım fakat daha yayınlamadım. Bir kaç testten sonra paylaşacağım.)
- Yazı istatistiği (Bu kısımla da ilgili bir çalışmam var. Biraz düzenledikten sonra yayınlayacağım.)
- Yanlış yazılan kelimelerin bulunması ve doğru yazımına dair öneride bulunulması yada otomatik olarak düzeltilmesi.
- Cümle analizi yapılması ve cümlenin öğelerine ayrılması.

### Fikirler :

### İletişim :
esatmahmutbayol@gmail.com
