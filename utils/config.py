import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993
START_DATE = "20-Feb-2025"

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")  # Pastikan ini ada!
