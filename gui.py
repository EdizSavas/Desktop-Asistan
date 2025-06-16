from PyQt6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QDialog, QTextEdit, QFrame
)
from PyQt6.QtGui import QIcon, QFont, QPainterPath, QRegion, QColor, QBitmap, QPainter
from PyQt6.QtCore import Qt, QTimer, QRectF
import sys
import os
import json
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QMessageBox
import speech_recognition as sr
from vosk import Model, KaldiRecognizer
import sounddevice as sd
import queue
import numpy as np
import tempfile
import scipy.io.wavfile as wavfile
from faster_whisper import WhisperModel
from config_loader import load_config, get_config_path


config_data = load_config("gui_config")
shortcut_data = load_config("shortcut_config")

path = get_config_path("gui_config")
config_path = get_config_path("shortcut_config")

#base_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
#path = os.path.join(base_dir, "ashborn_gui_config.json")
#config_path = os.path.join(base_dir, "shortcut_config.json")

class ShortcutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ashborn Bilgi Penceresi")
        self.setFixedSize(320, 220)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")

        self.text = QTextEdit(self)
        self.text.setReadOnly(True)
        self.text.setFrameShape(QFrame.Shape.NoFrame)
        self.text.setStyleSheet("""
        QTextEdit {
            background-color: #2e2e2e;
            color: white;
            border-radius: 8px;
            padding: 10px;
            font-family: 'Segoe UI';
            font-size: 13px;
        }

        QScrollBar:vertical {
            background: transparent;
            width: 6px;
            margin: 6px 2px 6px 0px;
            border-radius: 3px;
        }
        QScrollBar::handle:vertical {
            background: #aaaaaa;
            border-radius: 3px;
            min-height: 24px;
        }
        QScrollBar::handle:vertical:hover {
            background: #c8c8c8;
        }
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            background: none;
            height: 0px;
        }
        QScrollBar::add-page:vertical,
        QScrollBar::sub-page:vertical {
            background: none;
        }
        """)

        
        self.text.setFont(QFont("Segoe UI", 12))

        layout = QVBoxLayout()
        layout.addWidget(self.text)
        self.setLayout(layout)
        self.update_shortcuts()
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        dialog_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        dialog_geometry.moveCenter(center_point)
        self.move(dialog_geometry.topLeft())

        
    @staticmethod
    def markdown_to_html(text: str) -> str:
        import re
        text = re.sub(r"\*(.*?)\*", r'<span style="color:#b48eed; font-weight:bold">\1</span>', text)
        text = text.replace("\n", "<br>")
        return text

    def update_shortcuts(self):
        try:
            from config_loader import load_config
            data = load_config("shortcut_config")
            kısayol = data.get("drag_shortcut", ["Alt", "LeftButton"])
        except:
            kısayol = ["Alt", "LeftButton"]
            

        self.text.setHtml(f"""
<div style="padding-left: 20px; padding-right: 14px; padding-top: 10px; padding-bottom: 10px;">

<span style="color:#b48eed; font-weight:bold;">§ Temel Kullanım</span><br>
<b>Emir Ver:</b><br>
    •Giriş kutusuna yaz veya mikrofon simgesine tıkla.<br>
    •Komutlar anında çalışır.<br><br>

<b>Komut Geçmişi:</b><br>
    •Yukarı / Aşağı ok tuşlarıyla önceki komutlara geri dön.<br><br>

<span style="color:#b48eed; font-weight:bold;">▣ Genel Arayüz Bilgisi</span><br>
    •Arayüz ekranın sağ alt köşesinde başlar.<br>
    •{self.markdown_to_html(f"{kısayol[0]} + {kısayol[1]}")} ile taşınabilir.<br>
    •Nerede bırakılırsa bir sonraki açılışta orada başlar.<br>
    •Kenarlar yumuşatılmıştır. Her zaman ekranın üstünde kalır.<br><br>

<span style="color:#b48eed; font-weight:bold;">⌘ Kısayollar</span><br>
    •Taşıma/Sürükleme – {kısayol[0]} + {kısayol[1]}<br>
    •Menü aç/kapat – Üç Nokta Butonu<br>
    •Sesli komut başlat – Mikrofon Butonu<br><br>
    •Kısayol değiştirmek için:<br>
    ⤷Sürükleme kısayolunu [istediğiniz bir tuş] + [istediğiniz bir tuş] yap<br><br>

<span style="color:#b48eed; font-weight:bold;">☰ Sistem Komutları</span><br>
    •bilgisayarı kapat<br>
    •yeniden başlat<br>
    •oturumu kapat<br>
    •uyku moduna geç<br>
    •ekranı kilitle<br>
    •sesi aç / sesi kapat<br>
    •görev yöneticisini aç<br>
    •ayarlar panelini aç<br><br>

<span style="color:#b48eed; font-weight:bold;">⮞ Dosya Komutları</span><br>
    •masaüstünü göster<br>
    •belgeleri aç<br>
    •indirilenleri aç<br>
    •ekran görüntüsü al<br>
    •ana dizini aç<br>
    •klasör oluştur: <i>klasör_adı</i><br><br>

<span style="color:#b48eed; font-weight:bold;">⇄ Web Komutları</span><br>
    •google'da ara: <i>sorgu</i><br>
    •youtube'da aç: <i>video adı</i><br>
    •chatgpt'yi aç<br>
    •hava durumu nedir<br><br>

<span style="color:#b48eed; font-weight:bold;">※ Diğer Komutlar</span><br>
    •kendini yeniden başlat<br>
    •yardım ekranını aç<br>
    •kısayolları göster<br><br>

<span style="color:#b48eed; font-weight:bold;">⧉ Ayar Dosyaları</span><br>
    •ashborn_gui_config.json – Konum ve pencere ayarları<br>
    •shortcut_config.json – Kısayollar ve eşleşmeler<br>
    •command_aliases.json – Fuzzy komut kümeleri<br><br>

<span style="color:#888888; font-size:11px;">
    Ashborn v0.6.5 | Ömer Ediz Savaş tarafından geliştirilmiştir. (c) 2025
</span>

</div>
""")
        
        self.text.adjustSize()
        self.setFixedSize(self.text.width() + 240, self.text.height() + 65)
        

class AshbornGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ashborn")
        self.setMinimumSize(460, 110)
        #self.setMinimumSize(420, 100)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        #self.setStyleSheet("background-color: #1e1e1e; border-radius: 14px;")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet(self.setStyleSheet("background: transparent;"))
        
        #Kafam çok karıştı buna ne desem bende bilmiyorum o yüzden saat damgası var --> 05.19
        #Edit: Şuan saat 15.55 ve kafam daha da çok karıştı artık saat damgasını da neden attım bilmiyorum
        
        self.inner_frame = QWidget(self)
        self.inner_frame.setObjectName("AshbornFrame")
        self.inner_frame.setStyleSheet("""
            QWidget#AshbornFrame {
                background-color: #1e1e1e;
                border-radius: 18px;
            }
        """)
        self.inner_frame.setGeometry(0, 0, 460, 110)  

        # Başlık
        self.title_label = QLabel("Komut Verin:", self)
        self.title_label.setFont(QFont("Segoe UI", 12, weight=600))
        self.title_label.setStyleSheet("color: #dddddd; margin-left: 14px;")

        # Giriş kutusu
        self.input = QLineEdit(self)
        self.input.setPlaceholderText("Ashborn dinliyor...")
        self.input.setFont(QFont("Segoe UI", 11))
        self.input.setStyleSheet("background-color: #2e2e2e; color: white; padding: 6px; border-radius: 8px;")
        self.input.returnPressed.connect(self.on_enter)

        # [+] Mikrofon butonu
        button_style_M = """
        QPushButton {
            background-color: #7f5af0;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 3px;
        }
        QPushButton:hover {
            background-color: #6f5ea3;
        }
        """
        self.mic_button = QPushButton("𝄞", self)
        self.mic_button.setFixedWidth(40)
        self.mic_button.setStyleSheet(button_style_M)
        self.mic_button.clicked.connect(self.on_mic)

        # ⋮ Menü butonu
        button_style_I = """
            QPushButton {
                background-color: #7f5af0;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 3px;
            }
            QPushButton:hover {
                background-color: #6f5ea3;
                
            }
        """
        self.menu_button = QPushButton("⋮", self)
        self.menu_button.setFont(QFont("Segoe UI Symbol", 10, QFont.Weight.Bold))
        self.menu_button.setFixedWidth(20)
        self.menu_button.setStyleSheet(button_style_I)
        self.menu_button.clicked.connect(self.show_help)

        # Yanıt alanı, Output, Ne dersen işte
        self.output_label = QLabel("", self)
        self.output_label.setWordWrap(True)
        self.output_label.setStyleSheet("color: #cccccc; margin-left: 14px; margin-right: 14px;")
        self.output_label.setFont(QFont("Segoe UI", 10))

        # Layout
        top_layout = QVBoxLayout()
        top_layout.addWidget(self.title_label)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input)
        input_layout.addWidget(self.mic_button)
        input_layout.addWidget(self.menu_button)

        top_layout.addLayout(input_layout)
        top_layout.addWidget(self.output_label)
        
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.input)
        h_layout.addWidget(self.mic_button)
        h_layout.addWidget(self.menu_button)

        #self.setLayout(top_layout)
        
        #self.setMask(QRegion(self.rect(), QRegion.RegionType.Ellipse))
        self.show
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "ash.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        #self.round_corners()
        self.inner_frame.setLayout(top_layout)
        # Kısayol ve sürükleme
        self.drag_shortcut = self.load_shortcut()
        #self._drag_active = False
        
        self.command_history = []
        self.history_index = -1
        self.move_to_bottom_right()
        QTimer.singleShot(0, self.load_position)
        self.config_path = get_config_path("gui_config")
        self.whisper_model = WhisperModel("base", compute_type="int8")
        
        #shadow = QGraphicsDropShadowEffect(self)
        #shadow.setBlurRadius(20)
        #shadow.setXOffset(0)
        #shadow.setYOffset(4)
        #shadow.setColor(QColor(127, 90, 240))
        #self.setGraphicsEffect(shadow)
        
    #def round_corners(self):
        #rect = QRectF(0, 0, self.width(), self.height())
        #path = QPainterPath()
        #path.addRoundedRect(rect, 20.0, 20.0)  # xRadius, yRadius
        #region = QRegion(path.toFillPolygon().toPolygon())
        #self.setMask(region)

    def load_position(self):
        try:
            with open(self.config_path, "r") as f:
                data = json.load(f)
            x, y = data.get("position", [None, None])
            print(f"[DEBUG] Pozisyon yüklendi: {x}, {y}")
            if x is not None and y is not None:
                self.move(x, y)
            else:
                self.move_to_bottom_right()
        except Exception as e:
            print(f"[!] Pozisyon yüklenemedi: {str(e)}")
            self.move_to_bottom_right()


    def move_to_bottom_right(self):
        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.width() - self.width() - 10
        y = screen.height() - self.height() - 10
        self.move(x, y)

    def load_shortcut(self):
        try:
            from config_loader import load_config
            data = load_config("shortcut_config")
            return tuple(data.get("drag_shortcut", ("Alt", "LeftButton")))
        except:
            return ("Alt", "LeftButton")

    def mousePressEvent(self, event):
        modifiers = QApplication.keyboardModifiers()
        key, btn = self.drag_shortcut

        if key == "Alt" and modifiers & Qt.KeyboardModifier.AltModifier:
            if btn == "LeftButton" and event.button() == Qt.MouseButton.LeftButton:
                self._drag_active = True
                self._drag_pos = event.globalPosition().toPoint()
        
        #key_matched = (
            #(key == "Alt" and modifiers & Qt.KeyboardModifier.AltModifier) or
            #(key == "Ctrl" and modifiers & Qt.KeyboardModifier.ControlModifier) or
            #(key == "Shift" and modifiers & Qt.KeyboardModifier.ShiftModifier)
        #)

        #button_map = {
            #"LeftButton": Qt.MouseButton.LeftButton,
            #"RightButton": Qt.MouseButton.RightButton,
            #"MiddleButton": Qt.MouseButton.MiddleButton,
        #}

        #btn_matched = event.button() == button_map.get(btn, None)

        #if key_matched and btn_matched:
            #self._drag_active = True
            #self._drag_pos = event.globalPosition().toPoint()


    #def mousePressEvent(self, event):
        #modifiers = QApplication.keyboardModifiers()
        #key, btn = self.drag_shortcut
        #if key == "Alt" and modifiers & Qt.KeyboardModifier.AltModifier:
            #if btn == "LeftButton" and event.button() == Qt.MouseButton.LeftButton:
                #self._drag_active = True
                #self._drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if getattr(self, "_drag_active", False):
            current_pos = event.globalPosition().toPoint()
            delta = current_pos - self._drag_pos
            self.move(self.pos() + delta)
            self._drag_pos = current_pos

    def mouseReleaseEvent(self, event):
        self._drag_active = False
        self.save_position()

    def on_enter(self):
        from command_handler import komudu_al
        komut = self.input.text().strip()
        if komut:
            yanit = komudu_al(komut, gui_ref=self)
            self.output_label.setText(f"Ashborn: {yanit}")
            self.input.clear()
            self.output_label.adjustSize()
            new_height = self.output_label.height() + 90
            self.resize(self.width(), new_height)
        
        if komut and (not self.command_history or self.command_history[-1] != komut):
            self.command_history.append(komut)
        self.history_index = len(self.command_history)

    @staticmethod
    def get_preferred_microphone():
        devices = sd.query_devices()
        input_devices = [(i, dev) for i, dev in enumerate(devices) if dev['max_input_channels'] > 0]

        for i, dev in input_devices:
            name_lower = dev['name'].lower()
            if any(keyword in name_lower for keyword in ["mic", "microphone", "input", "kulaklık"]):
                print(f"[+] Mikrofon seçildi: {dev['name']} (ID {i})")
                return i

        if input_devices:
            print(f"[+] Varsayılan mikrofon: {input_devices[0][1]['name']} (ID {input_devices[0][0]})")
            return input_devices[0][0]

        print("[-] Mikrofon bulunamadı!")
        return 

    def on_mic(self):
        uyarı = QMessageBox()
        uyarı.setWindowTitle("Deneysel Özellik")
        uyarı.setText("Bu özellik deneysel bir durumdadır. Hata payı yüksektir ve komutları doğru algılayamayabilir. Devam etmek istiyor musunuz?")
        uyarı.setIcon(QMessageBox.Icon.Warning)
        uyarı.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        uyarı.setStyleSheet("""
            QMessageBox {
                background-color: #1e1e1e;
                color: white;
                font-family: 'Segoe UI';
                font-size: 11pt;
            }
            QPushButton {
                background-color: #7f5af0;
                color: white;
                border-radius: 4px;
                padding: 4px 8px;
            }
            QPushButton:hover {
                background-color: #6f5ea3;
            }
        """)
        cevap = uyarı.exec()

        if cevap != QMessageBox.StandardButton.Yes:
            return
            
        self.output_label.setText("Ashborn: Dinliyorum...")

        duration = 7  
        samplerate = 16000
        #device_id = AshbornGUI.get_preferred_microphone()
        device_id = 2
        
        if device_id is None:
            self.output_label.setText("Ashborn: Mikrofon bulunamadı.")
            return

        try:
            audio = sd.rec(int(duration * samplerate), samplerate=samplerate,
                            channels=1, dtype='int16', device=device_id)
            sd.wait()
            print("[+] Kayıt tamamlandı.")

            audio = np.squeeze(audio).astype(np.float32) / 32768.0

            if np.max(audio) < 0.01:
                self.output_label.setText("Ashborn: Ses algılanmadı.")
                print("[WARN] Ses çok düşük geldi.")
                return

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                wavfile.write(f.name, samplerate, audio)
                wav_path = f.name

            segments, info = self.whisper_model.transcribe(wav_path, language="tr")
            komut = "".join([segment.text for segment in segments]).strip()

            if komut:
                print(f"[+] Algılanan komut: {komut}")
                self.input.setText(komut)
                self.on_enter()
            else:
                self.output_label.setText("Ashborn: Komut anlaşılamadı.")
        except Exception as e:
            self.output_label.setText(f"Ashborn: Hata oluştu ({str(e)})")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Up:
            if self.command_history and self.history_index > 0:
                self.history_index -= 1
                self.input.setText(self.command_history[self.history_index])
        elif event.key() == Qt.Key.Key_Down:
            if self.command_history and self.history_index < len(self.command_history) - 1:
                self.history_index += 1
                self.input.setText(self.command_history[self.history_index])
            else:
                self.history_index = len(self.command_history)
                self.input.clear()
        
        elif event.key() == Qt.Key.Key_F12:
            self.test_kayit()

    def test_kayit(self):
        import sounddevice as sd
        from scipy.io.wavfile import write
        import numpy as np

        samplerate = 16000
        duration = 5 
        device = AshbornGUI.get_preferred_microphone() 

        print("[DEBUG] Kayıt başlıyor...")
        recording = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16', device=device)
        sd.wait()
        print("[DEBUG] Kayıt tamamlandı.")

        write("kayit.wav", samplerate, recording)
        print("[DEBUG] Dosya kaydedildi: kayit.wav")
        

    def show_help(self):
        dialog = ShortcutDialog(self)
        dialog.exec()
    
    def closeEvent(self, event):
        try:
            pos = self.pos()
            with open(self.config_path, "w") as f:
                json.dump({"position": [pos.x(), pos.y()]}, f, indent=4)
            print(f"[DEBUG] Pozisyon kaydedildi: {pos.x()}, {pos.y()}")
        except Exception as e:
            print(f"[!] Pozisyon kaydedilemedi: {str(e)}")
        event.accept()

    
    def save_position(self):
        try:
            pos = self.pos()
            with open(self.config_path, "w") as f:
                json.dump({"position": [pos.x(), pos.y()]}, f, indent=4)
            print(f"[+] Pozisyon kaydedildi: ({pos.x()}, {pos.y()})")
        except Exception as e:
            print("[!] Pozisyon kaydedilemedi:", e)

if __name__ == "__main__":
    print("[DEBUG] Mikrofon test ediliyor...")
    if AshbornGUI.get_preferred_microphone() is None:
        print("[FATAL] Mikrofon algılanamadı. Uygulama başlamayacak.")
        sys.exit(1)
        
    app = QApplication(sys.argv)
    gui = AshbornGUI()
    gui.show()
    sys.exit(app.exec())
    