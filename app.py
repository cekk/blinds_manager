# -*- coding: utf-8 -*-
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_restful import reqparse
from routes.api import api_bp
from routes.frontend import frontend
from utils import createSocketMessage
from utils import mqtt
from utils import socketio

parser = reqparse.RequestParser()
parser.add_argument("command", type=str, help="")


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    if message.payload == "announce":
        #  skip it
        return
    socket_message = createSocketMessage(message)
    if not socket_message:
        return
    socketio.emit(socket_message["event"], socket_message["data"])


@socketio.on("connect")
def connect_handler():
    mqtt.publish("shellies/command", "announce")


def create_app(debug=False, local=False):
    """Create an application."""
    app = Flask(
        __name__, instance_relative_config=True, static_folder="static/build"
    )
    app.config.from_pyfile("config.py")
    Api(api_bp)
    app.register_blueprint(api_bp)

    if local:
        app.config["LOCAL"] = True
        app.register_blueprint(frontend)

    JWTManager(app)
    socketio.init_app(app)
    mqtt.init_app(app)

    for blind in app.config.get("BLINDS", []):
        mqtt.subscribe("shellies/{id}/online".format(id=blind.get("id", "")))
        mqtt.subscribe(
            "shellies/{id}/roller/0/pos".format(id=blind.get("id", ""))
        )
        mqtt.subscribe("shellies/{id}/roller/0".format(id=blind.get("id", "")))

    return app
