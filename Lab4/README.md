## 1. Overview

This project demonstrates a complete IoT pipeline using ESP32, MQTT, Node-RED, InfluxDB, and Grafana. The ESP32 runs MicroPython and sends simulated sensor data (random integers) to an MQTT broker. Node-RED subscribes to the MQTT topic, processes the data, and writes it to InfluxDB, a time-series database. Grafana is then used to visualize the data in a real-time dashboard.

## 2. Learning Income

By completing this project, you will learn:
- How to connect an ESP32 to Wi-Fi and publish MQTT messages using MicroPython.
- Setting up Node-RED flows to receive MQTT data and write it into InfluxDB.
- Creating and querying a time-series database using InfluxDB 1.x (InfluxQL).
- Visualizing real-time data in Grafana dashboards.
- Integrating multiple IoT tools to create a fully functional pipeline.
- Troubleshooting network, MQTT, database, and visualization issues.
## 3. Equipments
Hardware:
- MicroPython flashed on ESP32 (Upload scripts using Thonny, mpremote, or ampy)

Software:
- Node-RED Local automation server. Accessible at: http://localhost:1881
- InfluxDB 1.x. Time-series database Running at: [http://127.0.0.1:8086 (http://127.0.0.1:8086)
- Grafana — Visualization dashboard. Accessible at: http://localhost:3000

Optional:
- MQTT Explorer — inspect and debug MQTT topics
  
## 4. Wiring & Flowcharts

## 5. Micropython - Thonny


## 6. Node-RED Setup

## 7. InfluxDB

## 8. Grafana

## 9. Videos
