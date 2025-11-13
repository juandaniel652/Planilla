# update/version_checker.py
import requests

def get_latest_version_info_txt(txt_url):
    try:
        response = requests.get(txt_url, timeout=5)
        if response.status_code == 200:
            data = response.text.strip()
            version, apk_url = data.split('|')
            return {
                "version": version.strip(),
                "apk_url": apk_url.strip()
            }
    except Exception as e:
        print("Error al leer el archivo de versión:", e)
    return None
