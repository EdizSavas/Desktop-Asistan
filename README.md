# Teknik Altyapı ve Mimarisi

1. Ana Program (‘main.py’):

Uygulamanın başlangıç noktasıdır. GUI ve komut yönetim sistemini burada entegre eder.

2. Görsel Arayüz (‘gui.py’):

PyQt6 kullanılarak oluşturulan modern bir arayüz sunar. Kullanıcıdan gelen yazılı komutları alır, mikrofona bağlı olarak ses kaydı yapabilir. Arayüzde mikrofon tuşu, input alanı ve yardım menüsü gibi öğeler yer alır.

3. Komut Yöneticisi (‘command_handler.py’):

Girilen komutları yorumlayarak, doğru çalışacak modüle yönlendirir. Takma adlar (alias) ve benzerlik puanları ile esnek komut tanıma sağlar.

4. Komut Modülleri (commands klasörü):

file_operations.py: Dosya açma, kopyalama, taşıma gibi işlevler

system_control.py: Bilgisayarı kapatma, yeniden başlatma vs.

web_operations.py: Tarayıcıda URL açma vb.

shortcuts.py, kişisel.py: Kısayollar ve kişisel tepki komutları

5. Ses Tanıma Altyapısı:

Proje ilk aşamada Vosk kullanarak offline olarak çalışan bir ses tanıma sistemine sahiptir. Fakat sistem, daha doğru ve modern bir tanıma için Whisper-Tiny modeline geçiş yapacak şekilde tasarlanmıştır. Bu sayede komutlar çok daha kararlı ve doğru algılanabilecektir.


#  Kullanılan Teknolojiler

• Python 3.11 / 3.13

• PyQt6: Modern ve profesyonel bir GUI sunar

• NumPy, SciPy: Bazı mantıksal hesaplamalarda

• Vosk: Offline ses tanıma (ilk versiyon)

• Whisper (faster-whisper): Yeni jenerasyon ses tanıma

• JSON: Yapılandırma dosyaları için

# Genişleme Potansiyeli ve Gelecek Planları

• Whisper-Tiny ile daha doğru sesli komut algılama

• Karmaşık doğal dil işleme: "Bana bugünün hava durumunu söyle" gibi

• Görsel geri bildirim: Komutlara karşı arayüzde anında tepki verme

• Olay zamanlayıcıları, kışisel not sistemi, hafıza sistemi gibi özellikler planlanmaktadır.

# Kullanılabilir Komutlar Listesi

 • Dosya ve Sistem Komutları

    "bilgisayarı kapat"

    "yeniden başlat"

    "oturumu kapat"

    "uykuyu başlat"

• Dosya İşlemleri

    "masaüstü klasörünü aç"

    "belgeleri aç"

    "bir dosya ara"

• Web ve Bağlantı Komutları

    "google'ı aç"

    "youtube'da video ara"

    "github'a git"

• Kısayol ve Yardım Komutları

    "yardım ekranını göster"

    "kısayol ayarlarına gir"

    "ayarları sıfırla"

• Kışisel ve Tepki Komutları

    "kapat"

    "sesi kıs" / "sesi aç"

    "sus" / "konuş"
