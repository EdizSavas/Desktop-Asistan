import customtkinter as ctk
import tkinter
import ctypes
from command_handler import komudu_al
import pyautogui
import os

ico_path = os.path.join(os.path.dirname(__file__), "icon_baby.ico")

with open("gui_boot_log.txt", "a") as f:
    f.write("[+] GUI başlatıldı\n")


class RECT(ctypes.Structure):
    _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long),
                ("right", ctypes.c_long), ("bottom", ctypes.c_long)]

class APPBARDATA(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.c_ulong),
        ("hWnd", ctypes.c_void_p),
        ("uCallbackMessage", ctypes.c_uint),
        ("uEdge", ctypes.c_uint),
        ("rc", RECT),
        ("lParam", ctypes.c_int),
    ]


def get_screen_size():
    screen_width, screen_height = pyautogui.size()
    return screen_width, screen_height

def get_taskbar_position():
    data = APPBARDATA()
    data.cbSize = ctypes.sizeof(APPBARDATA)
    ctypes.windll.shell32.SHAppBarMessage(5, ctypes.byref(data))
    return data.uEdge, (data.rc.left, data.rc.top, data.rc.right, data.rc.bottom)

#def get_taskbar_position():
    #class RECT(ctypes.Structure):
        #_fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long),
                    #("right", ctypes.c_long), ("bottom", ctypes.c_long)]

    #class APPBARDATA(ctypes.Structure):
        #_fields_ = [
            #("cbSize", ctypes.c_ulong),
            #("hWnd", ctypes.c_void_p),
            #("uCallbackMessage", ctypes.c_uint),
            #("uEdge", ctypes.c_uint),
            #("rc", RECT),
            #("lParam", ctypes.c_int),
        #]

    #data = APPBARDATA()
    #data.cbSize = ctypes.sizeof(APPBARDATA)
    #ctypes.windll.shell32.SHAppBarMessage(5, ctypes.byref(data))

    #return {
        #"edge": data.uEdge,
        #"rect": (data.rc.left, data.rc.top, data.rc.right, data.rc.bottom)
    #}


class AshbornGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("")
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(fg_color="#1e1e1e")
        self.geometry("420x60")
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<B1-Motion>", self.do_move)
        self.title("Ashborn")
        try:
            self.iconbitmap(ico_path)
        except Exception as e:
            print(f"[HATA] İkon atanamadı: {e}")

        #self.update_position()
        #self.place_to_taskbar()

        self.input = ctk.CTkEntry(self, placeholder_text="Ashborn dinliyor...", width=300, height=40, font=("Segoe UI", 14))
        self.input.pack(side="left", padx=(15, 0), pady=10)
        self.input.bind("<Return>", self.on_enter)

        self.mic_button = ctk.CTkButton(self, text="🎤", width=40, command=self.on_mic)
        self.mic_button.pack(side="left", padx=10)

        self.output_label = ctk.CTkLabel(self, text="", text_color="#aaaaaa", font=("Segoe UI", 12), wraplength=400)
        self.output_label.pack(side="bottom", pady=(0, 5))

        self.bind("<Escape>", lambda e: self.destroy())

    #def place_to_taskbar(self):
        #edge, rect = get_taskbar_position()
        #x = rect.right - 440
        #y = rect.top - 70 if edge == 3 else rect.bottom + 10
        #self.geometry(f"+{x}+{y}")
        
        # Olmadı çalışmadı ama bir ara gerekebilir
            
    def on_enter(self, event=None):
        komut = self.input.get().strip()
        if komut:
            yanit = komudu_al(komut)
            self.output_label.configure(text=f"Ashborn: {yanit}")
            self.input.delete(0, tkinter.END)

    def on_mic(self):
        print("[DEBUG] GUI konumu güncelleniyor...")
        self.output_label.configure(text="[🎤 Mikrofon simgesi tıklandı (şimdilik pasif)]")
    
    ##def update_position(self):
        #edge, rect = get_taskbar_position()
        #left, top, right, bottom = rect

        #if edge == 3:  # Bottom
            #x = right - 460
            #y = top - 70  # görev çubuğu yukarı çıktığında yukarıya göre konumlanır
        #elif edge == 1:  # Top
            #x = right - 460
            #y = bottom + 10
        #elif edge == 0:  # Left
            #x = right + 10
            #y = bottom - 100
        #elif edge == 2:  # Right
            #x = left - 470
            #y = bottom - 100
        #else:  # bilinmeyen durumlar için yedek plan --- Edit: Bilinmeyen durum olmasa bile çalışmadı
            #x = 100
            #y = 100 #Edit-2: Pythonda gui tasarımı yapmak daraltıyor çok ham çok yüzeysel vakit olsa css kullanırdım 

        #self.geometry(f"+{x}+{y}")
        #self.after(500, self.update_position)
    
    def start_move(self, event):
        self._drag_start_x = event.x_root
        self._drag_start_y = event.y_root
        self._window_start_x = self.winfo_x()
        self._window_start_y = self.winfo_y()

    def do_move(self, event):
        dx = event.x_root - self._drag_start_x
        dy = event.y_root - self._drag_start_y
        new_x = self._window_start_x + dx
        new_y = self._window_start_y + dy
        self.geometry(f"+{new_x}+{new_y}")


    
    #def update_position(self):
        #screen_w, screen_h = get_screen_size()
        #x = screen_w - 460
        #y = screen_h - 90
        #self.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = AshbornGUI()
    app.mainloop()
