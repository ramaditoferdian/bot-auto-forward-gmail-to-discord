import imaplib
import email
import re
from bs4 import BeautifulSoup
from utils.config import EMAIL, PASSWORD, IMAP_SERVER, IMAP_PORT, START_DATE
from utils.discord_notifier import kirim_discord

KATA_KUNCI = [
    # Screening Dokumen
    "recruitment", "rekrutmen", "administrative", "selection", "seleksi", "administrasi",
    "document", "screening", "resume", "CV", "shortlisted", "lolos", "administrasi",
    "review", "dokumen", "accepted", "diterima", "application", "berkas", "requirements", "kelengkapan",

    # Interview
    "interview", "wawancara", "schedule", "jadwal", "invitation", "undangan",
    "user", "technical", "HR", "confirmation", "konfirmasi", "online", "zoom", "google", "meet",

    # Psikotes & Assessment
    "psychological", "psikotes", "aptitude", "kompetensi", "personality", "kepribadian",
    "online", "test", "assessment", "tes",

    # Technical Test
    "technical", "coding", "skill", "practical", "work", "ujian", "praktik", "keterampilan",

    # Medical Check Up
    "medical", "check", "up", "MCU", "health", "screening", "examination", "tes", "kesehatan",

    # Offering
    "offering", "offer", "job", "congratulations", "accepted", "letter", "contract", "sign",
    "join", "date", "onboarding", "final", "result", "employment", "schedule", "penawaran",

    # Umum
    "selection", "result", "process", "application", "announcement", "opportunity", "information",
    "screening", "process", "proses", "lamaran", "tahap", "lowongan"
]

BLACKLIST_KATA_KUNCI = [
    "newsletter", "diskon", "discount", "voucher",
    "penawaran spesial", "special offer", "gratis", "free trial",
    "iklan", "marketing", "affiliate", "flash sale", "limited offer",
    "subscribe", "unsubscribe", "beli sekarang", "buy now",
    "gift", "membership", "donasi", "donation", "kupon"
]


BLACKLIST_PENGIRIM = [
    "noreply", "no-reply", "newsletter", "promo", "marketing", 
    "notification", "customer_service", "support", "info", 
    "robot", "mailer-daemon", "donotreply"
]



def extract_body(part):
    try:
        payload = part.get_payload(decode=True).decode("utf-8", errors="ignore")
        if part.get_content_type() == "text/html":
            soup = BeautifulSoup(payload, "html.parser")
            text = soup.get_text(separator="\n")
        elif part.get_content_type() == "text/plain":
            text = payload
        else:
            return ""

        text = re.sub(r"\n{3,}", "\n\n", text)  
        text = re.sub(r" {2,}", " ", text)  
        return text.strip()
    except:
        return ""

def email_bukan_promosi(sender, body):
    if any(blacklist in sender.lower() for blacklist in BLACKLIST_PENGIRIM):
        return False
    if any(kata in body.lower() for kata in BLACKLIST_KATA_KUNCI):
        return False
    return True

def cek_kata_kunci(body):
    return any(kata.lower() in body.lower() for kata in KATA_KUNCI)

def baca_email():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, f'(UNSEEN SINCE {START_DATE})')
        email_ids = messages[0].split()

        if not email_ids:
            print("[❌] Tidak ada email baru")
            return

        for num in email_ids:
            status, data = mail.fetch(num, "(RFC822)")
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            sender = msg["from"]
            subject = msg["subject"] if msg["subject"] else "(Tidak Ada Subjek)"
            date = msg["date"]
            body = ""

            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() in ["text/html", "text/plain"]:
                        body = extract_body(part)
                        if body:
                            break
            else:
                body = extract_body(msg)

            print(f"[📩] Email dari: {sender} | Tanggal: {date}")

            if email_bukan_promosi(sender, body):
                if cek_kata_kunci(body):
                    kirim_discord(sender, subject, date, body)
                    mail.store(num, "+FLAGS", "\\Seen")
                else:
                    print("[❌] Isi pesan tidak mengandung kata kunci")
                    mail.store(num, "-FLAGS", "\\Seen")
            else:
                print("[🚫] Email promosi diabaikan")
                mail.store(num, "-FLAGS", "\\Seen")

        mail.logout()
    except Exception as e:
        print(f"[⚠️] Error: {e}")
