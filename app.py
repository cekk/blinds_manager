# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import Flask
from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from flask_mqtt import Mqtt
from flask_restful import Resource, Api, reqparse, abort
from flask_socketio import SocketIO
from utils import createSocketMessage
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
)
from functools import wraps
import logging
import os
import re

app = Flask(__name__, instance_relative_config=True, static_folder="static/build")
app.config.from_pyfile("config.py")

api_bp = Blueprint("api", __name__)
api = Api(api_bp)
app.register_blueprint(api_bp)

socketio = SocketIO(app)
mqtt = Mqtt(app)
jwt = JWTManager(app)

parser = reqparse.RequestParser()
parser.add_argument("command", type=str, help="")


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    # mqtt.subscribe("shellies/command")
    for blind in app.config.get("BLINDS", []):
        mqtt.subscribe("shellies/{id}/online".format(id=blind.get("id", "")))
        mqtt.subscribe("shellies/{id}/roller/0/pos".format(id=blind.get("id", "")))
        mqtt.subscribe("shellies/{id}/roller/0".format(id=blind.get("id", "")))


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


# @app.route("/", defaults={"path": ""})
# @app.route("/<path:path>")
# def serve(path):
#     if path != "" and os.path.exists(app.static_folder + "/" + path):
#         return send_from_directory(app.static_folder, path)
#     else:
#         app.logger.info("AAAA")
#         app.logger.debug("BBB")
#         app.logger.warning("CCC")
#         app.logger.error("DDD")
#         return send_from_directory(app.static_folder, "index.html")


class ProtectedResource(Resource):
    method_decorators = [jwt_required]

    def check_skill_id(*args, **kwargs):
        if not app.config["SKILL_ID"]:
            abort(401)
        skill_id = get_jwt_identity()
        if skill_id != app.config["SKILL_ID"]:
            abort(401)


class Blinds(ProtectedResource):
    def get(self):
        self.check_skill_id()
        return app.config.get("BLINDS", [])


class Announce(Resource):
    def get(self):
        # force all shellies to announce their status
        mqtt.publish("shellies/command", "announce")
        return "", 204


class Update(Resource):
    def get(self):
        # force all shellies to announce their status
        mqtt.publish("shellies/command", "update")
        return "", 204


class Action(ProtectedResource):
    def publish(self, id, action):
        mqtt.publish("shellies/{id}/roller/0/command".format(id=id), action)

    def get(self, id, action):
        self.check_skill_id()
        if action not in ["close", "open", "stop"]:
            return (
                {"message": 'Valid actions are "close", "open", "stop" or "rc"'},
                400,
            )
        if id == "all":
            for blind in app.config.get("BLINDS", []):
                self.publish(id=blind.get("id", ""), action=action)
        else:
            self.publish(id=id, action=action)
        return "", 204


# class Command(Resource):
#     def post(self):
#         args = parser.parse_args()
#         mqtt.publish("shellies/shellyswitch25-68E5F8/roller/0/command", "close")
#         return {todo_id: todos[todo_id]}


api.add_resource(Blinds, "/blinds")
api.add_resource(Announce, "/announce")
api.add_resource(Update, "/update")
# api.add_resource(Command, "/command")
api.add_resource(Action, "/roller/<string:id>/<string:action>")

if __name__ == "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    socketio.run(app, debug=True, host="0.0.0.0", port=4000)
