<h2> ÖBA Otomatik Oynatıcı </h2>
<h3> Katkıda Bulunma Rehberi </h3>  

Uygulamaya katkı vermeye karar verdiğiniz için <i>çok teşekkürler!</i> Katkılarınız uygulamanın daha işlevsel kalmasına ve sürdürülebilir olmasına <i>müthiş bir katkısı olacak.</i>

---------------------------------

<h3> Nasıl katkıda bulunulur? </h3> 

<b>Öncelikle</b>, uygulamada bulduğunuz her türlü hata için hemen kodda değişiklik yapıp <i>PR</i> oluşturmanıza <i>gerek yok</i>. Proje sahibi ve bakımcılarına, katkı verenlerine <b>geri bildirim için</b> yaşadığınız sorunu <i>öncelikle</i> <i>Issues</i> bölümünden belirtebilir ya da <a href="https://forms.gle/6o3kqXHRJ2iXEqs36">bu formu</a> doldurabilirsiniz.

Uygulama deposuna katkıda bulunabilmeniz için ilk önce <i>depoyu çatallayıp</i> değişikliklerinizi <b><i>mevcut çatalınızda</i></b> yapmalısınız. Değişiklikleri yaptıktan sonra asıl dal için <i>PR</i> oluşturmalısınız. 

Uygulama için özel sanal ortam oluşturma işini kolaylaştırmak için <code><a  href="src">src</a></code> dizininde bulunan Powershell betiklerini inceleyebilir ve kullanabilirsiniz. Aynı biçimde, uygulamanın kullandığı kütüphanelere ve sürümlerine <code><a  href="src/requirements.txt">src/requirements.txt</a></code> dosyadan ulaşabilirsiniz. Daha detaylı bir açıklamaya <a  href="src/README.md">buradan</a> ulaşabilirsiniz. 

Düzenlemenizi bitirdikten sonra, kendi çatalınızda yaptığınız değişiklikleri PR'da <i>liste halinde özetlemeli</i> ve ne değişiklikler yaptığınızı <i>kısaca açıklamalısınız</i>. PR proje sahibi tarafından incelendikten sonra <i>sorun olmadığı takdirde</i> ana dalla birleştirilecektir.  

<br>
<i>⚠️<b>Uyarı</b>: Çatalınızda değişiklikler yaparken <b>asla</b> <code><a  href="src/VERSION">src/VERSION</a></code> ve <code><a  href="src/executable/x86.zip">src/executable/x86.zip</a></code> dosyalarını değiştirmemelisiniz. Bu dosyalarda <u>değişiklik yapıldığı takdirde</u> PR'ınız <b>reddedilecektir</b>. Kodun yürütülebilir bir dağıtım paketine dönüştürülmesi süreci tamamen kod sahibine ve bakımcılarına aittir, PR'nız kabul edilip ana dalla birleştirildiği takdirde <u>yalnızca proje sahibi</u> uygulamanın dağıtılabilir sürümünü hazırlayabilir.</i>