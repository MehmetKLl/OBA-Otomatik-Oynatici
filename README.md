<h2> ÖBA Otomatik Oynatıcı </h2>
<h3> Sürüm 1.3.0 </h3>

<h4>Kullanım</h4>

- Program ilk çalıştırıldığı vakit gereken dosyaları kurmakta ve programı öyle çalıştırmaktadır. Bundan dolayı program ilk seferde biraz geç açılabilir.
- Program ilk çalıştırıldığı vakit kurulması gereken dosyaları internetten indirdiğinden program ilk çalıştırıldığı vakit internet gerektirmektedir.
- Arayüz ekrana gelmeden önce sürüm denetleyicisi çalıştırıldığından arayüzün ekrana gelmesi bazı etkenlere bağlı olarak değişebilir.
- Program kurulduktan sonra aynı dosyayla kuruluma gerek olmadan program çalıştırılabilir.
---------------------------------
<img src="img/pic1.png">
</img>
<i color="red">İlk oba_otomatik_oynatma.exe çalıştırılır.</i>

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
- Programda requests, pywin32, pyautogui, tkinter, keyboard, os, multiprocessing ve time modülleri kullanılmıştır.
- Programı kendi atadığınız kısayol ile kapatabilirsiniz. 

---------------------------------

<h4>Uyarılar</h4>

- Programın düzgün bir şekilde kullanılabilmesi için yönetici yetkisi ile çalıştırılmalıdır. Programın yönetici yetkisi ile çalıştırılması gerekmesinin sebebi dosya işlemleri sırasında yönetici yetkisinin gerekmesidir.
- Program Chrome tarayıcısında %100 site büyütme boyutunda farklı ekran boyutlarında çalışabilmektedir. 
- Tüm çalıştırılabilir dosyalar 32 bit pyinstaller ile bundle edilmiştir, 64 bit sistemlerde de çalışmaktadır. 
- Program Windows 10 64 bit sistemde kusursuz çalışmaktadır, program diğer sistemlerde denenmemiştir.
- Program "Eğitime başla/Eğitime devam et" tuşuna basılıp yeni ekran açıldığı zaman en önde tarayıcı gözükecek şekilde çalıştırılmalıdır.
- Program çalışırken fare ile oynanmamalıdır, eğer oynarsanız büyük ihtimalle programın videoyu kontrol etme mekanizması bozulacaktır.
- Program çalışırken bilgisayarın kapanmaması için bilgisayarın uyku moduna girme süresi kapatılmalıdır. 

---------------------------------

<h4>Sürüm Notları</h4>

|Sürüm|Notlar|
|-|-|
|1.3.0|Sürüm denetleyicisi eklendi. Bazı hatalar giderildi.|
