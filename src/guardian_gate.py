import time
import requests
import grovepi
import os

# ==============================
# GrovePi Pin Configuration
# ==============================

U1 = 2      # Ultrasonic Sensor 1
U2 = 3      # Ultrasonic Sensor 2
BTN1 = 7    # Button 1
BTN2 = 8    # Button 2
ARM = 4     # Arm/Disarm Toggle Button
BUZ = 5     # Buzzer
LED = 6     # LED


# ==============================
# Telegram Configuration
# ==============================

USE_TELEGRAM = True

# Telegram credentials are loaded from environment variables
# and are NOT stored directly in the source code.
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def tg_send(text):
    """Send a notification message through Telegram."""

    if not USE_TELEGRAM:
        print("[TELEGRAM DISABLED] {}".format(text))
        return

    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[TELEGRAM ERROR] Telegram credentials are not configured.")
        return

    url = "https://api.telegram.org/bot{}/sendMessage".format(
        TELEGRAM_BOT_TOKEN
    )

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }

    try:
        r = requests.post(
            url,
            json=payload,
            timeout=6
        )

        print("[TELEGRAM REPLY]", r.status_code, r.text)

        if r.status_code != 200 or '"ok":true' not in r.text:
            print(
                "[TELEGRAM WARNING] "
                "Check token/chat_id or open bot and press Start."
            )

    except Exception as e:
        print("[TELEGRAM EXCEPTION]", e)


# ==============================
# GrovePi Pin Initialization
# ==============================

for p in (BTN1, BTN2, ARM):
    grovepi.pinMode(p, "INPUT")

for p in (BUZ, LED):
    grovepi.pinMode(p, "OUTPUT")


# ==============================
# Helper Functions
# ==============================

def is_pressed(pin):
    """Read the state of a digital input pin."""

    try:
        return grovepi.digitalRead(pin) == 1
    except:
        return False


def set_output(pin, state):
    """Turn an output device ON or OFF."""

    try:
        grovepi.digitalWrite(pin, 1 if state else 0)
    except:
        pass


def read_ultra(pin):
    """Read distance from an ultrasonic sensor in centimeters."""

    try:
        d = grovepi.ultrasonicRead(pin)

        if d and 0 < d < 300:
            return d

        return None

    except:
        return None


# ==============================
# System Configuration
# ==============================

NEAR1_CM = 30.0
NEAR2_CM = 30.0

ALARM_DURATION_S = 4


# ==============================
# Main Guardian Gate System
# ==============================

def main():

    print("Guardian Gate starting...")

    system_active = False

    last_arm_state = False
    last_msg_time = 0
    last_alarm_time = 0

    # Make sure alarm devices are OFF at startup
    set_output(BUZ, False)
    set_output(LED, False)

    try:

        while True:

            # ------------------------------
            # Arm / Disarm Toggle
            # ------------------------------

            arm_now = is_pressed(ARM)

            if arm_now and not last_arm_state:

                system_active = not system_active

                status = "ACTIVE" if system_active else "STOPPED"

                print("[SYSTEM] {}".format(status))

                tg_send(
                    "Guardian Gate is now {}.".format(status)
                )

                if not system_active:
                    set_output(BUZ, False)
                    set_output(LED, False)

                # Button debounce
                time.sleep(0.25)

            last_arm_state = arm_now


            # ------------------------------
            # Wait if System is Inactive
            # ------------------------------

            if not system_active:

                time.sleep(0.2)

                continue


            # ------------------------------
            # Read Sensors and Buttons
            # ------------------------------

            u1 = read_ultra(U1)
            u2 = read_ultra(U2)

            b1 = is_pressed(BTN1)
            b2 = is_pressed(BTN2)


            print(
                "U1={}cm, U2={}cm, BTN1={}, BTN2={}, ARM={}".format(
                    u1,
                    u2,
                    b1,
                    b2,
                    arm_now
                )
            )


            # ------------------------------
            # Detect Human Presence
            # ------------------------------

            both_near = (
                u1 is not None
                and u1 < NEAR1_CM
                and u2 is not None
                and u2 < NEAR2_CM
            )


            t_now = time.time()


            # ------------------------------
            # Case A:
            # Ultrasonic Sensors Detect Human
            # ------------------------------

            if both_near and (t_now - last_msg_time > 8):

                tg_send(
                    "Someone is in front of the door."
                )

                print(
                    "[INFO] Sent: Someone is in front of the door."
                )

                last_msg_time = t_now


            # ------------------------------
            # Case B:
            # Human + Button Detection
            # ------------------------------

            if (
                both_near
                and (b1 or b2)
                and (t_now - last_alarm_time > 10)
            ):

                tg_send(
                    "Intruder confirmed! LED/Buzzer activated."
                )

                print(
                    "[ALARM] Human + button detected"
                )

                # Activate alarm
                set_output(LED, True)
                set_output(BUZ, True)

                time.sleep(ALARM_DURATION_S)

                # Deactivate alarm
                set_output(LED, False)
                set_output(BUZ, False)

                last_alarm_time = time.time()


            # Small delay before next sensor reading
            time.sleep(0.2)


    except KeyboardInterrupt:

        print("System interrupted by user.")


    finally:

        # Always turn off alarm devices when exiting
        set_output(BUZ, False)
        set_output(LED, False)

        print("Exiting cleanly.")


# ==============================
# Program Entry Point
# ==============================

if __name__ == "__main__":
    main()

