<h2> ÖBA Otomatik Oynatıcı </h2>
<b> Sürüm 1.6.1 </b>
<br><br>

<h4><a href="/src/"><code>src/</code></a> dizini</h4>
<p> ÖBA Otomatik Oynatıcı'nın kaynak kodlarının bulunduğu dizindir. </p>
<br>
<b> • </b><code><a href="run.py">run.py</a></code>: oba_otomatik_oynatma.exe dosyasının kaynak kodudur.<br>
<b> • </b><code><a href="main.py">main.py</a></code>: Programın arayüzünün kaynak kodudur.<br>
<b> • </b><code><a href="stub.py">stub.py</a></code>: Programın eski yükleyicisinin uyumluluk yöneticisinin kaynak kodudur.<br>
<b> • </b><code><a href="autoplayer/main.py">autoplayer/main.py</a></code>: Otomatik oynatma mekanizmasının kaynak kodudur.<br><br>
<b> • </b><code><a href="install-dependencies.ps1">install-dependencies.ps1</a></code>:  <code>*.py</code> dosyalarının direkt 
çalıştırılabilmesi için gerekli Python yorumlayıcısı ve kütüphanelerini indiren PowerShell betiği.<br>
<b> • </b><code><a href="main.ps1">main.ps1</a></code>: <code><a href="main.py">main.py</a></code> dosyasını kurulmuş olan Python yorumlayıcısı ile çalıştıran PowerShell betiği.<br>
<b> • </b><code><a href="run.ps1">run.ps1</a></code>: <code><a href="run.py">run.py</a></code> dosyasını kurulmuş olan Python yorumlayıcısı ile çalıştıran PowerShell betiği.<br>
<b> • </b><code><a href="unblock-scripts.bat">unblock-scripts.bat</a></code>: <code>*.ps1</code> dosyalarının çalıştırma engelini kaldıran komut dosyası.<br><br>

<h4>Kodların direkt çalıştırılması</h4>
<p><code>*.py</code> dosyalarının direkt çalıştırılabilmesi için, bir Python yorumlayıcısı ve <code><a href="requirements.txt">requirements.txt</a></code>'deki kütüphanelerin yüklenmiş olması gerekmektedir. Program, dağıtılan sürümde <i>Python 3.7.0</i> sürümünü kullanmaktadır. Eğer sisteminizde <i>Python yüklü ise</i> kütüphaneleri aşağıdaki kodla indirebilir ve sonradan Python ile kodları çalıştırabilirsiniz.</p>

```console
pip install -r requirements.txt
```

<br>

<i><b>Önemli Not:</b> PowerShell betiklerinin çalışması için en düşük PowerShell 3 ve .NET 4.5 sürümleri gereklidir. Daha düşük sürümlerde betikler çalışmayabilir.</i>

<p>Eğer sisteminizde Python yüklü değilse programın ihtiyaç duyduğu tüm kütüphane ve dosyaları indiren <code><a href="install-dependencies.ps1">install-dependencies.ps1</a></code> betiğine sağ tıklayıp <code>PowerShell ile çalıştır</code> tuşuna basarak betiği çalıştırabilirsiniz. <i>Betik imzalı olmadığı için</i> ilk çalıştırıldığında PowerShell betiğe güvenilip güvenilmeyeceğine dair <i>soru sorabilir</i>, bu durumda <code>Y</code> cevabını vererek betiği çalıştırabilirsiniz. <i>Bazı PS sürümlerinde ise</i> PS hiçbir soru sormadan betiğe güvenilmediğine dair hata mesajı vererek <i>kapanabilir</i>, bu durumda ise <code><a href="unblock-scripts.bat">unblock-scripts.bat</a></code> dosyasını çalıştırabilirsiniz. Dosyayı çalıştırıp hata mesajı almadığınız takdirde PowerShell betiklerini çalıştırmayı tekrar deneyebilirsiniz.</p><br>

<p>Eğer <code><a href="unblock-scripts.bat">unblock-scripts.bat</a></code> dosyası başarısız olursa, aşağıdaki kodu PowerShell'i <b>yönetici yetkileriyle açıp</b> komut satırına girerek betik çalıştırma engelini kaldırabilirsiniz. Engeli kaldırdıktan sonra betikleri çalıştırmayı tekrar deneyebilirsiniz.</p>

```powershell
Set-ExecutionPolicy Bypass -Scope CurrentUser
```
<br>

<p><code>*.ps1</code> dosyalarıyla işiniz bittiğinde, PowerShell'in çalıştırma politikasını varsayılan hale geri getirmek için aşağıdaki kodu kullanabilirsiniz.</p>

```powershell
Set-ExecutionPolicy Default -Scope CurrentUser
```

<br>

<p><code><a href="install-dependencies.ps1">install-dependencies.ps1</a></code> dosyasını başarılı bir şekilde çalıştırıp gerekli kütüphaneleri ve Python yorumlayıcısını kurduktan sonra, <code><a href="main.py">main.py</a></code> ve <code><a href="run.py">run.py</a></code> dosyalarını çalıştırmak için <code><a href="main.ps1">main.ps1</a></code> ve <code><a href="main.ps1">run.ps1</a></code> dosyalarını kullanabilirsiniz.</p>
