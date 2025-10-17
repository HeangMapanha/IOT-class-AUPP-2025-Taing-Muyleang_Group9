# 1. Overview
Build a three-slot smart parking system using an ESP32 that:
- detects vehicles at the entry gate with an ultrasonic sensor
- shows available slots on an LCD and opens the servo gate only if space is available
- assigns auto-IDs 1–3 to cars in the order they actually occupy a slot (via IR sensors)
- records time-in and time-out automatically
- calculates the parking fee
- shows live status on a web dashboard hosted by the ESP32
- and sends receipts to Telegram when cars leave.

# 2. Equipments
- ESP32
- IR sensors
- Ultrasonic sensor
- Servo motor
- LCD player
- Prototype board
- Wire

# 3. Usage Instrcutions
- Power on → LCD shows all slots free.
- Car detected → Gate opens if space is available.
- Park the car → ID assigned and displayed on dashboard.
- Check web dashboard (status updates in real-time).
- Remove the car → Fee calculated and Telegram receipt sent.
- Dashboard updates and slot becomes free again.

# 4. Wiring and Flowcharts
![image_alt](https://raw.githubusercontent.com/mleanggg/IOT-class-AUPP-2025-Taing-Muyleang_Group9/f1e2de5aff8e8d27bd9bde92c11acde0603caeaf/mini_project_1/photo_2025-10-14%2020.56.19.jpeg)



# 5. Video

[![My YouTube Video](https://img.youtube.com/vi/020EAW8se9U/hqdefault.jpg)](https://www.youtube.com/watch?v=020EAW8se9U)

