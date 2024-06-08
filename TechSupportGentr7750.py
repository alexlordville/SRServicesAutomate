import csv
import sys
from netmiko import ConnectHandler
from getpass import getpass
import time
from datetime import date

#Variables for connecting to the router
passwrd = getpass("Type your password:")
tsfnumber = input('Tech Support ID (ex. ts1 ts2): ')

with open("7750list.csv", newline='') as nodesfile:
    nodesReader = csv.DictReader(nodesfile)
    for row in nodesReader:
        routerIp = row["ip"]
        device = ConnectHandler(
            device_type="alcatel_sros",
            host=routerIp,
            username="P3194337",
            password=passwrd,
        )
        
        output = device.send_command(
            "/show system information | match Name\n",
            read_timeout=90
        )
       
        nodeName = output.split()
        today = date.today()
        tsfGen = device.send_command(
            f"/admin tech-support cf3:{nodeName[-1]}.{tsfnumber}",
            expect_string=r"\#",
            read_timeout=90
        )
        print(tsfGen)
        print(f"Tech Support File generated: {nodeName[-1]}-{routerIp} "+ today.strftime("%A %d. %B %Y"))

         