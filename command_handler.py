import json
import os
from commands.system_control import *
from commands.file_operations import *
from commands.web_operations import *
from commands.kişisel import *


command_map = {
    "çık": exit_system,
    "yeniden başlat": reboot_assistant,
    "müzik": music,
    "youtube": youtube,
    "şarkıyı duraklat": sarki_duraklat,
    "önceki şarkı": sarki_onceki,
    "sonraki şarkı": sarki_sonraki,
    "bilgisayarı kapat": shutdown,
    "bilgisayarı yeniden başlat": restart_os,
    "oturumu kapat": logoff,
    "uyku modu": sleep_mode,
    "ekranı kilitle": lock_screen,
    "görev yöneticisini aç": open_task_manager,
    "ayarlar panelini aç": open_settings,
    "sesi kapat": mute_audio,
    "sesi aç": unmute_audio,
    "masaüstünü göster": show_desktop,
    "belgeleri aç": open_documents,
    "son indirilen dosyayı aç": open_latest_download,
    "ekran görüntüsü al": take_screenshot,
    "ana dizini aç": open_home,
    "klasör oluştur": create_folder,
    "chatgpt'yi aç": open_chatgpt,
    "hava durumu": show_weather
}

alias_path = os.path.join(os.path.dirname(__file__), "config", "command_aliases.json")
with open(alias_path, "r", encoding="utf-8") as f:
    alias_map = json.load(f)

def resolve_alias(command: str) -> str:
    """Kullanıcı komutunu alias listesinden eşleştirerek gerçek komutla değiştirir"""
    for real_cmd, aliases in alias_map.items():
        if command in aliases:
            return real_cmd
    return command

def komudu_al(command: str, gui_ref=None) -> str:
    command = command.lower().strip()
    command = resolve_alias(command)

    if command in command_map:
        if command == "klasör oluştur":
            return command_map[command](command)
        return command_map[command]()
    return "[-] Bu komut tanımlı değil veya doğru algılanamadı."

    
# def komudu_al(command: str, gui_ref=None) -> str:
#     command = command.lower().strip()
    
#     if command in ["çık", "çıkış", "kapat", "görüşürüz", "kapan", "sistemi kapat", "exit", "end"]:
#         from commands.system_control import exit_system
#         return exit_system()
    
#     elif command.startswith("aç"):
#         from commands.file_operations import dosya_ac
#         return dosya_ac(command)
    
#     elif command.startswith("sil") or command.startswith("dosya sil"):
#         from commands.file_operations import dosya_sil
#         return dosya_sil(command)
    
#     #elif command.startswith("ara ") or command.startswith("bilgi ver "):
#         #from commands.knowledge import search_info 
#         #return search_info(command)
    
    # elif command in ["yeniden başlat", "reboot", "ashborn yeniden başlasın"]:
    #     subprocess.Popen([sys.executable, sys.argv[0]])
    #     os._exit(0)
        
#         #from commands.system_control import reboot_assistant
#         #return reboot_assistant()
    
#     elif command in ["yt music", "şarkı", "müzik", "tıngırdat", "müzik", "ym"]:
#         from commands.kişisel import music
#         return music()
    
#     elif command in ["yt", "youtube", "video", "sıkıldım", "daraldım"]:
#         from commands.kişisel import youtube
#         return youtube()
    
#     elif command in ["durdur", "duraklat", "stop", "ps", "devam", "oynat", "hadi", "bekletme", "çal", "şarkıyı oynat"]:
#         from commands.kişisel import sarki_duraklat
#         return sarki_duraklat()
    
#     elif command in ["önceki", "öncekini oynat", "az önceki", "yeni biteni aç", "bf"]:
#         from commands.kişisel import sarki_onceki
#         return sarki_onceki()
    
#     elif command in ["sonraki", "bir sonraki", "geç", "sıradaki", "ardını gönder", "yolla", "hadi", "hızını kesme", "sp"]:
#         from commands.kişisel import sarki_sonraki
#         return sarki_sonraki()
    
#     elif command in["bilgisayarı kapat", "kill", "over", "kl", "shutdown"]:
#         from commands.system_control import shutdown
#         return shutdown()
    
#     elif command in ["bilgisayarı yeniden başlat", "restart", "st"]:
#         from commands.system_control import restart_os
#         return restart_os()
    
#     elif command in ["oturumu kapat", "başka kullanıcı", "kişi değiştir"]:
#         from commands.system_control import logoff
#         return logoff()
    
#     elif command in ["uyu", "uyku", "uykuya geç", "sistemi uyut", "sleep", "slp"]:
#         from commands.system_control import sleep_mode
#         return sleep_mode()
    
#     elif command in ["kilitle", "lock", "lock screen", "kilit ekranı", "bilgisayarı kilitle", "kilit", "sc"]:
#         from commands.system_control import lock_screen
#         return lock_screen()
    
#     elif command in ["yönetici", "yöneticiyi aç", "görev yöneticisi", "görev yöneticisini aç", "işlem sonlandırasım geldi"]:
#         from commands.system_control import open_task_manager
#         return open_task_manager()
    
#     elif command in ["ayarlar", "ayarları aç", "ayar", "sistem ayarları"]:
#         from commands.system_control import open_settings
#         return open_settings()
    
#     elif command in ["sesi kapat", "sus", "kapa çeneni", "tıp", "shh", "mute"]:
#         from commands.system_control import mute_audio
#         return mute_audio()
    
#     elif command in ["sesi düzelt", "konuş", "konuşabilirsin", "susturma kakdırıldı", "susturma", "unmute"]:
#         from commands.system_control import unmute_audio
#         return unmute_audio()
    
#     elif command in ["Masaüstünde göster", "Masaüstünü göster", "Desktop", "Masaüstü"]:
#         from commands.file_operations import show_desktop
#         return show_desktop()
    
#     elif command in ["Belgeler", "Belgelerde aç", "Dökümanlarda aç", "Dökümanlar", "Documents"]:
#         from commands.file_operations import open_documents
#         return open_documents()
    
#     elif command in ["Yeniler", "Yeni gelenler", "Son yüklenenler", "latest"]:
#         from commands.file_operations import open_latest_download
#         return open_latest_download()
    
#     elif command in ["SS", "Screenshot", "Ekran görüntüsü", "Ekran görüntüsü al", "Kap", "Yakala", "Kaçırma", "Hızlı düşün"]:
#         from commands.file_operations import take_screenshot
#         return take_screenshot()
    
#     elif command in ["Ev", "Beni eve götür", "Home", "Ana klasör", "Başlangıç dizini", "Home klasörü"]:
#         from commands.file_operations import open_home
#         return open_home()
    
#     elif command in ["Klasör oluştur", "Klasör yarat", "Klasörle beni", "Yarat"]:
#         if ":" not in command:
#             return "[-] Klasör adı belirtilmedi."
#         from commands.file_operations import create_folder
#         return create_folder(command)
    
#     elif command.lower().startswith("google'da ara:"):
#         from commands.web_operations import search_google
#         return search_google(command)
    
#     elif command in ["chatgpt'yi aç", "AI", "ai", "Yapay zeka", "Chatgpt", "Sohbet Zeka", "Makine", "Ses çıkaran teneke"]:
#         from commands.web_operations import open_chatgpt
#         return open_chatgpt()
    
#     elif command.lower().startswith("youtube'da aç:"):
#         from commands.web_operations import search_youtube
#         return search_youtube(command)
    
#     elif command in ["hava durumu nedir", "hava", "havadurumu", "yanıyorum", "donuyorum", "güneşli hava mı olur"]:
#         from commands.web_operations import show_weather
#         return show_weather()

    # else:
    #     return "Komut anlaşılamadı. Yeniden emir verin."