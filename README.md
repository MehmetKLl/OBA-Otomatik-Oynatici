
<h2> ÖBA Otomatik Oynatıcı </h2>
<h3> Sürüm 1.3.6 </h3>

<h4>Kullanım</h4>

- Program ilk çalıştırıldığı vakit gereken dosyaları kurmakta ve programı öyle çalıştırmaktadır. Bundan dolayı program ilk seferde biraz geç açılabilir.
- Program ilk çalıştırıldığı vakit kurulması gereken dosyaları internetten indirdiğinden program ilk çalıştırıldığı vakit internet gerektirmektedir.
- Arayüz ekrana gelmeden önce sürüm denetleyicisi çalıştırıldığından arayüzün ekrana gelmesi bazı etkenlere bağlı olarak değişebilir.
- Program kurulduktan sonra aynı dosyayla kuruluma gerek olmadan program çalıştırılabilir.
---------------------------------
<img src="img/pic1.png">
</img>
<i>İlk oba_otomatik_oynatma.exe çalıştırılır.</i>

---------------------------------
<img src="img/pic2.png">
</img>

---------------------------------

<img src="img/pic3.png">
</img>
<i>Ayarlar kısmından gerekli düzenlemeler yapılabilir.</i>

---------------------------------

<img src="img/pic2.png">
</img>
<i>"Başlat" tuşuna basarak program çalıştırılır.</i>

---------------------------------

<h4>Program Hakkında Bilgiler</h4>

- Program Python ile yazılmıştır, arayüzlü basit bir makro uygulamasıdır.
- Program çalışırken ekran görüntüsünü işleyerek çalışmaktadır, bu yüzden bir yere gideceğiniz zaman programı açık bırakabilirsiniz.
- Programda requests, pywin32, pyautogui, tkinter ve keyboard modülleri/kütüphaneleri kullanılmıştır.
- Programı kendi atadığınız kısayol ile kapatabilirsiniz. 

---------------------------------

<h4>Uyarılar</h4>

- Program Chrome tarayıcısında %100 site büyütme boyutunda farklı ekran boyutlarında çalışabilmektedir. 
- Tüm çalıştırılabilir dosyalar 32 bit pyinstaller ile bundle edilmiştir, 64 bit sistemlerde de çalışmaktadır. 
- Program Windows 10 x64/x86, Windows 8 x64/x86 ve Windows 7 x86 (6.1 Build 7600) sistemlerde kusursuz çalışmaktadır, program diğer sistemlerde denenmemiştir.
- Program "Eğitime başla/Eğitime devam et" tuşuna basılıp yeni ekran açıldığı zaman en önde tarayıcı gözükecek şekilde çalıştırılmalıdır.
- Program çalışırken fare ile oynanmamalıdır, eğer oynarsanız büyük ihtimalle programın videoyu kontrol etme mekanizması bozulacaktır.
- Program çalışırken bilgisayarın kapanmaması için bilgisayarın uyku moduna girme süresi kapatılmalıdır. 

---------------------------------

<h4>Sürüm Notları</h4>

|Sürüm|Notlar|
|-|-|
|1.3.6|Programın mekanizması bilgisayarın uyku moduna girmesini engelleyecek biçimde geliştirildi. Optimizasyon sorunları, kod hataları giderildi.|
|1.3.5|Windows 7 desteği eklendi. Yeni log sistemi eklendi. Otomatik oynatma mekanizmasının kaynak kodları düzenlendi. Kurulum programının kodları düzenlendi. Arayüzün performansı arttırıldı.|
|1.3.4|Programın mekanizması geliştirildi. Log sistemi kaldırıldı. Kod yapısı düzenlendi.|
|1.3.3|Arayüz tasarımı geliştirildi.|
|1.3.2|Sürüm denetleyicisinin internet olmayınca oluşturduğu hatalar giderildi. Arayüz tasarımındaki hatalar giderildi. |
|1.3.1|Sürüm denetleyicisi geliştirildi. Kodlar düzenlendi. |
|1.3.0|Sürüm denetleyicisi eklendi. Bazı hatalar giderildi.|
|1.2.2|Hata yakalama geliştirildi. Bazı hatalar giderildi. Programın stabilitesi arttırıldı.|
|1.2.1|Arayüz eklendi. Programı durdurma kısayolunu değiştirme seçeneği eklendi.|
|1.1.0|Programın mekanizması geliştirildi.|
|1.0.0|Programın stabil olmayan ve yayınlanmayan ilk sürümü.|
