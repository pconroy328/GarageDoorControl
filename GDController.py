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


logging.basicConfig(filename='garagedoorcontroller.log', level=logging.DEBUG)
#
# logging.getLogger().setLevel(logging.DEBUG)
#

logging.info("GarageDoorController - v8 - Application start!")

aws_mqtt_broker = 'ec2-52-32-56-28.us-west-2.compute.amazonaws.com'
msgHandler = MessageHandler(aws_mqtt_broker)
msgHandler.start()

loopCounter = 0
while True:
    #if (loopCounter % 10 == 0):
    #    logging.info('v7 Main loop sleeping - processing messages')
    msgHandler.sendStatusMessage()
    sleep(30)
    loopCounter += 1
