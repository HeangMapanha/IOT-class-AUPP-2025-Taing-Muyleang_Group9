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
### Hardware:
- MicroPython flashed on ESP32 (Upload scripts using Thonny, mpremote, or ampy)

### Software:
- Node-RED Local automation server. Accessible at: http://localhost:1881
- InfluxDB 1.x. Time-series database Running at: [http://127.0.0.1:8086 (http://127.0.0.1:8086)
- Grafana — Visualization dashboard. Accessible at: http://localhost:3000

### Optional:
- MQTT Explorer — inspect and debug MQTT topics
  
## 4. Wiring & Flowcharts
![image_alt](https://raw.githubusercontent.com/mleanggg/IOT-class-AUPP-2025-Taing-Muyleang_Group9/58ed7ae515f08ffe4add90d60fc109a858009232/Lab4/photo_2025-11-07%2023.33.09.jpeg)

![image_alt](https://raw.githubusercontent.com/mleanggg/IOT-class-AUPP-2025-Taing-Muyleang_Group9/6f84a9f2491a0becb7f322c51f3cc7b93f31d23c/Lab4/lab4-flowchart.png)

## 5. Micropython - Thonny
![image_alt](https://raw.githubusercontent.com/mleanggg/IOT-class-AUPP-2025-Taing-Muyleang_Group9/cd87ae613f88a8acdf0427ce706c28cff6100357/Lab4/photo_2025-11-07%2022.30.16.jpeg)

## 6. Node-RED Setup
![image_alt](https://raw.githubusercontent.com/mleanggg/IOT-class-AUPP-2025-Taing-Muyleang_Group9/8ef7093edf461f82014b4ccd530aaba631949381/Lab4/photo_2025-11-07%2022.30.03.jpeg)

## 7. InfluxDB
![image_alt](https://raw.githubusercontent.com/mleanggg/IOT-class-AUPP-2025-Taing-Muyleang_Group9/cd87ae613f88a8acdf0427ce706c28cff6100357/Lab4/photo_2025-11-07%2022.30.14.jpeg)

## 8. Grafana
![image_alt](https://raw.githubusercontent.com/mleanggg/IOT-class-AUPP-2025-Taing-Muyleang_Group9/cd87ae613f88a8acdf0427ce706c28cff6100357/Lab4/photo_2025-11-07%2022.30.12.jpeg)

## 9. Videos
[![My YouTube Video](https://img.youtube.com/vi/n4BJDCQjyTU/hqdefault.jpg)](https://www.youtube.com/watch?v=n4BJDCQjyTU)

