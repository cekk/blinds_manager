# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import Flask
from flask import current_app
from flask import render_template
from flask import request
from flask_restful import abort
from flask_restful import Api
from flask_restful import reqparse
from flask_restful import Resource
from functools import wraps
from routes.api import api_bp
from routes.frontend import frontend
from utils import createSocketMessage
from utils import mqtt
from utils import socketio

from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
)

import logging
import os
import re

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
    app = Flask(__name__, instance_relative_config=True, static_folder="static/build")
    app.config.from_pyfile("config.py")
    api = Api(api_bp)
    app.register_blueprint(api_bp)

    if local:
        app.config["LOCAL"] = True
        app.register_blueprint(frontend)

    jwt = JWTManager(app)
    socketio.init_app(app)
    mqtt.init_app(app)

    for blind in app.config.get("BLINDS", []):
        mqtt.subscribe("shellies/{id}/online".format(id=blind.get("id", "")))
        mqtt.subscribe("shellies/{id}/roller/0/pos".format(id=blind.get("id", "")))
        mqtt.subscribe("shellies/{id}/roller/0".format(id=blind.get("id", "")))

    return app
