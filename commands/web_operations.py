import webbrowser

def search_google(command: str):
    try:
        query = command.split(":", 1)[1].strip()
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        return f"Google'da aratılıyor: {query}"
    except Exception as e:
        return f"[-] Google araması başarısız: {str(e)}"

def open_chatgpt():
    try:
        webbrowser.open("https://chat.openai.com")
        return "ChatGPT açılıyor."
    except Exception as e:
        return f"[-] ChatGPT açılamadı: {str(e)}"

def search_youtube(command: str):
    try:
        query = command.split(":", 1)[1].strip()
        url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(url)
        return f"YouTube'da aratılıyor: {query}"
    except Exception as e:
        return f"[-] YouTube araması başarısız: {str(e)}"

def show_weather():
    try:
        url = "https://www.google.com/search?q=hava+durumu"
        webbrowser.open(url)
        return "Hava durumu açılıyor."
    except Exception as e:
        return f"[-] Hava durumu açılamadı: {str(e)}"