# Atlantis Travel – Kurulum ve Yayına Alma Rehberi

Bu depo, Promake'e ihtiyaç duymadan Hostinger'da çalışan Atlantis Travel web sitesidir.
Statik HTML sayfaları + tek bir PHP form işleyicisinden oluşur. Veritabanı, eklenti veya
ücretli hizmet gerektirmez.

> **Önemli:** Bu rehberdeki hiçbir adım mevcut atlantistravel.com.tr sitesini, DNS kayıtlarını,
> e-posta hesaplarını veya Lidya Hasat sitesini değiştirmez. Alan adı bağlama adımı (Bölüm 6)
> ayrıca onay gerektirir.

## 1. İçerik

| Bölüm | Dosyalar |
| --- | --- |
| Türkçe sayfalar | `index.html`, `kurumsal-konaklama.html`, `vip-transfer.html`, `saglik-turizmi.html`, `fuar-konaklama.html`, `services.html` (Kurumsal Çözümler), `about.html`, `teklif-al.html`, `contact.html`, `sss.html`, `privacy.html`, `terms.html`, `tesekkurler.html` |
| İngilizce sayfalar | `en/` klasörü (aynı sayfaların İngilizcesi) |
| Form | `form.php` + `inc/config.php` + `inc/mailer.php` |
| Stil / betik / görsel | `assets/` |
| Sunucu kuralları | `.htaccess` (temiz adresler, HTTPS, güvenlik başlıkları, önbellek, eski adres yönlendirmeleri) |
| SEO | `sitemap.xml`, `robots.txt`, her sayfada başlık, açıklama, canonical, hreflang, Open Graph, JSON-LD |
| Kaynak | `_kaynak/build.py` (tüm sayfaları üretir), `_kaynak/router.php` (yalnızca yerel test) |

Mevcut Promake adresleri korunmuştur: `/about`, `/services`, `/contact`, `/sss`, `/kurumsal-konaklama`,
`/fuar-konaklama`, `/privacy`, `/terms`. Boş şablon olan `/turlar` → `/services`, `/team` → `/about`
adresine kalıcı (301) yönlendirilir.

## 2. GitHub'a aktarma

1. GitHub'da **özel (private)** bir depo oluşturun, örneğin `atlantis-travel-site`.
2. Bu klasörde:
   ```bash
   git remote add origin git@github.com:KULLANICI/atlantis-travel-site.git
   git push -u origin main
   ```

## 3. Hostinger geçici adresinde test sitesi

1. hPanel → **Web Siteleri** → **Web sitesi ekle** → boş site (PHP/HTML) seçin ve
   **geçici alan adı** (…hostingersite.com) ile oluşturun.
   *Planınızda boş web sitesi hakkı yoksa ve ek ödeme isteniyorsa burada durun.*
2. Yeni sitenin panelinde **Gelişmiş → Git** bölümüne gidin.
   - Depo: `git@github.com:KULLANICI/atlantis-travel-site.git`
   - Dal (branch): `main`
   - Kurulum yolu: boş bırakın (sitenin kendi `public_html` klasörü)
3. Depo özel olduğu için hPanel'in gösterdiği **SSH anahtarını** GitHub'da
   *Depo → Settings → Deploy keys → Add deploy key* bölümüne ekleyin (yalnızca okuma).
4. **Deploy** düğmesine basın. İsterseniz "Auto Deployment" adresini GitHub *Webhooks*
   bölümüne ekleyerek her `git push` sonrası otomatik güncelleme sağlayabilirsiniz.
5. Geçici adreste site arama motorlarına kapalıdır (`.htaccess` `X-Robots-Tag: noindex` gönderir).

Lidya Hasat sitesinin klasörünü kurulum yolu olarak **seçmeyin**.

## 4. Formun e-posta gönderimi

Varsayılan: PHP `mail()` ile `info@atlantistraveltr.com` adresine gönderim. Ek ayar gerekmez.

Daha güvenilir teslimat için (önerilir) SMTP kullanın:
1. hPanel'de, sitenin bağlı olduğu alan adında bir gönderim adresi kullanın (ör. mevcut
   `emrah@atlantistravel.com.tr` ya da yalnızca form için açılacak bir adres; yeni hesap
   açmak ücretliyse açmayın).
2. Dosya Yöneticisi → `public_html/inc/` içinde `config.local.example.php` dosyasını
   `config.local.php` adıyla kopyalayın ve yorum satırlarını açıp bilgileri doldurun.
3. Bu dosya Git'e gönderilmez; şifre depoda yer almaz.

Alıcı adresini değiştirmek için `inc/config.php` içindeki `to_email` değerini düzenleyin.

## 5. Test kontrol listesi (geçici adreste)

- [ ] Tüm menü bağlantıları TR ve EN'de açılıyor; TR/EN geçişi aynı sayfanın karşılığına gidiyor
- [ ] Teklif formu: boş gönderimde uyarı; dolu gönderimde yeşil onay mesajı
- [ ] `info@atlantistraveltr.com` kutusuna test talebi ulaştı (spam klasörünü de kontrol edin)
- [ ] Fuar ve iletişim formları da e-posta gönderiyor
- [ ] "WhatsApp ile gönder" düğmesi form bilgileriyle +90 507 397 87 94'e mesaj açıyor
- [ ] Telefonda alt çubuk (Ara / WhatsApp / Teklif Al) çalışıyor
- [ ] `/turlar` → `/services` yönleniyor; `/inc/config.php` 403 veriyor
- [ ] Çerez bildirimi: "Kabul et" sonrası Google Analytics yükleniyor, "Yalnızca zorunlu" sonrası yüklenmiyor
- [ ] PageSpeed Insights (mobil) ölçümü

## 6. Canlıya alma (yalnızca onayınızdan sonra)

Mevcut site Promake'ten yayında olduğu için geçiş anında yalnızca **web trafiği** değişir:

1. Geçişten önce hPanel → DNS bölgesindeki tüm kayıtların ekran görüntüsünü alın.
2. hPanel'de yeni siteye `atlantistravel.com.tr` alan adını bağlayın; yalnızca **A** ve **www**
   kayıtları değişmelidir. **MX, SPF (TXT) ve diğer e-posta kayıtlarına dokunulmaz.**
3. SSL sertifikasının etkinleştiğini kontrol edin; Search Console'a `sitemap.xml` gönderin.
4. İlk 48 saat formları ve e-posta teslimatını izleyin; sorun olursa A kaydını eski değere
   (1. adımdaki ekran görüntüsü) döndürerek Promake sitesine geri dönebilirsiniz.
5. Promake aboneliğini ancak yeni site sorunsuz çalıştıktan sonra değerlendirin.

## 7. İçerik düzenleme

Metinler `_kaynak/build.py` içindedir. Düzenledikten sonra:
```bash
python3 _kaynak/build.py      # sayfaları ve sitemap.xml'i yeniden üretir
git commit -am "İçerik güncellemesi" && git push
```
Yerelde denemek için: `php -S localhost:8080 _kaynak/router.php` → http://localhost:8080

CSS veya JS değiştirirseniz `build.py` içindeki `VERSION` değerini artırın (tarayıcı önbelleği için).

## 8. Görseller

Sitede yalnızca Atlantis Travel'ın kendi logosu ve özgün çizilmiş bir İstanbul silüeti kullanılır;
kullanım hakkı sorunu yoktur. Fotoğraf eklemek isterseniz yalnızca **kendi çekimleriniz** veya
ticari kullanıma izin veren ücretsiz lisanslı kaynaklar (ör. Unsplash, Pexels lisansı) kullanın;
dosyaları WebP'ye çevirip 1600 px genişliği aşmadan `assets/img/` içine koyun.

## 9. Onay bekleyen içerikler

- TÜRSAB belge numarası ve ticari ünvan (altbilgi ve güven bölümüne eklenecek)
- "200+ otel" ifadesi brifinize göre yazılmıştır; farklıysa `build.py` içinde güncelleyin
- İkinci telefon numarası (+90 554 135 36 40) mevcut siteden alınmıştır; doğrulayın
