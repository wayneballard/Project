# sense_server.py
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from sense_hat import SenseHat
import threading
import time
import math
import collections

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)

sense = SenseHat()
time.sleep(1)

# Shared state (protected by lock)
_state_lock = threading.Lock()
# we'll expose data as a list of items (client doesn't need to know length)
_latest_list = []
# store rgb matrix as 8x8 list-of-lists or flat 64 list
_latest_matrix = []
# joystick events (most recent first)
_joystick_events = collections.deque(maxlen=50)

# Sampling interval (seconds) - ensure <= 1.0 to satisfy requirement 6
SAMPLING_INTERVAL = 0.5  # 500 ms


def read_sensors_once():
    """
    Read everything from Sense HAT and return as Python structures.
    We'll return a *list* of sensor entries so the client does not need to know length.
    Each entry is a dict: { "id": "...", "label": "...", "value": ..., "unit": "..." }
    """
    # Basic sensors
    temp = sense.get_temperature()
    hum = sense.get_humidity()
    pres = sense.get_pressure()

    # IMU raw
    accel = sense.get_accelerometer_raw()
    mag = sense.get_compass_raw()
    gyro = sense.get_gyroscope_raw()
    orientation = sense.get_orientation()  # pitch/roll/yaw in degrees by default

    # Orientation variants (radians)
    orientation_rad = {
        "roll": math.radians(orientation["roll"]),
        "pitch": math.radians(orientation["pitch"]),
        "yaw": math.radians(orientation["yaw"]),
    }

    # RGB matrix (flat ordered list of 64 [r,g,b] values)
    pixels = sense.get_pixels()  # returns list of 64 [r,g,b]
    # joystick events since last read are collected separately (see background joystick poller)
    # Compose the list (unknown length)
    results = []

    # Add sensors (each as separate item)
    results.append({"id": "temperature", "label": "Temperature", "value": temp, "unit": "°C"})
    results.append({"id": "humidity", "label": "Humidity", "value": hum, "unit": "%"})
    results.append({"id": "pressure", "label": "Pressure", "value": pres, "unit": "hPa"})

    # IMU groups - we can include nested dicts as value
    results.append({
        "id": "accelerometer_raw",
        "label": "Accelerometer (raw)",
        "value": {"x": accel["x"], "y": accel["y"], "z": accel["z"]},
        "unit": "g"
    })
    results.append({
        "id": "magnetometer_raw",
        "label": "Magnetometer (raw)",
        "value": {"x": mag["x"], "y": mag["y"], "z": mag["z"]},
        "unit": "μT"
    })
    results.append({
        "id": "gyroscope_raw",
        "label": "Gyroscope (raw)",
        "value": {"x": gyro["x"], "y": gyro["y"], "z": gyro["z"]},
        "unit": "°/s"
    })
    results.append({
        "id": "orientation_degrees",
        "label": "Orientation",
        "value": {"roll": orientation["roll"], "pitch": orientation["pitch"], "yaw": orientation["yaw"]},
        "unit": "°"
    })
    results.append({
        "id": "orientation_radians",
        "label": "Orientation (radians)",
        "value": orientation_rad,
        "unit": "rad"
    })

    # RGB matrix as a single item (client can render it)
    results.append({
        "id": "rgb_matrix",
        "label": "RGB Matrix (flat 64)",
        "value": pixels,
        "unit": None
    })

    # joystick recent events included as an item
    with _state_lock:
        events_list = list(_joystick_events)  # copy snapshot

    results.append({
        "id": "joystick_events",
        "label": "Joystick Events (most recent first)",
        "value": events_list,
        "unit": None
    })

    # Add timestamp
    results.append({"id": "timestamp", "label": "Timestamp (unix)", "value": time.time(), "unit": "s"})

    return results


def sampler_thread():
    """Background thread to periodically sample sensors and update shared state."""
    global _latest_list, _latest_matrix
    while True:
        try:
            new_list = read_sensors_once()
            # update shared copy
            with _state_lock:
                _latest_list = new_list
                # matrix is the item with id rgb_matrix
                for it in new_list:
                    if it["id"] == "rgb_matrix":
                        _latest_matrix = it["value"]
                        break
        except Exception as e:
            # don't crash sampler; optionally log
            print("Sampler error:", e)
        time.sleep(SAMPLING_INTERVAL)


def joystick_poller():
    """
    Sense HAT joystick events: we poll get_events() in a loop and append to deque.
    get_events() returns any events since the last call.
    Each event has .direction and .action (pressed, released, held) and .timestamp.
    """
    global _joystick_events
    while True:
        try:
            events = sense.stick.get_events()
            if events:
                with _state_lock:
                    for ev in events:
                        # convert to serializable dict
                        _joystick_events.appendleft({
                            "direction": ev.direction,
                            "action": ev.action,
                            "timestamp": ev.timestamp
                        })
            # small sleep so CPU isn't pegged; joystick events are fast so 50ms is fine
            time.sleep(0.05)
        except Exception as e:
            print("Joystick poller error:", e)
            time.sleep(0.2)


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/sensors", methods=["GET"])
def api_sensors():
    """
    Returns JSON: a LIST of sensor entries, unknown length to the client.
    Client should iterate the list and display items dynamically.
    """
    with _state_lock:
        # return a copy so the client receives a snapshot
        payload = list(_latest_list)
    return jsonify(payload)


@app.route("/api/matrix", methods=["GET"])
def api_matrix_get():
    """Return the current matrix as flat list of 64 [r,g,b]"""
    with _state_lock:
        matrix = list(_latest_matrix)
    return jsonify(matrix)


@app.route("/api/matrix/pixel", methods=["POST"])
def api_matrix_set_pixel():
    """
    Set one pixel.
    JSON body: {"x":int,"y":int,"r":int,"g":int,"b":int}
    Values: x,y in 0..7, r/g/b in 0..255
    """
    payload = request.get_json(force=True)
    try:
        x = int(payload["x"])
        y = int(payload["y"])
        r = int(payload.get("r", 0))
        g = int(payload.get("g", 0))
        b = int(payload.get("b", 0))
    except Exception:
        return jsonify({"error": "invalid payload"}), 400

    if not (0 <= x <= 7 and 0 <= y <= 7):
        return jsonify({"error": "x,y out of range"}), 400
    for c in (r, g, b):
        if not (0 <= c <= 255):
            return jsonify({"error": "color out of range 0-255"}), 400

    sense.set_pixel(x, y, r, g, b)
    # update matrix snapshot immediately
    with _state_lock:
        _latest_matrix = sense.get_pixels()
    return jsonify({"status": "ok"})


@app.route("/api/matrix/pixels", methods=["POST"])
def api_matrix_set_pixels():
    """
    Set entire matrix. Accepts list of 64 color-triplets OR nested 8x8.
    Body: {"pixels": [...]} where pixels length can be 64 or 8 (rows of 8)
    """
    payload = request.get_json(force=True)
    pixels = payload.get("pixels")
    if not pixels:
        return jsonify({"error": "missing pixels"}), 400

    # normalize to flat 64 list
    flat = []
    # if given as 8 rows
    if len(pixels) == 8 and all(len(row) == 8 for row in pixels):
        for row in pixels:
            for pix in row:
                flat.append(pix)
    elif len(pixels) == 64:
        flat = pixels
    else:
        return jsonify({"error": "pixels must be 64 length or 8x8 nested"}), 400

    # validate each pixel is an iterable of 3 ints 0..255
    try:
        validated = []
        for p in flat:
            r, g, b = int(p[0]), int(p[1]), int(p[2])
            for c in (r, g, b):
                if not (0 <= c <= 255):
                    raise ValueError("color out of range")
            validated.append([r, g, b])
    except Exception as e:
        return jsonify({"error": "invalid pixel format: " + str(e)}), 400

    sense.set_pixels(validated)
    with _state_lock:
        _latest_matrix = sense.get_pixels()
    return jsonify({"status": "ok"})


@app.route("/api/matrix/clear", methods=["POST"])
def api_matrix_clear():
    """Clear matrix to black"""
    black = [[0, 0, 0]] * 64
    sense.set_pixels(black)
    with _state_lock:
        _latest_matrix = sense.get_pixels()
    return jsonify({"status": "ok"})


@app.route("/api/joystick/recent", methods=["GET"])
def api_joystick_recent():
    with _state_lock:
        events = list(_joystick_events)
    return jsonify(events)


if __name__ == "__main__":
    # start background threads
    t = threading.Thread(target=sampler_thread, daemon=True)
    t.start()
    j = threading.Thread(target=joystick_poller, daemon=True)
    j.start()

    print("Starting Sense HAT server on http://0.0.0.0:5000 (sampling interval: {:.3f}s)".format(SAMPLING_INTERVAL))
    app.run(host="0.0.0.0", port=5000, threaded=True)
