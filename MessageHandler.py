import paho.mqtt.client as mqtt
import json
import datetime
import time
from GarageDoor import GarageDoor
from SystemStats import SystemStats
import logging
from collections import OrderedDict
import os

##
## adding voice 21Feb2022
##


class MessageHandler(object):

    # ------------------------------------------------------------------------------------
    def __init__(self,broker_address='gx100.local'):
        self.broker_address = broker_address
        self.client = mqtt.Client(client_id="", clean_session=True, userdata=None)
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
        #logging.info( 'Payload came in: %s',  payload )
        try:
            jsonPayload = json.loads(payload)
            #
            # is this a HHB Door Status message?
            ###logging.info( 'Topic came in: %s',  jsonPayload['topic'] )

            #
            # is this a command to open or close the door?
            if jsonPayload['topic'] == self.commandTopic:
                logging.debug('Command received! [%s]', payload)

                date_time = jsonPayload["dateTime"]
                door_id = jsonPayload["doorID"]
                command = jsonPayload["command"]
                logging.info('Command received on %s, for door %s, command %s', date_time, door_id, command)

                if command.upper() == 'OPEN':
                    self.garageDoors.get(door_id).do_open_door()

                elif command.upper() == 'CLOSE':
                    # Stop receiving messages for a bit
                    logging.info('Close command arrived - unsubcribing from the topic')
                    self.client.subscribe(self.commandTopic)

                    logging.info('Playing warning message')
                    os.system('aplay -Dplughw /home/pconroy/GarageDoorControl/doorclosing.wav')

                    logging.info('Sending close command to door')
                    self.garageDoors.get(door_id).do_close_door()

                    logging.info('Sleeping 5 seconds then resubcribing')
                    time.sleep(5)
                    self.client.subscribe(self.commandTopic,0)

                elif command.upper() == 'TRIGGER':
                    self.garageDoors.get(door_id).do_trigger_door()

            elif jsonPayload['topic'] == self.doorStatusTopic:
                #
                # OK - this is a standard HHB/STATUS command - look for the message about Garage Doors
                device_type = jsonPayload['deviceType']
                if device_type == 24:
                    door_state = jsonPayload['state'].upper()
                    date_time = jsonPayload['dateTime']
                    logging.info('Door 24 Status Received! State %s', door_state)

                    # Fix this as soon as I get more than one Garage Door
                    door_id = 1
                    if door_state == 'CLOSED':
                        self.garageDoors.get(door_id).set_closed(date_time)
                    else:
                        self.garageDoors.get(door_id).set_opened(date_time)
        except Exception as ex:
            logging.error('Error trying to convert message to json You havent fixed the json payload in HHB yet, have you?')
            logging.error(ex)

    # ------------------------------------------------------------------------------------
    def start(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker_address)
        self.client.subscribe(self.commandTopic,0)
        self.client.subscribe(self.doorStatusTopic,0)
        self.client.loop_start()
        logging.info('Mosquitto loop started.')

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
        data['dateTime'] = datetime.datetime.now().replace(microsecond=0).isoformat()
        #data['system'] = SystemStats().asJSON()
        # data['door'] = self.garageDoors.get(1).asJSON()
        doorData = self.garageDoors.get(1).asJSON()
        data['door'] = doorData
        try:
            json_data = json.dumps(data)
        except Exception as ex:
            logging.error( 'Error ', ex )
        self.client.publish(self.statusTopic, json_data,qos=0)
