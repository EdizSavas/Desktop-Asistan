from PyQt6.QtWidgets import QApplication
from gui import AshbornGUI
import sys, os
from command_handler import komudu_al

log_path = os.path.join(os.path.dirname(__file__), "asistan_startup_log.txt")
with open(log_path, "a") as log:
    log.write("[Asistan başlatılıyor...]\n")

def main():
    print("Kralımızın emirleri için beklemedeyim...")
    
    while True:
        try: 
            kulllanıcı_girdisi = input(">> ")
            cevap = komudu_al(kulllanıcı_girdisi)
            print(cevap)
        except SystemExit:
            break
        except Exception as e:
            print(f"[-] Hata Beklenmeyen bir sorun oluştu: {str(e)}")
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = AshbornGUI()
    gui.show()
    sys.exit(app.exec())
    