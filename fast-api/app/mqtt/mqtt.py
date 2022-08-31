from paho.mqtt.client import Client
import random

broker = "127.0.0.1"
port = 1883
topic = "mqtt"
client_id = f"python-mqtt-{random.randint(0,10000)}"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
    else:
        print("Failed to connect, return code %d\n", rc)


def on_message(client, userdata, msg):
    print(f"Received '{msg.payload.decode()}' from topic: '{msg.topic}'")


class MQTTManager:
    def __init__(self) -> None:
        self._mqtt = Client(client_id)
        self._mqtt.on_connect = on_connect
        print("MQTT try connect")
        self._mqtt.connect(broker, port)

    def sub(self, topic: str):
        self._mqtt.subscribe(topic)
        self._mqtt.on_message = on_message

    def pub(self, topic: str, msg: str):
        result = self._mqtt.publish(topic, msg)
        if result[0] == 0:
            print(f"send '{msg}' to topic '{topic}'")
        else:
            print(f"Failed to send message to topic '{topic}'")
