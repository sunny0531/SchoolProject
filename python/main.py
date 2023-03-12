import json

from RPi import GPIO
from flask import Flask, request, jsonify

from Config import Setting
from button import Buttons, setup, add_event_detect

app = Flask(__name__)
green = 11
yellow = 13
red = 15
blue = 16
GPIO.setmode(GPIO.BOARD)

setup([green, yellow, red, blue], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
button = Buttons(green, yellow, red, blue)
with open("config.json") as f:
    _setting = Setting(**json.loads(f.read()))
    button.mail_setup(_setting.sender, _setting.password)
add_event_detect([green, yellow, red, blue], GPIO.RISING, callback=button.pressed, bouncetime=300)


@app.route("/setting", methods=["PUT", "GET"])
def setting():
    if request.method == "PUT":
        content = request.get_json(silent=True)
        _setting.__init__(**content)
        button.mail_setup(_setting.sender, _setting.password)
        return "", 200
    elif request.method == "GET":
        return jsonify(_setting.__dict__), 200
    else:
        return "", 405


@app.route("/mail", methods=["POST"])
def send_mail():
    button.send_gmail(_setting.receiver)
    return "", 200

app.run( port=8080, host="0.0.0.0")
GPIO.cleanup()
