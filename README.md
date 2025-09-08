class-AUPP-2025-Taing-Muyleang_Group9

# 1. Overview

   In this lab, you will build a tiny IoT monitoring node with an ESP32, DHT22 temperature/humidity sensor, and a relay. The ESP32 sends Telegram alerts when the temperature rises above a threshold and lets users control the relay via chat commands. Once the temperature drops below the threshold again, the relay turns off automatically.

# 2. Learning Outcomes (CLO Alignment)
   - Design & implement an IoT system using ESP32 + MicroPython (sensing, actuation, networking).
   - Apply programming techniques for periodic sampling, debouncing, and simple state machines.
   - Develop a chat-based remote control application using Telegram Bot API (HTTP requests).
   - Document & present system design, wiring, and test evidence (screenshots/video), and reflect on reliability/ethics.
   - Evaluate performance (sampling interval, rate limits) and safety (relay loads, power isolation).
   
# 3. Equipment
   - ESP32 Dev Board (MicroPython firmware flashed)
   - DHT22 sensor
   - Relay module
   - jumper wires
   - USB cable + laptop with Thonny
   - Wi-Fi access (internet)

# 4. Wiring
   ![image_alt](https://github.com/HeangMapanha/IOT-class-AUPP-2025-Taing-Muyleang_Group9/blob/main/Pictures/Materials.png?raw=true)

# 5. Tasks

   ### Task 1: Sensor Read and Print
   > - Read DHT22 every 5 seconds and print the temperature and humidity with 2 decimals.
   > - Serial Screenshot:
   ![image_alt](https://github.com/HeangMapanha/IOT-class-AUPP-2025-Taing-Muyleang_Group9/blob/main/Pictures/message%233.jpeg?raw=true)
   

   ### Task 2: Telegram Send
   > - Implement send_message() and post a test message to your group.
   > - Screenshot:
   ![image_alt](https://github.com/HeangMapanha/IOT-class-AUPP-2025-Taing-Muyleang_Group9/blob/main/Pictures/message%233.jpeg?raw=true)

   
   ### Task 3: Bot command
   > - Implement /status to reply with current T/H and relay state.
   > - Implement /on and /off to control the relay.

   ![image_alt](https://github.com/HeangMapanha/IOT-class-AUPP-2025-Taing-Muyleang_Group9/blob/main/Pictures/message%231.jpeg?raw=true)
   ![image_alt](https://github.com/HeangMapanha/IOT-class-AUPP-2025-Taing-Muyleang_Group9/blob/main/Pictures/message%232.jpeg?raw=true)


   ### Task 4: Bot Command
   > - No messages while T < 30 °C.
   > - If T ≥ 30 °C and relay is OFF, send an alert every loop (5 s) until /on is received.
   > - After /on, stop alerts. When T < 30 °C, turn relay OFF automatically and send a one-time “auto-OFF” notice.
   Short video: N/A ( will provide later)

   ### Task 5: Robustness
   > - Auto-reconnect Wi-Fi when dropped.
   > - Handle Telegram HTTP errors (print status; skip this cycle on failure).
   > - Avoid crashing on DHT OSError (skip cycle).
   ![image_alt](https://github.com/HeangMapanha/IOT-class-AUPP-2025-Taing-Muyleang_Group9/blob/main/Pictures/codepic.jpeg?raw=true)


   ### Task 6-Document
   > - README.md with wiring diagram/photo, configuration steps (token, chat id), and usage instructions.
   > - Include a block diagram or flowchart of your loop/state.

   - Wiring diagram
     
   ![image_alt](https://github.com/HeangMapanha/IOT-class-AUPP-2025-Taing-Muyleang_Group9/blob/main/Pictures/wiring.png?raw=true)


   - Configuration steps:
     + Add your bot token to BOT_TOKEN
     + Add your chatID or groupID to ALLOWED_CHAT_ID
     + Add your Wifi and password for the hardware to connect
   
   - Usage Instruction:
     1. Upload code to ESP32 and run.
     2. Use Telegram commands:
        + /on → Stop alerts
        + /off → Relay OFF
        + /status → Show relay + T/H
        + /temp → Get current T/H
        + /whoami → Get your chat ID
      3. Temperature Alerts:
         + ≥ 30°C → Alert every 5s until /on to manual stop the alert
         + < 30°C → after /on (Relay auto-OFF), automatically start alerting above 30°C again
      4. Robustness:
         + Auto Wi-Fi reconnect
         + Skip DHT sensor errors
         + Telegram HTTP error handled
  
   - Diagram and flow chart:
     + block diagram:
       
        ![image_alt](https://github.com/mleanggg/IOT-class-AUPP-2025-Taing-Muyleang_Group9/blob/37489e7743e2e955ed8ebf69fc867a14965bec1a/photo_2025-09-07%2007.44.30.jpeg?raw=true)

       + flow chart
      
       ![image_alt](https://github.com/mleanggg/IOT-class-AUPP-2025-Taing-Muyleang_Group9/blob/b09777d789e0c4d1f8a53f7005c2dd504b27cec4/photo_2025-09-07%2002.29.17.jpeg?raw=true)

    
       
   
   
