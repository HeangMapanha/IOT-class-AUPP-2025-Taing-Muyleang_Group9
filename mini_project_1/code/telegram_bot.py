import network, urequests
from machine import Pin
from time import sleep, time

# ==============================
# --- USER CONFIG -------------
# ==============================
WIFI_SSID     = "Robotic WIFI"
WIFI_PASSWORD = "rbtWIFI@2025"

BOT_TOKEN     = "8287456396:AAFqFRyzC2uw0igfOFa4jJjeIAZz13I5WyU"
ALLOWED_CHAT_IDS = {-4964729464}  # Make sure this is correct (group starts with -)

API = "https://api.telegram.org/bot" + BOT_TOKEN
relay = Pin(2, Pin.OUT)

# ==============================
# --- Helper Functions --------
# ==============================
def _urlencode(d):
    parts = []
    for k, v in d.items():
        if isinstance(v, int): v = str(v)
        s = str(v)
        s = s.replace("%", "%25").replace(" ", "%20").replace("\n", "%0A")
        s = s.replace("&", "%26").replace("?", "%3F").replace("=", "%3D")
        parts.append(str(k) + "=" + s)
    return "&".join(parts)

# ==============================
# --- Wi-Fi Connection ---------
# ==============================
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        t0 = time()
        while not wlan.isconnected():
            if time() - t0 > 25:
                raise RuntimeError("Wi-Fi connect timeout")
            sleep(0.25)
    print("Connected to Wi-Fi:", wlan.ifconfig())
    return wlan

# ==============================
# --- Telegram Messaging -------
# ==============================
def send_message(chat_id, text):
    try:
        url = API + "/sendMessage?" + _urlencode({"chat_id": chat_id, "text": text})
        print("Sending Telegram message...")
        print("URL:", url)  # Debug URL
        r = urequests.get(url)
        print("Response:", r.text)  # Debug API response
        r.close()
    except Exception as e:
        print("Telegram send error:", e)

def send_ticket(ticket_id, slot_num, minutes, seconds, fee):
    for chat_id in ALLOWED_CHAT_IDS:
        send_message(chat_id,
            f"✅ Ticket CLOSED\nID: {ticket_id} Slot: S{slot_num}\nDuration: {minutes}m {seconds}s\nFee: ${fee:.2f}")
