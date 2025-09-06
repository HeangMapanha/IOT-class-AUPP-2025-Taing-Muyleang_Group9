# IOT-class-AUPP-2025-Taing-Muyleang_Group9

1. Overview
   - Build a small IoT monitoring system using ESP32 + MicroPython.
   - Use a DHT22 sensor for temperature/humidity monitoring and a relay for actuation.
   - System behavior:
      + Send Telegram alerts when temperature exceeds a threshold.
      + Allow remote relay control via Telegram chat commands.
      + Auto turn-off relay when temperature drops below threshold.
  - Apply programming techniques:
      + Periodic sampling of sensor data.
      + Debouncing and simple state machines for reliable control.
  - Develop a chat-based control interface using Telegram Bot API (HTTP requests).
  - Document system design with wiring diagrams, test evidence (screenshots/video), and reflect on reliability and ethics.
  - Evaluate performance and safety:
      + Sampling intervals and API rate limits.
      + Relay loads and power isolation for safe operation.
