from flask import Blueprint
from flask import current_app as app
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_restful import abort
from flask_restful import Api
from flask_restful import reqparse
from flask_restful import Resource
from functools import wraps
from utils import mqtt

import requests


api_bp = Blueprint("api", __name__)
api = Api(api_bp)

parser = reqparse.RequestParser()
parser.add_argument("id", type=str, required=True)
parser.add_argument("type", type=str, required=True)
parser.add_argument("value", type=int, required=True)


def verify_access(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if app.config.get("LOCAL", False):
            return func(*args, **kwargs)
        if not app.config["SKILL_ID"]:
            abort(401)
        try:
            verify_jwt_in_request()
        except NoAuthorizationError:
            abort(401)
        skill_id = get_jwt_identity()
        if skill_id != app.config["SKILL_ID"]:
            abort(401)
        return func(*args, **kwargs)

    return wrapper


class ProtectedResource(Resource):
    method_decorators = [verify_access]

    def get_roller_status(self, blind):
        response = requests.get("http://{ip}/roller/0".format(ip=blind.get("ip")))
        if not response.ok:
            app.logger.error(
                'Unable to retrieve status of Blind "{id}" ({ip}): {reason}'.format(
                    blind.get("id"), blind.get("ip"), response.reason
                )
            )
            return {}
        return response.json()


class Blinds(ProtectedResource):
    def get(self):
        res = []
        for blind in app.config.get("BLINDS", []):
            blind_infos = blind.copy()
            response = requests.get("http://{ip}/roller/0".format(ip=blind.get("ip")))
            roller_status = self.get_roller_status(blind=blind)
            if roller_status:
                blind_infos["action"] = roller_status.get("state")
                blind_infos["position"] = roller_status.get("current_pos")
            del blind_infos["ip"]
            res.append(blind_infos)
        return res


class Announce(ProtectedResource):
    def get(self):
        # force all shellies to announce their status
        mqtt.publish("shellies/command", "announce")
        return "", 204


class Update(ProtectedResource):
    def get(self):
        # force all shellies to announce their status
        mqtt.publish("shellies/command", "update")
        return "", 204


class Command(ProtectedResource):
    def publish(self, id, command):
        mqtt.publish("shellies/{id}/roller/0/command".format(id=id), command)

    def get(self, id, command):
        if command not in ["close", "open", "stop", "rc"]:
            return (
                {"message": 'Valid commands are "close", "open", "stop" or "rc"'},
                400,
            )
        if id == "all":
            for blind in app.config.get("BLINDS", []):
                self.publish(id=blind.get("id", ""), command=command)
        else:
            self.publish(id=id, command=command)
        return "", 204


class SkillCommand(ProtectedResource):
    def publish(self, id, value):
        mqtt.publish("shellies/{id}/roller/0/command/pos".format(id=id), value)

    def get_blind_infos(self, id):
        for blind in app.config.get("BLINDS", []):
            return blind
        return None

    def post(self):
        args = parser.parse_args(strict=True)
        if args["type"] == "SetRangeValue":
            self.publish(id=args["id"], value=args["value"])
            return {"position": args["value"]}
        blind = self.get_blind_infos(id=args["id"])
        roller_status = self.get_roller_status(blind=blind)
        new_position = roller_status["current_pos"] + args["value"]
        if new_position < 0:
            new_position = 0
        elif new_position > 100:
            new_position = 100
        self.publish(id=args["id"], value=new_position)
        return {"position": new_position}


class Position(ProtectedResource):
    def publish(self, id, value):
        mqtt.publish("shellies/{id}/roller/0/command/pos".format(id=id), value)

    def get(self, id, value):
        if id == "all":
            for blind in app.config.get("BLINDS", []):
                self.publish(id=blind.get("id", ""), value=value)
        else:
            self.publish(id=id, value=value)
        return "", 204


api.add_resource(Command, "/roller/<string:id>/<string:command>")
api.add_resource(Position, "/roller/<string:id>/position/<int:value>")
api.add_resource(SkillCommand, "/blind/position")
api.add_resource(Announce, "/announce")
api.add_resource(Blinds, "/blinds")
api.add_resource(Update, "/update")
