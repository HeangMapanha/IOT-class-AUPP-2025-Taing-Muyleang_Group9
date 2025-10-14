# 1. Overview
Build a three-slot smart parking system using an ESP32 that:
• detects vehicles at the entry gate with an ultrasonic sensor,
• shows available slots on an LCD and opens the servo gate only if space is available,
• assigns auto-IDs 1–3 to cars in the order they actually occupy a slot (via IR sensors),
• records time-in and time-out automatically,
• calculates the parking fee,
• shows live status on a web dashboard hosted by the ESP32,
• and sends receipts to Telegram when cars leave.

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

# 4. Wiring and flowcharts


# 5. Video

# 6. Image
