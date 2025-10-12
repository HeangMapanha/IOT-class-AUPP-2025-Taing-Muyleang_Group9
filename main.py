from machine import Pin, SoftI2C, PWM, time_pulse_us
from time import sleep, sleep_us, time, localtime
from machine_i2c_lcd import I2cLcd
import telegram_bot
import _thread
import web_dashboard  # <-- Dashboard module

# ==============================
# --- LCD Setup ----------------
# ==============================
I2C_ADDR = 0x27
i2c = SoftI2C(sda=Pin(27), scl=Pin(14), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

lcd.clear()
lcd.move_to(0, 0)
lcd.putstr("Smart Parking")
lcd.move_to(0, 1)
lcd.putstr("System Ready")
sleep(2)

# ==============================
# --- IR Sensors (Slots) -------
# ==============================
ir_sensor1 = Pin(4, Pin.IN, Pin.PULL_UP)
ir_sensor2 = Pin(16, Pin.IN, Pin.PULL_UP)
ir_sensor3 = Pin(15, Pin.IN, Pin.PULL_UP)

MAX_IDS = [1, 2, 3]
slots = {
    1: {"pin": ir_sensor1, "occupied": False, "id": None, "time_in": None},
    2: {"pin": ir_sensor2, "occupied": False, "id": None, "time_in": None},
    3: {"pin": ir_sensor3, "occupied": False, "id": None, "time_in": None},
}
available_ids = set(MAX_IDS)

# ==============================
# --- Ultrasonic & Servo -------
# ==============================
servo = PWM(Pin(26), freq=50)
TRIG = Pin(12, Pin.OUT)
ECHO = Pin(13, Pin.IN)

SERVO_OPEN_ANGLE = 90
SERVO_CLOSED_ANGLE = 0

current_servo_angle = SERVO_CLOSED_ANGLE

def set_angle(angle):
    min_duty = 40
    max_duty = 115
    duty = int(min_duty + (angle / 180) * (max_duty - min_duty))
    servo.duty(duty)

def move_servo_smooth(target_angle, step=1, delay=0.02):
    global current_servo_angle
    current = current_servo_angle
    if target_angle > current:
        angles = range(current, target_angle + 1, step)
    else:
        angles = range(current, target_angle - 1, -step)
    for a in angles:
        set_angle(a)
        sleep(delay)
    current_servo_angle = target_angle

def distance_cm():
    TRIG.off(); sleep_us(2)
    TRIG.on(); sleep_us(5)
    TRIG.off()
    t = time_pulse_us(ECHO, 1, 30000)
    if t < 0:
        return None
    return (t * 0.0343) / 2.0

# ==============================
# --- Helper Functions ---------
# ==============================
def lcd_show_status():
    free_slots = [f"S{s}" for s, d in slots.items() if not d["occupied"]]
    lcd.clear()
    lcd.move_to(0, 0)
    if len(free_slots) == 0:
        lcd.putstr("FULL")
    elif len(free_slots) == 3:
        lcd.putstr("EMPTY")
    else:
        lcd.putstr("Free: " + " ".join(free_slots))

def format_time(t):
    lt = localtime(t)
    return "{:02d}:{:02d}:{:02d}".format(lt[3], lt[4], lt[5])

def assign_id(slot_num):
    global available_ids
    if available_ids:
        assigned = min(available_ids)
        available_ids.remove(assigned)
        slots[slot_num]["id"] = assigned
        slots[slot_num]["time_in"] = time()
        print(f"[ENTRY] ID {assigned} -> Slot {slot_num}, time_in={format_time(slots[slot_num]['time_in'])}")

def close_ticket(slot_num):
    global available_ids
    assigned = slots[slot_num]["id"]
    if assigned is not None:
        t_in = slots[slot_num]["time_in"]
        t_out = time()
        duration_sec = t_out - t_in
        minutes = int(duration_sec // 60)
        seconds = int(duration_sec % 60)
        fee = (duration_sec / 60) * 0.5

        print(f"[EXIT] ID {assigned} <- Slot {slot_num}")
        print(f"   time_in:  {format_time(t_in)}")
        print(f"   time_out: {format_time(t_out)}")
        print(f"   duration: {minutes}m {seconds}s")
        print(f"   fee:      ${fee:.2f}")

        # Telegram
        try:
            telegram_bot.send_ticket(assigned, slot_num, minutes, seconds, fee)
        except Exception as e:
            print("Telegram send failed:", e)

        # Add to closed tickets for dashboard
        web_dashboard.closed_tickets.append({
            "id": assigned,
            "slot": slot_num,
            "duration": f"{minutes}m {seconds}s",
            "fee": fee,
            "time_out": format_time(t_out)
        })
        if len(web_dashboard.closed_tickets) > 10:
            web_dashboard.closed_tickets.pop(0)

        available_ids.add(assigned)

    slots[slot_num]["id"] = None
    slots[slot_num]["time_in"] = None
    slots[slot_num]["occupied"] = False

# ==============================
# --- Main Loop ----------------
# ==============================
ENTRY_DEBOUNCE = 3
EXIT_GRACE = 1

entry_counters = {1:0, 2:0, 3:0}
exit_counters = {1:0, 2:0, 3:0}
prev_occupied = {1: False, 2: False, 3: False}

def main():
    print("Parking System Running...")

    # Connect Wi-Fi
    try:
        telegram_bot.connect_wifi()
    except Exception as e:
        print("Wi-Fi connection failed:", e)
        return

    # Link slots & closed tickets for dashboard
    web_dashboard.slots = slots
    web_dashboard.closed_tickets = []

    # Start web dashboard
    _thread.start_new_thread(web_dashboard.start_server, ())

    while True:
        # --- IR slot detection ---
        for slot_num, data in slots.items():
            sensor_val = data["pin"].value()
            if sensor_val == 0 and not data["occupied"]:
                entry_counters[slot_num] += 1
                exit_counters[slot_num] = 0
                if entry_counters[slot_num] >= ENTRY_DEBOUNCE:
                    data["occupied"] = True
                    assign_id(slot_num)
            elif sensor_val == 1 and data["occupied"]:
                exit_counters[slot_num] += 1
                entry_counters[slot_num] = 0
                if exit_counters[slot_num] >= EXIT_GRACE:
                    close_ticket(slot_num)
            else:
                entry_counters[slot_num] = 0
                exit_counters[slot_num] = 0

        lcd_show_status()

        # --- Ultrasonic Gate ---
        dist = distance_cm()
        free_slots_exist = any(not d["occupied"] for d in slots.values())
        if dist is not None and dist < 5 and free_slots_exist:
            print("Car detected at entry, opening gate slowly for 5s")
            move_servo_smooth(SERVO_OPEN_ANGLE, step=2, delay=0.03)
            sleep(3)
            move_servo_smooth(SERVO_CLOSED_ANGLE, step=2, delay=0.03)
            print("Gate closed")

        # --- Exit Gate ---
        for slot_num, data in slots.items():
            if prev_occupied[slot_num] and not data["occupied"]:
                print(f"Slot {slot_num} freed, opening exit gate slowly for 8s")
                move_servo_smooth(SERVO_OPEN_ANGLE, step=2, delay=0.03)
                sleep(6)
                move_servo_smooth(SERVO_CLOSED_ANGLE, step=2, delay=0.03)
                print("Exit gate closed")
            prev_occupied[slot_num] = data["occupied"]

        sleep(0.5)

if __name__ == "__main__":
    main()
