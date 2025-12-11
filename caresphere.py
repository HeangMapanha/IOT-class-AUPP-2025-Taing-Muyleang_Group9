import urequests as requests
import ujson
import time
from machine import Pin, I2C
import network

# -----------------------------
# Wi-Fi Setup
# -----------------------------
SSID = "Robotic WIFI"
PASSWORD = "rbtWIFI@2025"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    time.sleep(1)
print("Connected:", wlan.ifconfig())

# -----------------------------
# DS3231 RTC
# -----------------------------
class DS3231:
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr

    def _bcd2dec(self, bcd):
        return (bcd >> 4) * 10 + (bcd & 0x0F)

    def get_hhmm(self):
        data = self.i2c.readfrom_mem(self.addr, 0x00, 7)
        hour = self._bcd2dec(data[2])
        minute = self._bcd2dec(data[1])
        return "{:02d}:{:02d}".format(hour, minute)

i2c = I2C(1, scl=Pin(22), sda=Pin(21))
rtc = DS3231(i2c)

# -----------------------------
# Hardware
# -----------------------------
buzzer = Pin(25, Pin.OUT)
ir_sensor = Pin(34, Pin.IN)  # 0 = pill present, 1 = pill removed

# -----------------------------
# Blynk & Telegram Setup
# -----------------------------
BLYNK_TOKEN = "K_qC1E6aGTMyY4Bl6kZFvu_q5sMQucfR"
ALARM_PINS = ["V1", "V2", "V3"]
SILENCE_SWITCH = "V4"

TELEGRAM_TOKEN = "8588263277:AAGKTuvMQFeDe3GiN6MPiy-vSeytM1KZxU4"
TELEGRAM_CHAT_ID = "-1003321386259"

# -----------------------------
# InfluxDB Setup (v1.x)
# -----------------------------
INFLUX_HOST = "http://10.30.0.110:8086"
INFLUX_DB   = "medicine_monitor"
INFLUX_USER = ""
INFLUX_PASS = ""

def send_to_influx(alarm_id, event, patient_id=1, retries=3):
    data = f'pill_status,alarm={alarm_id},patient={patient_id} status="{event}"'
    url = "{}/write?db={}".format(INFLUX_HOST, INFLUX_DB)
    if INFLUX_USER and INFLUX_PASS:
        url += "&u={}&p={}".format(INFLUX_USER, INFLUX_PASS)
    for _ in range(retries):
        try:
            resp = requests.post(url, data=data)
            if resp.status_code == 204:
                print(f"InfluxDB logged: {event} for alarm {alarm_id}")
                return True
        except Exception as e:
            print("InfluxDB POST failed:", e)
        time.sleep(1)
    print(f"Failed to log {event} after {retries} retries")
    return False

# -----------------------------
# Utility functions
# -----------------------------
def hhmm_to_minutes(hhmm):
    h, m = map(int, hhmm.split(":"))
    return h * 60 + m

def get_time_interval(pin):
    try:
        url = f"https://blynk.cloud/external/api/get?token={BLYNK_TOKEN}&{pin}"
        resp = requests.get(url).text.strip()
        parts = resp.split('\x00')
        if len(parts) >= 2:
            start_min = int(parts[0]) // 60
            stop_min  = int(parts[1]) // 60
            return start_min, stop_min
    except:
        pass
    return None, None

def get_switch_state(pin):
    try:
        url = f"https://blynk.cloud/external/api/get?token={BLYNK_TOKEN}&{pin}"
        return requests.get(url).text.strip() == '1'
    except:
        return False

def send_telegram_message(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = ujson.dumps({
            "chat_id": TELEGRAM_CHAT_ID,
            "text": msg,
            "parse_mode": "Markdown"
        })
        headers = {'Content-Type': 'application/json'}
        requests.post(url, data=data, headers=headers)
        print("Telegram sent:", msg)
    except Exception as e:
        print("Failed to send Telegram:", e)

# -----------------------------
# Alarm & pill tracking
# -----------------------------
PULSE_ON  = 800
PULSE_OFF = 800
SILENT_DELAY = 15000
DEBOUNCE_MS = 200

buzzer_state = False
last_toggle = time.ticks_ms()
pill_prev_state = ir_sensor.value() == 0  # fix initial state

num_alarms = len(ALARM_PINS)
pill_taken_flags = [False] * num_alarms
pill_notified_flags = [False] * num_alarms
alarm_active_flags = [False] * num_alarms
silent_alarm_start_ms = [None] * num_alarms
silence_used_flags = [False] * num_alarms
last_ir_change_ms = [0] * num_alarms
alarm_started_flags = [False] * num_alarms  # Track Telegram alarm start

print("Starting timed alarm monitor...")

# -----------------------------
# Main Loop
# -----------------------------
while True:
    now_hhmm = rtc.get_hhmm()
    now_min = hhmm_to_minutes(now_hhmm)
    now_ms = time.ticks_ms()
    pill_present = ir_sensor.value() == 0

    # Get alarm intervals
    alarm_intervals = [get_time_interval(pin) for pin in ALARM_PINS]
    silence_active = get_switch_state(SILENCE_SWITCH)
    alarm_any_active = False

    for idx, (start_min, stop_min) in enumerate(alarm_intervals):
        active = start_min is not None and stop_min is not None and start_min <= now_min < stop_min

        # Alarm just started → Telegram notification
        if active and not alarm_started_flags[idx]:
            send_telegram_message(f"⏰ Alarm {idx+1} started! Time to take your medicine 💊")
            alarm_started_flags[idx] = True

        # Alarm just ended
        if not active and alarm_active_flags[idx]:
            if not pill_taken_flags[idx] and not pill_notified_flags[idx]:
                send_to_influx(idx+1, "missed")
                send_telegram_message(f"⚠️ Alarm {idx+1}: Pill missed")
            # Reset flags for next alarm
            pill_taken_flags[idx] = False
            pill_notified_flags[idx] = False
            silence_used_flags[idx] = False
            silent_alarm_start_ms[idx] = None
            alarm_started_flags[idx] = False

        alarm_active_flags[idx] = active
        if active:
            alarm_any_active = True

    # Pill taken logic with debounce
    for idx, active in enumerate(alarm_active_flags):
        if active and pill_prev_state and not pill_present and not pill_taken_flags[idx]:
            if time.ticks_diff(now_ms, last_ir_change_ms[idx]) > DEBOUNCE_MS:
                send_to_influx(idx+1, "taken")
                send_telegram_message(f"✅ Alarm {idx+1}: Pill taken")
                pill_taken_flags[idx] = True
                pill_notified_flags[idx] = True
                last_ir_change_ms[idx] = now_ms

    pill_prev_state = pill_present

    # Silent mode
    for idx, active in enumerate(alarm_active_flags):
        if active and silence_active and not silence_used_flags[idx]:
            silence_used_flags[idx] = True
            silent_alarm_start_ms[idx] = now_ms

    # Silent reminder
    for idx, active in enumerate(alarm_active_flags):
        if active and silence_used_flags[idx] and silent_alarm_start_ms[idx]:
            if time.ticks_diff(now_ms, silent_alarm_start_ms[idx]) >= SILENT_DELAY:
                if pill_present and not pill_taken_flags[idx]:
                    send_telegram_message(f"🚨⚠️ Alarm {idx+1}: Reminder! You still haven't taken your medicine! 💊")
                silent_alarm_start_ms[idx] = None

    # Buzzer logic
    buzzer_active = any(active and pill_present and not pill_taken_flags[idx] and not silence_used_flags[idx] for idx, active in enumerate(alarm_active_flags))
    if buzzer_active:
        if buzzer_state:
            if time.ticks_diff(now_ms, last_toggle) >= PULSE_ON:
                buzzer.value(0)
                buzzer_state = False
                last_toggle = now_ms
        else:
            if time.ticks_diff(now_ms, last_toggle) >= PULSE_OFF:
                buzzer.value(1)
                buzzer_state = True
                last_toggle = now_ms
    else:
        buzzer.value(0)
        buzzer_state = False

    # Status display
    print("Time:", now_hhmm,
          "| Buzzer:", "ON" if buzzer_state else "OFF",
          "| Alarm Active:", alarm_any_active,
          "| Pill Present:", pill_present,
          "| Pill Taken Flags:", pill_taken_flags,
          "| Notified Flags:", pill_notified_flags,
          "| Silence:", silence_active)

    time.sleep(0.5)

