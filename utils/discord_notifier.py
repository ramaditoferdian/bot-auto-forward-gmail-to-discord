import requests
from utils.config import DISCORD_WEBHOOK_URL

def kirim_discord(pengirim, subjek, waktu, pesan):
    payload = {
        "content": f"""```
📧 Email Baru 🚨

Pengirim : {pengirim}
Subjek   : {subjek}
Waktu    : {waktu}

Isi Pesan:
{pesan[:1500]}
```"""
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload, headers=headers)

    if response.status_code == 204:
        print("[✅] Pesan berhasil dikirim ke Discord")
    else:
        print(f"[❌] Gagal kirim ke Discord | Status Code: {response.status_code}")
