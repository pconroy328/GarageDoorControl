#import Relay
from MessageHandler import MessageHandler
from time import sleep
import logging

#
# Use latest version of Paho MQTT
#   sudo pip install paho-mqtt --upgrade
#
#
FORMAT = '%(asctime)-15s|%(levelname)s|%(message)s'
logging.basicConfig(format=FORMAT,filename='/tmp/garagedoorcontroller.log', level=logging.WARNING)
#
logging.getLogger().setLevel(logging.INFO)
#

logging.info("GarageDoorController - v9.2 - Application start!")

mqtt_broker = 'gx100.local'
msgHandler = MessageHandler(mqtt_broker)
msgHandler.start()

loopCounter = 0
while True:
    if (loopCounter % 10 == 0):
        logging.info('Main loop sleeping - processing messages')
    msgHandler.sendStatusMessage()
    sleep(30)
    loopCounter += 1
