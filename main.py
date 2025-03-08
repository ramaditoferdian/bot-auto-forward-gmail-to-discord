import time
from utils.email_reader import baca_email
from datetime import datetime, timedelta

if __name__ == "__main__":
    start_time = datetime.now()  # Waktu mulai program

    try:
        while True:
            # Hitung durasi runtime
            elapsed_time = datetime.now() - start_time
            total_hours = elapsed_time.total_seconds() // 3600
            total_days = elapsed_time.total_seconds() // 86400

            print("=" * 50)
            print(f"[🕒] Service berjalan selama: {int(total_days)} hari, {int(total_hours) % 24} jam")
            print("[🔍] Cek Email...")
            
            baca_email()
            
            print("[⏳] Tunggu 1 jam...\n")
            time.sleep(3600)  # Tunggu 1 jam
    except KeyboardInterrupt:
        print("\n[❌] Program dihentikan secara manual.")
