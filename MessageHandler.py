import paho.mqtt.client as mqtt
import json
import datetime
from GarageDoor import GarageDoor
from SystemStats import SystemStats
import logging
from collections import OrderedDict



class MessageHandler(object):

    # ------------------------------------------------------------------------------------
    def __init__(self,broker_address='ec2-52-32-56-28.us-west-2.compute.amazonaws.com'):
        self.broker_address = broker_address
        self.client = mqtt.Client('gdcontroller2')
        self.commandTopic = "GDCTL/COMMAND"
        self.statusTopic = "GDCTL/STATUS"
        self.doorStatusTopic = "HHB/STATUS"
        self.garageDoors = {1: GarageDoor(1), 2: GarageDoor(2)}

    # ------------------------------------------------------------------------------------
    def on_connect(self, client, userdata, flags, rc):
        logging.info('Connected to broker at %s', self.broker_address)
        pass

    # ------------------------------------------------------------------------------------
    def on_message(self, client, userdata, message):
        payload = str(message.payload.decode("utf-8"))
        try:
            jsonPayload = json.loads(payload)
            #
            # is this a HHB Door Status message?

            print 'Topic >>>> ', jsonPayload['topic']
            #
            # is this a command to open or close the door?
            if jsonPayload['topic'] == self.commandTopic:
                logging.info('Command received! [%s]', payload)
                print 'Command received!',payload

                date_time = jsonPayload["datetime"]
                door_id = jsonPayload["doorID"]
                command = jsonPayload["command"]
                logging.debug('Command received on %s, for door %s, command %s', date_time, door_id, command)

                if command.upper() == 'OPEN':
                    self.garageDoors.get(door_id).do_open_door()
                elif command.upper() == 'CLOSE':
                    self.garageDoors.get(door_id).do_close_door()
                elif command.upper() == 'TRIGGER':
                    self.garageDoors.get(door_id).do_trigger_door()

            elif jsonPayload['topic'] == self.doorStatusTopic:
                #
                # OK - this is a standard HHB/STATUS command - look for the message about Garage Doors
                device_type = jsonPayload['deviceType']
                if device_type == 24:
                    print 'Door 24 Status Received !', payload
                    door_state = jsonPayload['state'].upper()
                    date_time = jsonPayload['datetime']

                    # Fix this as soon as I get more than one Garage Door
                    door_id = 1
                    if door_state == 'CLOSED':
                        self.garageDoors.get(door_id).set_closed(date_time)
                    else:
                        self.garageDoors.get(door_id).set_opened(date_time)
        except:
            logging.error('Error trying to convert message to json You havent fixed the json payload in HHB yet, have you?')

    # ------------------------------------------------------------------------------------
    def start(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker_address)
        self.client.subscribe(self.commandTopic,0)
        self.client.subscribe(self.doorStatusTopic,0)
        self.client.loop_start()

    # ------------------------------------------------------------------------------------
    def cleanup(self):
        self.client.unsubscribe(self.commandTopic)
        self.client.unsubscribe(self.doorStatusTopic)
        self.client.disconnect()
        self.client.loop_stop()

    # ------------------------------------------------------------------------------------
    def sendStatusMessage(self):
        ##logging.info('Sending a status message')
        data = OrderedDict()
        data['topic'] = 'GDCTL/STATUS'
        data['datetime'] = datetime.datetime.now().replace(microsecond=0).isoformat()
        data['system'] = SystemStats().asJSON()
        # data['door'] = self.garageDoors.get(1).asJSON()
        doorData = self.garageDoors.get(1).asJSON()
        data['door'] = doorData
        try:
            json_data = json.dumps(data)
        except Exception as ex:
            logging.error( 'Error ', ex )
        self.client.publish(self.statusTopic, json_data,qos=0)
