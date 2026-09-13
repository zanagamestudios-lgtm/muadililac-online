# Muadil İlaç iOS Web

TİTCK kaynaklı ilaç referans kataloğu için GitHub Pages üzerinde yayınlanan mobil odaklı web uygulaması.

## Canlı veri kaynağı

Uygulamanın tek canlı katalog kaynağı:

`https://zanagamestudios-lgtm.github.io/muadililac/data/releases/latest/manifest.json`

İlk açılışta cihazda doğrulanmış yerel katalog yoksa uygulama bu manifesti alır, manifestteki `medicines.json.gz` `latestPath` dosyasını indirir, SHA-256 ile doğrular ve JSON kayıt sayaçlarını `recordCount`, `activeCount` ve `passiveCount` ile karşılaştırır. Doğrulama geçmeden katalog kullanıma açılmaz.

## Güncelleme davranışı

Daha sonraki açılışlarda uygulama yalnızca daha önce doğrulanmış katalog pointer’ının gösterdiği Cache Storage verisini yükler. Kullanıcı **Şimdi kontrol et** düğmesine basmadıkça canlı manifest yeniden indirilip yerel katalog değiştirilmez.

Kullanıcı güncelleme istediğinde yeni manifest ve gzip katalog ayrı bir Cache Storage alanına indirilir. SHA-256, JSON kayıt sayısı ve aktif/pasif toplamları doğrulandıktan sonra pointer atomik biçimde yeni alana geçirilir; eski alanlar daha sonra temizlenir. Favoriler, tema ve son aramalar ayrı localStorage anahtarlarında tutulur ve katalog güncellemesinden etkilenmez.

## Yayın

Site GitHub Pages üzerinden yayınlanır. `index.html`, cache busting amacıyla `assets/index-live-v5.js` production bundle’ını kullanır. Service worker shell sürümü `muadil-ilac-shell-v2` olarak güncellenmiştir.
