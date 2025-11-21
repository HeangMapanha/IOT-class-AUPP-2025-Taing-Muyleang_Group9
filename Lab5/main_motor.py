import network, socket, ure, time
from machine import Pin, PWM
import gp9morning_graf

# --- Wi-Fi ---
WIFI_SSID = "Robotic WIFI"
WIFI_PASS = "rbtWIFI@2025"

def wifi_connect():
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    if not sta.isconnected():
        sta.connect(WIFI_SSID, WIFI_PASS)
        for _ in range(80):
            if sta.isconnected():
                break
            time.sleep(0.25)
    if not sta.isconnected():
        raise RuntimeError("WiFi connect failed")
    print("WiFi:", sta.ifconfig())
    return sta.ifconfig()[0]

# --- L298N pins ---
IN1 = Pin(26, Pin.OUT)
IN2 = Pin(27, Pin.OUT)
ENA = PWM(Pin(25), freq=1000)
PWM_MAX = 1023
_speed_pct = 0
_current_state = "stop"
speed_info = 0  # this will reflect forward/backward speed continuously

# --- Motor control functions ---
def set_speed(pct):
    global _speed_pct
    pct = int(max(0, min(100, pct)))
    _speed_pct = pct
    ENA.duty(int(PWM_MAX * (_speed_pct / 100.0)))
    print("Speed:", _speed_pct, "%")

def motor_forward():
    global _current_state
    IN1.on()
    IN2.off()
    _current_state = "forward"
    print("Motor: Forward")

def motor_backward():
    global _current_state
    IN1.off()
    IN2.on()
    _current_state = "backward"
    print("Motor: Backward")

def motor_stop():
    global _current_state
    IN1.off()
    IN2.off()
    _current_state = "stop"
    print("Motor: Stop")

# --- Update speed_info based on motor state ---
def update_speed_info():
    global speed_info
    if _current_state == "forward":
        speed_info = _speed_pct
    elif _current_state == "backward":
        speed_info = -_speed_pct
    else:
        speed_info = 0

# --- HTTP server ---
HEAD_OK_TEXT = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/plain\r\n"
    "Access-Control-Allow-Origin: *\r\n"
    "Connection: close\r\n\r\n"
)

HEAD_OK_HTML = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/html\r\n"
    "Access-Control-Allow-Origin: *\r\n"
    "Connection: close\r\n\r\n"
)

HEAD_404 = (
    "HTTP/1.1 404 Not Found\r\n"
    "Content-Type: text/plain\r\n"
    "Access-Control-Allow-Origin: *\r\n"
    "Connection: close\r\n\r\nNot Found"
)

HOME_HTML = """<!doctype html><meta name=viewport content="width=device-width,initial-scale=1">
<h3>ESP32 Motor</h3>
<p>
  <a href="/forward"><button>Forward</button></a>
  <a href="/backward"><button>Backward</button></a>
  <a href="/stop"><button>Stop</button></a>
</p>
<p>
  <label>Speed:</label>
  <input id="spd" type="range" min="0" max="100" value="0"
    oninput="fetch('/speed?value='+this.value).then(r=>r.text()).then(console.log);">
</p>
"""

def route(path):
    if path == "/" or path.startswith("/index"):
        return HEAD_OK_HTML + HOME_HTML
    if path.startswith("/favicon.ico"):
        return HEAD_OK_TEXT
    if path.startswith("/forward"):
        motor_forward()
        return HEAD_OK_TEXT + "forward"
    if path.startswith("/backward"):
        motor_backward()
        return HEAD_OK_TEXT + "backward"
    if path.startswith("/stop"):
        motor_stop()
        return HEAD_OK_TEXT + "stop"
    if path.startswith("/speed"):
        m = ure.search(r"value=(\d+)", path)
        if m:
            set_speed(int(m.group(1)))
            return HEAD_OK_TEXT + "speed=" + m.group(1)
        return HEAD_OK_TEXT + "speed?value=0..100"
    print("Unknown path:", path)
    return HEAD_404

def start_server(ip):
    addr = socket.getaddrinfo(ip, 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(3)
    print("HTTP server running at http://%s/" % ip)

    while True:
        try:
            cl, _ = s.accept()
            cl.settimeout(2)
            try:
                req = cl.recv(1024)
                if not req:
                    cl.close()
                    continue
                try:
                    text = req.decode("utf-8", "ignore")
                except:
                    text = str(req)
                first = ""
                for ln in text.split("\r\n"):
                    if ln:
                        first = ln
                        break
                parts = first.split(" ")
                path = parts[1] if len(parts) >= 2 else "/"
                resp = route(path)
                cl.sendall(resp)34
            except OSError as e:
                if getattr(e, "errno", None) != 116:
                    print("Socket error:", e)
            except Exception as e:
                print("Handler error:", e)
            finally:
                try:
                    cl.close()
                except:
                    pass
        except Exception as e:
            print("Accept error:", e)
            time.sleep(0.1)

# --- MQTT sender thread ---
def mqtt_sender_loop():
    global client
    while True:
        try:
            update_speed_info()  # continuously update speed info
            data = {
                "state": _current_state,
                "speed": speed_info
            }
            gp9morning_graf.publish(client, b"/aupp/esp32/gp9/motor", data)
        except OSError as e:
            print("MQTT error:", e)
            print("Reconnecting MQTT...")
            try:
                gp9morning_graf.connect_mqtt(client)
            except Exception as e2:
                print("Reconnect failed:", e2)
        time.sleep(5)  # send every 1 second

# --- Main program ---
if __name__ == "__main__":
    import _thread

    motor_stop()
    set_speed(_speed_pct)

    # Connect WiFi
    ip = wifi_connect()

    # MQTT setup
    client = gp9morning_graf.make_client()
    gp9morning_graf.connect_mqtt(client)

    # Start MQTT thread
    _thread.start_new_thread(mqtt_sender_loop, ())

    # Start HTTP server
    start_server(ip)
