#!/usr/bin/env python 

import os
import sys
import time
from termcolor import colored
import subprocess
import shlex
import psycopg2

targetPort = "/dev/ttyACM0"
operator = ""
serialNumber = ""
iserail = ""

print "Board Logger"
directory = os.path.split(os.path.realpath(__file__))[0]

if len(sys.argv) < 2:
    print "operator required: boardlogger <operator>"
    sys.exit(0)

operator = sys.argv[1]

print "Connecting to database..."
# Open our file outside of git repo which has database location, password, etc
dbfile = open(directory+'/postgres_info.txt', 'r')
postgresInfo = dbfile.read()
dbfile.close()
try:
    testStorage = psycopg2.connect(postgresInfo)
except:
    print "Could not connect!"
    sys.exit(0)


def beep():
    subprocess.call(["beep","-f 2250"])

def getInternalSerialNumber():
        global iserial
        #/sbin/udevadm info --query=property --name=/dev/ttyACM1 | awk -F'=' '/SHORT/ {print $2}
        #for line in subprocess.check_output(shlex.split("/sbin/udevadm info --query=property --name=/dev/ttyACM1")).splitlines():
        iserialproc = subprocess.Popen(shlex.split("/sbin/udevadm info --query=property --name=" + targetPort),stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for line in iserialproc.communicate()[0].splitlines():
            if line.split('=')[0] == "ID_SERIAL_SHORT": iserial = line.split('=')[1]
        if iserial == "":
            beep()
            print colored("USB Serial port does not exist or is not connected.","yellow")
            return 0
        return iserial

while True:
    note = ""
    serialNumber = ""
    iserial = ""

    print "Logged in as: " + colored(operator,'blue')
    print "Enter serial number : "
    serialNumber = raw_input().strip()

    subprocess.call(["/usr/bin/sudo",directory+"/dfu32.sh",directory+"/32u2fw.hex"])
    time.sleep(1)

    if not getInternalSerialNumber() and serialNumber == "": continue
 
    print "iserial: " + str(iserial)

    print "Enter note : "
    note = raw_input().strip()
    if not len(note): continue

    testStorage = psycopg2.connect(postgresInfo)
    cursor = testStorage.cursor()
    cursor.execute("""INSERT INTO rework(serial, timestamp, iserial, note, operator) VALUES (%s, %s, %s, %s, %s)""", (serialNumber, 'now', iserial, note, operator) )
    testStorage.commit()

