import RPi.GPIO as GPIO
import subprocess
import json

FAN_PIN = 14
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT)
pwm = GPIO.PWM(FAN_PIN, 100)
pwm.start(0)

def get_temp():
    out = subprocess.check_output(["vcgencmd", "measure_temp"])
    return float(out.decode().split('=')[1].split("'")[0])

def load_settings():
    with open("settings.json") as f:
        return json.load(f)

def apply_fan_control():
    settings = load_settings()
    temp = get_temp()

    if settings.get("manual_override"):
        pwm.ChangeDutyCycle(settings.get("manual_duty", 0))
        return temp, settings["manual_duty"]

    duty = 0
    for rule in sorted(settings["temp_thresholds"], key=lambda x: x["temp"]):
        if temp >= rule["temp"]:
            duty = rule["duty"]

    pwm.ChangeDutyCycle(duty)
    return temp, duty
