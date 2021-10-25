import os
from datetime import timedelta
from subprocess import check_output
import json

class SystemStats(object):
    def __init__(self):
        pass

    def get_cpu_temperature(self):
        try:
            res = os.popen('vcgencmd measure_temp').readline()
            tempC = float((res.replace("temp=", "").replace("'C\n", "")))
        except:
            tempC = 0
        return (tempC * 1.8) + 32.0

    def get_camera_present(self):
        try:
            res = os.popen('vcgencmd get_camera').readline()
        except:
            res = ''
        return 'supported=1 detected=1' in res

    def get_uptime(self):
        try:
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
                uptime_string = str(timedelta(seconds=uptime_seconds))
        except:
            uptime_string = '??'
        return uptime_string

    def get_SSID(self, interface='wlan0'):
        ssid = "None"
        try:
            scanoutput = check_output(['iwconfig', interface])
            for line in scanoutput.split():
                line = line.decode('utf-8')
                if line[:5] == 'ESSID':
                    ssid = line.split('"')[1]
        except:
            pass
        return ssid

    def asJSON(self):
        mydict = { "cpu_temp": self.get_cpu_temperature(),
                   "camera_present": self.get_camera_present(),
                   "uptime": self.get_uptime(),
                   "ssid": self.get_SSID()}
        return mydict
