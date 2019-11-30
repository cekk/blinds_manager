from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_mqtt import Mqtt

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("config.py")
api = Api(app)
mqtt = Mqtt(app)

parser = reqparse.RequestParser()
parser.add_argument("command", type=str, help="")


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe("shellies/command")
    for blind in app.config.get("BLINDS", []):
        # mqtt.subscribe("shellies/{id}".format(id=blind.get("id", "")))
        mqtt.subscribe("shellies/{id}/online".format(id=blind.get("id", "")))
        mqtt.subscribe("shellies/{id}/roller/0/pos".format(id=blind.get("id", "")))
        mqtt.subscribe("shellies/{id}/roller/0".format(id=blind.get("id", "")))


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    print("{} - {}".format(message.topic, message.payload))


class HomePage(Resource):
    def get(self):
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


class Open(Resource):
    def get(self, id):
        mqtt.publish("shellies/{id}/roller/0/command".format(id=id), "open")
        return "", 204


class Close(Resource):
    def get(self, id):
        mqtt.publish("shellies/{id}/roller/0/command".format(id=id), "close")
        return "", 204


class Stop(Resource):
    def get(self, id):
        mqtt.publish("shellies/{id}/roller/0/command".format(id=id), "stop")
        return "", 204


class Command(Resource):
    def post(self):
        args = parser.parse_args()
        mqtt.publish("shellies/shellyswitch25-68E5F8/roller/0/command", "close")
        return {todo_id: todos[todo_id]}


api.add_resource(HomePage, "/")
api.add_resource(Announce, "/announce")
api.add_resource(Update, "/update")
api.add_resource(Command, "/command")
api.add_resource(Close, "/<string:id>/close")
api.add_resource(Open, "/<string:id>/open")
api.add_resource(Stop, "/<string:id>/stop")

if __name__ == "__main__":
    app.run(debug=False)
