try:
    import usocket as socket
except:
    import socket

import network
from machine import Pin, SoftI2C, time_pulse_us
import dht
import esp
import gc
from machine_i2c_lcd import I2cLcd
from time import sleep, sleep_us
import time
import ure

# --- ESP32 setup ---
esp.osdebug(None)
gc.collect()

ssid = 'Robotic WIFI'
password = 'rbtWIFI@2025'

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)
while not station.isconnected():
    pass
print('Connected, IP:', station.ifconfig()[0])

# --- Pins ---
led = Pin(2, Pin.OUT)
sensor = dht.DHT11(Pin(4))
TRIG = Pin(27, Pin.OUT)
ECHO = Pin(26, Pin.IN)

# --- I2C LCD ---
I2C_ADDR = 0x27
i2c = SoftI2C(sda=Pin(21), scl=Pin(22), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
lcd.clear()

# --- Display control ---
show_distance = False
show_temp = False
custom_text_mode = False
last_custom_text_row1 = ""
last_custom_text_row2 = ""
scroll_pos_row1 = 0
scroll_pos_row2 = 0
last_update = 0

# --- Last valid readings ---
last_temp = None
last_distance = None

# --- Functions ---
def update_lcd(row1="", row2=""):
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr(row1[:16])
    lcd.move_to(0,1)
    lcd.putstr(row2[:16])

def read_sensor():
    try:
        sensor.measure()
        return round(sensor.temperature(),1)
    except OSError:
        return None

def safe_read_sensor():
    global last_temp
    t = read_sensor()
    if t is not None:
        last_temp = t
    return last_temp

def measure_distance():
    TRIG.off(); sleep_us(2)
    TRIG.on(); sleep_us(10)
    TRIG.off()
    t = time_pulse_us(ECHO, 1, 30000)
    if t < 0: return None
    return round((t * 0.0343)/2, 1)

def safe_measure_distance():
    global last_distance
    d = measure_distance()
    if d is not None:
        last_distance = d
    return last_distance

def web_page():
    temp = safe_read_sensor()
    distance = safe_measure_distance()
    gpio_state = "ON" if led.value() == 1 else "OFF"

    html = f"""
    <!DOCTYPE HTML>
    <html>
    <head>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <script>
        function updateData() {{
            fetch("/data").then(response => response.json()).then(data => {{
                document.getElementById('dist').innerText = data.distance;
                document.getElementById('temp').innerText = data.temp;
            }});
        }}
        setInterval(updateData, 2000);
      </script>
      <style>
        html {{ font-family: Arial; text-align:center; }}
        .button {{ background-color:#e7bd3b; border:none; border-radius:4px; color:white; padding:12px 30px; font-size:16px; cursor:pointer; margin:5px; }}
        .button2 {{ background-color:#4286f4; }}
        input[type=text] {{ padding:10px; width:200px; font-size:16px; }}
      </style>
    </head>
    <body>
      <h2>ESP Web Server</h2>
      <p>GPIO state: <strong>{gpio_state}</strong></p>
      <p>
        <a href="/?led=on"><button class="button">LED ON</button></a>
        <a href="/?led=off"><button class="button button2">LED OFF</button></a>
      </p>
      <p>
        <a href="/?lcd=distance"><button class="button {'button2' if show_distance else ''}">Show Distance</button></a>
        <a href="/?lcd=temp"><button class="button {'button2' if show_temp else ''}">Show Temp</button></a>
      </p>
      <p>Distance: <span id="dist">{distance if distance is not None else 'N/A'}</span> cm</p>
      <p>Temperature: <span id="temp">{temp if temp is not None else 'N/A'}</span> °C</p>
      <form action="/" method="get">
        <input type="text" name="custom" placeholder="Enter text for LCD" value="">
        <input type="submit" class="button button2" value="Send">
      </form>
    </body>
    </html>
    """
    return html

# --- Web server ---
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
print("Server running on port 80")

# --- Main loop ---
while True:
    conn, addr = s.accept()
    request = conn.recv(1024)
    request = str(request)
    print('Request:', request)

    # Parse GET params
    match = ure.search(r'GET /(\S*) HTTP', request)
    path = match.group(1) if match else ""

    if path.startswith("?"):
        params = path[1:]
        if "led=on" in params: led.value(1)
        if "led=off" in params: led.value(0)
        if "lcd=distance" in params:
            show_distance = True
            custom_text_mode = False
        if "lcd=temp" in params:
            show_temp = True
            custom_text_mode = False
        if "custom=" in params:
            idx = params.find("custom=")+len("custom=")
            msg = params[idx:].replace("%20"," ")[:64]
            last_custom_text_row1 = msg[:32]
            last_custom_text_row2 = msg[32:]
            custom_text_mode = True
            # Clear sensor display
            show_distance = False
            show_temp = False
            # Redirect browser to clear input
            response = 'HTTP/1.1 303 See Other\nLocation: /\n\n'
            conn.send(response.encode())
            conn.close()
            continue

    # Update LCD every 0.5 sec
    now = time.time()
    if now - last_update >= 0.5:
        scroll_window = 16

        if custom_text_mode:
            # Row 1 scrolling
            if len(last_custom_text_row1) <= scroll_window:
                row1 = last_custom_text_row1
            else:
                row1 = last_custom_text_row1[scroll_pos_row1:scroll_pos_row1+scroll_window]
                scroll_pos_row1 += 1
                if scroll_pos_row1 > len(last_custom_text_row1)-scroll_window:
                    scroll_pos_row1 = 0
            # Row 2 scrolling
            if len(last_custom_text_row2) <= scroll_window:
                row2 = last_custom_text_row2
            else:
                row2 = last_custom_text_row2[scroll_pos_row2:scroll_pos_row2+scroll_window]
                scroll_pos_row2 += 1
                if scroll_pos_row2 > len(last_custom_text_row2)-scroll_window:
                    scroll_pos_row2 = 0
        else:
            # Row 1: distance if active
            if show_distance:
                distance_val = safe_measure_distance()
                row1 = f"Dist:{distance_val} cm"
            else:
                row1 = ""

            # Row 2: temp if active
            if show_temp:
                temp_val = safe_read_sensor()
                row2 = f"T:{temp_val}C" if temp_val is not None else ""
            else:
                row2 = ""

        update_lcd(row1=row1, row2=row2)
        last_update = now

    # AJAX data request
    if path == "data":
        temp_val = safe_read_sensor()
        distance_val = safe_measure_distance()
        data_json = f'{{"distance":"{distance_val if distance_val is not None else "N/A"}","temp":"{temp_val if temp_val is not None else "N/A"}"}}'
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: application/json\n')
        conn.send('Connection: close\n\n')
        conn.sendall(data_json.encode())
        conn.close()
        continue

    # Send main webpage
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response.encode())
    conn.close()

