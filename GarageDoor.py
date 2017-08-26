from Relay import Relay
import datetime
import logging

class GarageDoor(object):

    def __init__(self, door_id):
        self.door_id = door_id
        self.state = 'UNKNOWN'
        self.state_datetime = datetime.datetime.now()
        self.door_relay = Relay()
        self.last_command = 'UNKNOWN'
        self.last_command_datetime = datetime.datetime.now()

    def set_opened(self, date_time):
         #logging.debug('Setting garage door state to OPENED at %s', date_time)
         self.state_datetime = date_time
         self.state = 'OPENED'

    def set_closed(self, date_time):
         #logging.debug('Setting garage door state to CLOSED at %s', date_time)
         self.state_datetime = date_time
         self.state = 'CLOSED'

    def is_opened(self):
        return self.state == 'OPENED'

    def is_closed(self):
        return self.state == 'CLOSED'

    def do_open_door(self):
        logging.info('Command received to open the door')
        if self.state == 'OPENED':
            logging.info('Open command ignored - door is already open')
            return
        logging.info('Setting state to in-motion - triggering relay')
        self.last_command = 'OPEN'
        self.last_command_datetime = datetime.datetime.now()
        self.state = 'INMOTION'
        self.door_relay.trigger(self.door_id)

    def do_close_door(self):
        logging.info('Command received to close the door')
        if self.state == 'CLOSED':
            logging.info('Close command ignored - door is already open')
            return
        logging.info('Setting state to in-motion - triggering relay')
        self.last_command = 'CLOSE'
        self.last_command_datetime = datetime.datetime.now()
        self.state = 'INMOTION'
        self.door_relay.trigger(self.door_id)

    def do_trigger_door(self):
        logging.info('Trigger command received')
        self.last_command = 'TRIGGER'
        self.last_command_datetime = datetime.datetime.now()
        self.state = 'INMOTION'
        self.door_relay.trigger(self.door_id)

    def asJSON(self):
        mydict = dict(door_id=self.door_id, state=self.state, state_datetime=self.state_datetime,
                      last_command=self.last_command, last_command_datetime=self.last_command_datetime)
        return mydict