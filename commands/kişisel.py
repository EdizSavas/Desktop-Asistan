from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import webbrowser
import pygetwindow as gw
import pyautogui
import time
import ctypes
import keyboard


def music():
    webbrowser.open("https://music.youtube.com/")
    return "Yönlendirildi..."

def youtube():
    webbrowser.open("https://www.youtube.com/")
    return "Yönlendirildi.."

MEDIA_KEYS = {
    "şarkıyı değiştir": 0xB0,
    "öncekini çal": 0xB1,
    "durdur": 0xB2,
    "devam et": 0xB3
}

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002

def medya_tusu_gonder(vk_code):
    ctypes.windll.user32.keybd_event(vk_code, 0, KEYEVENTF_EXTENDEDKEY, 0)
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(vk_code, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0)
    
def sarki_duraklat():
    try:
        keyboard.send("play/pause media")
        return "Şarkı duraklatıldı ya da devam ettirildi."
    except:
        return "Duraklatma sırasında bir hata oluştu."

def sarki_onceki():
    try:
        keyboard.send("previous track")
        return "Önceki şarkı çalınıyor."
    except:
        return "Önceki şarkıya geçilemedi."

def sarki_sonraki():
    try:
        keyboard.send("next track")
        return "Sonraki şarkı çalınıyor."
    except:
        return "Sonraki şarkıya geçilemedi."


#def _odaklan_ve_tus_bas(title_kismi, tuslar):
#    for pencere in gw.getWindowsWithTitle(title_kismi):
#        if pencere.isMinimized:
#            pencere.restore()
#        pencere.activate()
#        time.sleep(0.5)
#        pyautogui.hotkey(*tuslar)
#        return True
#    return False
#Nefret ediyorum böyle alıntıya almaktan çok düzensiz



#def sarki_duraklat():
    #return _odaklan_ve_tus_bas("YouTube Music", ["k"])

#def sarki_sonraki():
    #return _odaklan_ve_tus_bas("YouTube Music", ["shift", "n"])

#def sarki_onceki():
    #return _odaklan_ve_tus_bas("YouTube Music", ["shift", "p"])    
    #Çok daha estetik değil mi sence de?