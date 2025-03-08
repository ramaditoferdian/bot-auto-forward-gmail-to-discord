import time
from utils.email_reader import baca_email

if __name__ == "__main__":
    try:
        while True:
            print("[🔍] Cek Email...")
            baca_email()
            print("[⏳] Tunggu 1 jam...\n")
            time.sleep(3600)
    except KeyboardInterrupt:
        print("Program dihentikan secara manual.")
