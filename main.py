import time
from utils.email_reader import baca_email

if __name__ == "__main__":
    try:
        while True:
            print("[🔍] Cek Email...")
            baca_email()
            print("[⏳] Tunggu 10 detik...\n")
            time.sleep(10)
    except KeyboardInterrupt:
        print("Program dihentikan secara manual.")
