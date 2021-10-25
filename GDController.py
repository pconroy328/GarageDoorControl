#import Relay
from MessageHandler import MessageHandler
from time import sleep
import logging

#
# To get this into CodeCommit
#   Log into AWS Console, Code Commit
#   Create Code Commit repo
#
# from home dir
#   git init
#   git config --global user.name "Patrick Conroy"
#   git config --global user.email "patrick@conroy-family.net"
#   git add .
#   git commit
#   git remote add origin <url from AWS Code Commit Repo>
#
# Use latest version of Paho MQTT
#   sudo pip install paho-mqtt --upgrade
#
# If AWS complains about handshake failure:
# on 'pats'
#   cd git-openssl/
#   sudo dpkg -i git_1.9.1-1ubuntu0.3_amd64.deb
#   echo "git hold" | sudo dpkg --set-selections

#
# Repo is https://git-codecommit.us-east-1.amazonaws.com/v1/repos/GarageDoorControl
#
FORMAT = '%(asctime)-15s|%(levelname)s|%(message)s'
logging.basicConfig(format=FORMAT,filename='/tmp/garagedoorcontroller.log', level=logging.WARNING)
#
logging.getLogger().setLevel(logging.DEBUG)
#

logging.info("GarageDoorController - v9.1 - Application start!")

mqtt_broker = 'gx100.local'
msgHandler = MessageHandler(mqtt_broker)
msgHandler.start()

loopCounter = 0
while True:
    if (loopCounter % 10 == 0):
        logging.info('v9.1 Main loop sleeping - processing messages')
    msgHandler.sendStatusMessage()
    sleep(30)
    loopCounter += 1
