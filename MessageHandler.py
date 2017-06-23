import paho.mqtt.client as mqtt
import json
import datetime
from GarageDoor import GarageDoor
from SystemStats import SystemStats

class MessageHandler(object):
    def __init__(self,broker_address="10.0.0.11"):
        self.broker_address = broker_address
        self.client = mqtt.Client('gdcontroller')
        self.commandTopic = "GDCTL/COMMAND"
        self.statusTopic = "GDCTL/STATUS"
        self.doorStatusTopic = "HHB/STATUS"
        self.garageDoors = {1: GarageDoor(1), 2: GarageDoor(2)}

    def on_connect(self, client, userdata, flags, rc):
        print 'Connected to broker at ', self.broker_address
        m = 'Connected flags' +str(flags) + ' result code ' + str(rc) + 'client1_id ' + str(client)
        print(m)

    def on_message(self, client, userdata, message):
        payload = str(message.payload.decode("utf-8"))
        # print 'message received ', payload
        try:
            jsonPayload = json.loads(payload)
            #
            # is this a command to open or close the door?
            if jsonPayload["topic"] == self.commandTopic:
                date_time = jsonPayload["datetime"]
                door_id = jsonPayload["doorID"]
                command = jsonPayload["command"]
                print 'Command received on', date_time, ' for door ', door_id, ' command: ', command
                if command.upper() == 'OPEN':
                    self.garageDoors.get(door_id).do_open_door()
                elif command.upper() == 'CLOSE':
                    self.garageDoors.get(door_id).do_close_door()
                elif command.upper() == 'TRIGGER':
                    self.garageDoors.get(door_id).do_trigger_door()
            #
            # is this a HHB Door Status message?
            elif jsonPayload['topic'] == self.doorStatusTopic:
                pass
        except:
            # print 'Error trying to convert message to json '
            # print 'You havent fixed the json payload in HHB yet, have you?'
            try:
                jsonStart = payload.index('{')
                jsonPayload = payload[jsonStart:]

                jsonPayload = json.loads(jsonPayload)
                device_type = jsonPayload['deviceType']
                if device_type == 24:
                    door_state = jsonPayload['state'].upper()
                    if 'CLOSE' in door_state:
                        self.garageDoors.get(1).set_closed(jsonPayload['datetime'])
                    elif 'OPEN' in door_state:
                        self.garageDoors.get(1).set_opened(jsonPayload['datetime'])
            except:
                print 'Second Error trying to convert message to json'

    def start(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker_address)
        self.client.subscribe(self.commandTopic,0)
        self.client.subscribe(self.doorStatusTopic,0)
        self.client.loop_start()

    def cleanup(self):
        self.client.unsubscribe(self.commandTopic)
        self.client.unsubscribe(self.doorStatusTopic)
        self.client.disconnect()
        self.client.loop_stop()

    def sendStatusMessage(self):
        print 'Sending a status message'
        data = {}
        data['topic'] = 'GDCTL/STATUS'
        data['datetime'] = datetime.datetime.now().replace(microsecond=0).isoformat()
        data['system'] = SystemStats().asJSON()
        data['door'] = self.garageDoors.get(1).asJSON()
        json_data = json.dumps(data)
        self.client.publish(self.statusTopic, json_data,qos=0)
