import ctypes
from pathlib import Path

def get_user_directories():
    from ctypes.wintypes import HWND, HANDLE, DWORD, LPCWSTR, MAX_PATH

    folders = {
        "Desktop": "{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}",
        "Documents": "{FDD39AD0-238F-46AF-ADB4-6C85480369C7}",
        "Downloads": "{374DE290-123F-4565-9164-39C4925E467B}"
    }

    paths = []
    SHGetKnownFolderPath = ctypes.windll.shell32.SHGetKnownFolderPath
    SHGetKnownFolderPath.argtypes = [ctypes.c_void_p, DWORD, HANDLE, ctypes.POINTER(ctypes.c_wchar_p)]

    for name, guid in folders.items():
        p_path = ctypes.c_wchar_p()
        result = SHGetKnownFolderPath(ctypes.byref(ctypes.create_unicode_buffer(guid)), 0, None, ctypes.byref(p_path))
        if result == 0:
            paths.append(p_path.value)

    return paths