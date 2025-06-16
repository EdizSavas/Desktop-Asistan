import os
import json

def normalize_button_name(name: str) -> str:
    name = name.lower().replace(" ", "").replace("click", "")
    if name in ["left", "sol"]:
        return "LeftButton"
    elif name in ["right", "sağ"]:
        return "RightButton"
    elif name in ["middle", "orta", "mid"]:
        return "MiddleButton"
    else:
        return name.capitalize()

def set_drag_shortcut(command: str, gui_ref=None) -> str:
    try:
        raw_combo = command.split("sürükleme kısayolunu")[1].split("yap")[0].strip()
        if "+" not in raw_combo:
            return "Format: sürükleme kısayolunu alt+left yap"

        mod, buton_raw = [x.strip() for x in raw_combo.split("+")]
        buton = normalize_button_name(buton_raw)
        mod = mod.capitalize()

        config_path = os.path.join(os.path.dirname(__file__), "..", "shortcut_config.json")
        config_path = os.path.abspath(config_path)

        with open(config_path, "r") as f:
            data = json.load(f)
        data["drag_shortcut"] = [mod, buton]
        with open(config_path, "w") as f:
            json.dump(data, f, indent=4)

        if gui_ref:
            gui_ref.drag_shortcut = (mod, buton)

        return f"Sürükleme kısayolu {mod} + {buton} olarak güncellendi."

    except Exception as e:
        return f"[-] Kısayol güncelleme hatası: {e}"
