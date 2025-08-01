from flask import Flask, render_template, request, redirect
from fan import apply_fan_control, load_settings
import json
import threading
import time
import os

SETTINGS_PATH = "settings.json"
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    settings = load_settings()

    if request.method == "POST":
        if request.form["action"] == "add":
            settings["temp_thresholds"].append({"temp": 0, "duty": 0})
        elif request.form["action"] == "update":
            new_rules = []
            for i in range(len(settings["temp_thresholds"])):
                if f"delete_{i}" in request.form:
                    continue
                temp = float(request.form.get(f"temp_{i}", 0))
                duty = int(request.form.get(f"duty_{i}", 0))
                new_rules.append({"temp": temp, "duty": duty})
            settings["temp_thresholds"] = new_rules

        # Manual override
        settings["manual_override"] = "override" in request.form
        settings["manual_duty"] = int(request.form.get("manual_duty", 0))

        with open(SETTINGS_PATH, "w") as f:
            json.dump(settings, f, indent=2)

        return redirect("/")

    temp, duty = apply_fan_control()
    return render_template("index.html", temp=temp, duty=duty, settings=settings)

def background_loop():
    while True:
        apply_fan_control()
        time.sleep(10)

if __name__ == "__main__":
    if not os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, "w") as f:
            json.dump({
                "temp_thresholds": [{"temp": 50, "duty": 70}],
                "manual_override": False,
                "manual_duty": 60
            }, f, indent=2)

    threading.Thread(target=background_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
