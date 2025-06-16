import sys 
import os
import platform
import subprocess
import ctypes
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL



def reboot_assistant() -> str:
    try:
        print("Ashborn yeniden başlatılıyor...")

        current_script = os.path.abspath(__file__)
        base_dir = os.path.dirname(current_script)

        found_main = None
        for _ in range(4): 
            potential_main = os.path.join(base_dir, "main.py")
            if os.path.exists(potential_main):
                found_main = potential_main
                break
            base_dir = os.path.dirname(base_dir)

        exe_path = os.path.join(os.path.dirname(current_script), "..", "dist", "gui.exe")
        exe_path = os.path.abspath(exe_path)

        if os.path.exists(exe_path):
            subprocess.Popen([exe_path], cwd=os.path.dirname(exe_path))
        elif found_main:
            subprocess.Popen([sys.executable, found_main], cwd=os.path.dirname(found_main))
        else:
            return "[HATA] Uygulama yeniden başlatılamadı. 'gui.exe' veya 'main.py' bulunamadı."

        sys.exit(0)

    except Exception as e:
        return f"[HATA] Ashborn'u yeniden başlatma başarısız: {str(e)}"


def exit_system() -> str: 
    print("Asistan kapatılıyor... Sonraki emre kadar elveda kralımız...")
    sys.exit(0)

def shutdown():
    try:
        os.system("shutdown /s /t 0")
        return "Bilgisayar kapatılıyor..."
    except Exception as e:
        return f"[-] Kapatma sırasında hata oluştu: {str(e)}"

def restart_os():
    try:
        os.system("shutdown /r /t 0")
        return "Bilgisayar yeniden başlatılıyor..."
    except Exception as e:
        return f"[-] Yeniden başlatma sırasında hata oluştu: {str(e)}"

def logoff():
    try:
        os.system("shutdown -l")
        return "Oturum kapatılıyor..."
    except Exception as e:
        return f"[-] Oturum kapatma hatası: {str(e)}"

def sleep_mode():
    try:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "Uyku moduna geçiliyor..."
    except Exception as e:
        return f"[-] Uyku modu hatası: {str(e)}"

def lock_screen():
    try:
        ctypes.windll.user32.LockWorkStation()
        return "Ekran kilitlendi."
    except Exception as e:
        return f"[-] Ekran kilitleme hatası: {str(e)}"

def open_task_manager():
    try:
        os.system("taskmgr")
        return "Görev yöneticisi açılıyor..."
    except Exception as e:
        return f"[-] Görev yöneticisi açılamadı: {str(e)}"

def open_settings():
    try:
        subprocess.run(["start", "ms-settings:"], shell=True)
        return "Ayarlar açılıyor..."
    except Exception as e:
        return f"[-] Ayarlar paneli açılamadı: {str(e)}"

try:
    def mute_audio():
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
            volume.SetMute(1, None)
            return "Ses kapatıldı."
        except Exception as e:
            return f"[-] Ses kapatılamadı: {str(e)}"

    def unmute_audio():
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
            volume.SetMute(0, None)
            return "Ses açıldı."
        except Exception as e:
            return f"[-] Ses açılamadı: {str(e)}"

except ImportError:
    def mute_audio():
        return "Ses kontrolü için pycaw modülü eksik."

    def unmute_audio():
        return "Ses kontrolü için pycaw modülü eksik."



