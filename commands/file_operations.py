import os
import time
import webbrowser
import subprocess
import pyautogui
import glob
import time
import ctypes.wintypes
from uuid import UUID


KNOWN_FOLDERS = {
    "desktop": "{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}",
    "documents": "{FDD39AD0-238F-46AF-ADB4-6C85480369C7}",
    "downloads": "{374DE290-123F-4565-9164-39C4925E467B}"
}

def get_known_folder_path(folder_id: str):
    path_ptr = ctypes.c_wchar_p()
    ctypes.windll.shell32.SHGetKnownFolderPath(
        ctypes.byref(UUID(folder_id)),
        0,
        0,
        ctypes.byref(path_ptr)
    )
    return path_ptr.value

def dosya_ac(command: str) -> str:
    try:
        hedef = command.replace("aç ", "").strip()
        if not hedef:
            return "[-] Açılacak dosya ya da site belirtilmedi."

        # Web siteleri için otomatik algılama
        if "." in hedef or hedef.startswith("http"):
            if not hedef.startswith("http"):
                hedef = "https://" + hedef
            print(f"Web adresine yönlendiriliyor: {hedef}")
            time.sleep(1)
            webbrowser.open(hedef)
            return "Tarayıcı yönlendirmesi yapıldı."

        # Dosya araması
        arama_başlangıcı = os.getcwd()
        bulunan_yol = None
        for kök, klasörler, dosyalar in os.walk(arama_başlangıcı):
            if hedef in dosyalar:
                bulunan_yol = os.path.join(kök, hedef)
                break

        if bulunan_yol:
            print(f"Dosya bulundu ve açılıyor: {bulunan_yol}")
            time.sleep(1)
            os.startfile(bulunan_yol)
            return "Dosya açıldı."
        else:
            return f"[-] '{hedef}' adlı dosya bulunamadı."

    except Exception as e:
        return f"[-] İşlem sırasında hata oluştu: {str(e)}"

def dosya_sil(command: str) -> str:
    try:
        hedef = command.replace("sil", "").replace("dosya", "").strip()
        if not hedef:
            return "[-] Silinecek dosya belirtilmedi."
        
        arama_başlangıcı = os.getcwd()
        eşleşenler = []
        
        for kök, klasörler, dosyalar in os.walk(arama_başlangıcı):
            for dosya in dosyalar:
                if dosya == hedef:
                    eşleşenler.append(os.path.join(kök, dosya))
        
        if not eşleşenler:
            return f"[-] {hedef} adlı dosya bulunamadı..."
        
        elif len(eşleşenler) == 1:
            silinecek = eşleşenler[0]
            os.remove(silinecek)
            return f"İstenen {hedef} dosyası silinecek."
        
        else:
            mesaj = f"{hedef} adlı birden çok dosya bulundu:\n"
            for i, yol in enumerate(eşleşenler):
                mesaj += f"[{i+1}] {yol}\n"
            mesaj += "\nSilmek istediğiniz dosyanın numarasını girin: "
            
            secim = input(mesaj)
            try:
                secilen_index = int(secim) - 1
                if 0 <= secilen_index < len(eşleşenler):
                    os.remove(eşleşenler[secilen_index])
                    return f"Seçilen dosya silindi: {eşleşenler[secilen_index]}"
                else:
                    return "[-] Geçersiz seçim. Hiçbir dosya silinemedi..."
            except:
                return "[-] Geçersiz giriş. Silme işlemi iptal edildi..."
            
    except Exception as e:
        return f"[-] Dosya silme işlemi başarısız: {str(e)}"

def show_desktop():
    try:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        os.startfile(desktop)
        return "Masaüstü açıldı."
    except Exception as e:
        return f"[-] Masaüstü açılamadı: {str(e)}"
    
def open_documents():
    try:
        documents = os.path.join(os.path.expanduser("~"), "Documents")
        os.startfile(documents)
        return "Belgeler klasörü açıldı."
    except Exception as e:
        return f"[-] Belgeler açılamadı: {str(e)}"

def open_latest_download():
    try:
        downloads = os.path.join(os.path.expanduser("~"), "Downloads")
        list_of_files = glob.glob(os.path.join(downloads, '*'))
        if not list_of_files:
            return "İndirilenlerde dosya bulunamadı."
        latest_file = max(list_of_files, key=os.path.getctime)
        os.startfile(latest_file)
        return f"Son indirilen dosya açıldı: {os.path.basename(latest_file)}"
    except Exception as e:
        return f"[-] Son indirilen dosya açılamadı: {str(e)}"

def take_screenshot():
    try:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        path = os.path.join(os.path.expanduser("~"), "Desktop", f"ekran_goruntusu_{timestamp}.png")
        screenshot = pyautogui.screenshot()
        screenshot.save(path)
        return f"Ekran görüntüsü kaydedildi: {path}"
    except Exception as e:
        return f"[-] Ekran görüntüsü alınamadı: {str(e)}"

def open_home():
    try:
        home = os.path.expanduser("~")
        os.startfile(home)
        return "Ana dizin açıldı."
    except Exception as e:
        return f"[-] Ana dizin açılamadı: {str(e)}"

def create_folder(command: str):
    try:
        folder_name = command.split(":", 1)[1].strip()
        path = os.path.join(os.path.expanduser("~"), folder_name)
        os.makedirs(path, exist_ok=True)
        return f"Klasör oluşturuldu: {path}"
    except Exception as e:
        return f"[-] Klasör oluşturulamadı: {str(e)}"
