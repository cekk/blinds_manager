import re


def createSocketMessage(message):
    blindId = ""
    data = dict(topic=message.topic, payload=message.payload.decode(), id=blindId)
    if message.topic.endswith("online"):
        blindIdExtractor = re.search("shellies\/(.+?)\/online", message.topic)
        if blindIdExtractor:
            blindId = blindIdExtractor.group(1)
            return {
                "event": "online",
                "data": {"id": blindId, "online": message.payload.decode()},
            }
    elif message.topic.endswith("pos"):
        blindIdExtractor = re.search("shellies\/(.+?)\/roller", message.topic)
        if blindIdExtractor:
            blindId = blindIdExtractor.group(1)
            return {
                "event": "position",
                "data": {"id": blindId, "position": message.payload.decode()},
            }
    else:
        blindIdExtractor = re.search("shellies\/(.+?)\/roller\/0", message.topic)
        if blindIdExtractor:
            blindId = blindIdExtractor.group(1)
            return {
                "event": "action",
                "data": {"id": blindId, "action": message.payload.decode()},
            }
