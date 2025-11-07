import network, time, random
from umqtt.simple import MQTTClient
import ujson  # MicroPython JSON module

SSID = "BMB_Extender"
PASSWORD = "LEI820396"
BROKER = "test.mosquitto.org"
PORT = 1883
CLIENT_ID = b"esp32_random_1"
TOPIC = b"/aupp/esp32/group9"
KEEPALIVE = 30

# WiFi connection function
def wifi_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(SSID, PASSWORD)
        t0 = time.ticks_ms()
        while not wlan.isconnected():
            if time.ticks_diff(time.ticks_ms(), t0) > 20000:
                raise RuntimeError("Wi-Fi connect timeout")
            time.sleep(0.3)
    print("WiFi OK:", wlan.ifconfig())
    return wlan

# MQTT client function
def make_client():
    return MQTTClient(client_id=CLIENT_ID, server=BROKER, port=PORT, keepalive=KEEPALIVE)

def connect_mqtt(c):
    time.sleep(0.5)
    c.connect()
    print("MQTT connected")

# Main loop
def main():
    wifi_connect()
    client = make_client()
    while True:
        try:
            connect_mqtt(client)
            while True:
                # Generate random values for all three fields
                temp = random.randint(0, 100)
                pressure = random.randint(1000, 1020)
                altitude = random.randint(50, 70)
                
                # Send as JSON
                msg = ujson.dumps({
                    "temperature": temp,
                    "pressure": pressure,
                    "altitude": altitude
                })
                
                client.publish(TOPIC, msg)
                print("Sent:", msg)
                time.sleep(5)
        except OSError as e:
            print("MQTT error:", e)
            try:
                client.close()
            except:
                pass
            print("Retrying MQTT in 3s...")
            time.sleep(3)

main()
