from flask import Flask, request, jsonify
import threading
import time

app = Flask(__name__)
lock = threading.Lock()
channel_busy = False
current_sender = None
collision = False

@app.route("/sense", methods=["GET"])
def sense():
    return jsonify({"busy": channel_busy})

@app.route("/transmit", methods=["POST"])
def transmit():
    global channel_busy, current_sender, collision
    sender = request.json.get("sender")
    with lock:
        if not channel_busy:
            channel_busy = True
            current_sender = sender
            return jsonify({"status": "ok"})
        else:
            if current_sender != sender:
                collision = True
            return jsonify({"status": "busy"})

@app.route("/stop", methods=["POST"])
def stop():
    global channel_busy, current_sender, collision
    sender = request.json.get("sender")
    with lock:
        if current_sender == sender:
            status = "collision" if collision else "success"
            channel_busy = False
            current_sender = None
            collision = False
            return jsonify({"status": status})
        return jsonify({"status": "not_owner"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
