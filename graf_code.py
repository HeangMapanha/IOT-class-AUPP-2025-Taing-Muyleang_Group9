# mqtt_module.py
import network, time
from umqtt.simple import MQTTClient
import json

# ---------------------
# WiFi & MQTT Settings
# ---------------------
SSID = "Robotic WIFI"
PASSWORD = "rbtWIFI@2025"

BROKER = "test.mosquitto.org"
PORT = 1883
CLIENT_ID = b"esp32_client_1"
KEEPALIVE = 30


# ---------------------
# WiFi
# ---------------------
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


# ---------------------
# MQTT
# ---------------------
def make_client():
    return MQTTClient(
        client_id=CLIENT_ID,
        server=BROKER,
        port=PORT,
        keepalive=KEEPALIVE
    )


def connect_mqtt(client):
    time.sleep(0.5)
    client.connect()
    print("MQTT connected")


# ---------------------
# Publish any data
# ---------------------
def publish(client, topic, data):
    """
    Publish ANY data (string, int, dict, sensor reading)
    Automatically converts dict to JSON.
    """
    if isinstance(data, dict):
        msg = json.dumps(data)
    else:
        msg = str(data)

    client.publish(topic, msg)
    print("Sent:", msg)
