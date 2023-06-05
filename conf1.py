from netmiko import ConnectHandler
# from genie import *

# https://www.thegeekstuff.com/2013/08/enable-ssh-cisco/

def parser(cisco_output):
    return 0

sdwan1 = {
    'device_type': 'cisco_ios',
    'host':   '192.168.8.254',
    'username': 'cisco',
    'password': 'ping123',
    # 'port' : 22,          # optional, defaults to 22
    'secret': 'ping123',     # optional, defaults to ''
    "session_log": 'logs/netmiko_session1.log',
}

sdwan2 = {
    'device_type': 'cisco_ios',
    'host':   '192.168.8.218',
    'username': 'cisco',
    'password': 'ping123',
    # 'port' : 22,          # optional, defaults to 22
    'secret': 'ping123',     # optional, defaults to ''
    "session_log": 'logs/netmiko_session2.log',
}

sdw1_connect = ConnectHandler(**sdwan1)
sdw1_connect.enable()
sdw2_connect = ConnectHandler(**sdwan2)
sdw2_connect.enable()

cmd = ["sh int Gi1/0/1 | inc drops|bits", "sh int Gi1/0/2 | inc drops|bits"]
for x in cmd:
    output = sdw1_connect.send_command(x)
    print(output)
for x in cmd:
    output = sdw2_connect.send_command(x)
    print(output)

# bande passante : "BW 1000000 Kbit/sec"
# Délais : "DLY 10 usec"
# Bande passante dispo et total (réel vs. théorique)
# IP : "Internet address is 192.168.8.197/24"
# 1000Mb/s
# input flow-control is on, output flow-control is unsupported
# I/O 117000 bits/sec /  0 bits/sec
# , débit (packet entré sortie
# délais, latence