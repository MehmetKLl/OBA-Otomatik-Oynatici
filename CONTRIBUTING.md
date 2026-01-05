<h2> ÖBA Otomatik Oynatıcı </h2>
<h3> Katkıda Bulunma Rehberi </h3>

Uygulamaya katkı vermeye karar verdiğiniz için çok teşekkürler! Katkılarınız uygulamanın daha işlevsel kalmasına ve sürdürülebilir olmasına müthiş bir katkısı olacak.

---------------------------------

<h3> Nasıl katkıda bulunulur? </h3>

Öncelikle, uygulamada bulduğunuz her türlü hata için hemen kodda değişiklik yapıp PR oluşturmanıza gerek yok. Proje sahibi ve bakımcılarına, katkı verenlerine geri bildirim için yaşadığınız sorunu öncelikle Issues bölümünden belirtebilirsiniz.

Uygulama deposuna katkıda bulunabilmeniz için ilk önce depoyu çatallayıp değişikliklerinizi mevcut çatalınızda yapmalısınız. Değişiklikleri yaptıktan sonra asıl dal için PR oluşturmalısınız.

Uygulama için özel sanal ortam oluşturma işini kolaylaştırmak için <code><a href="src">src</a></code> dizininde bulunan Powershell betiklerini inceleyebilir ve kullanabilirsiniz. Aynı biçimde, uygulamanın kullandığı kütüphanelere ve sürümlerine <code><a href="src/requirements.txt">src/requirements.txt</a></code> dosyadan ulaşabilirsiniz. Daha detaylı bir açıklamaya <a href="src/README.md">buradan</a> ulaşabilirsiniz.

Düzenlemenizini bitirdikten sonra, kendi çatalınızda yaptığınız değişiklikleri PR'da liste halinde özetlemeli ve ne değişiklikler yaptığınızı kısaca açıklamalısınız. PR proje sahibi tarafından incelendikten sonra sorun olmadığı takdirde ana dala birleştirilecektir.

<br>
<i>⚠️<b>Uyarı</b>: Çatalınızda değişiklikler yaparken asla <code><a href="src/VERSION">src/VERSION</a></code> ve <code><a href="src/executable/x86.zip">src/executable/x86.zip</a></code> dosyalarını değiştirmemelisiniz. Bu dosyalarda değişiklik yapıldığı takdirde PR'ınız reddedilecektir. Kodun yürütülebilir bir dağıtım paketine dönüştürülmesi süreci tamamen kod sahibine ve bakımcılarına aittir, PR'nız kabul edilip ana dalla birleştirildiği takdirde yalnızca proje sahibi uygulamanın dağıtılabilir sürümünü hazırlayabilir.</i>
