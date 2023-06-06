from netmiko import ConnectHandler
from parse import *

# https://www.thegeekstuff.com/2013/08/enable-ssh-cisco/


def parser_int(cisco_name, cisco_interface, cisco_output):
    cisco_int = {
    "cisco_name" : "SDWAN99",
    "cisco_interface" : "fa0/0",
    "size_I_queue" : -1,
    "max_I_queue" : -1,
    "drops_I_queue" : -1,
    "flushes_I_queue" : -1,
    "O_drop" : -1,
    "I_rate_bit" : -1,
    "I_rate_packet" : -1,
    "O_rate_bit" : -1,
    "O_rate_packet" : -1,
    "Unknown_protocol" : -1
    }
    template = ["Input queue: {}/{}/{}/{} (size/max/drops/flushes); Total output drops: {}",
  "5 minute input rate {} bits/sec, {} packets/sec",
  "5 minute output rate {} bits/sec, {} packets/sec",
     "{} unknown protocol drops"]
    parsed = []
    data = []
    for i in range(len(template)):
        # print(cisco_output[i])
        parsed.append(parse(template[i], cisco_output[i]))
    # print(list(parsed[0].fixed))
    if (parsed[0] != None):
        for i in range(len(parsed)):
            data0 = list(parsed[i].fixed)
            for j in range(len(data0)):
                data.append(data0[j])
    else :
        print("error with " + cisco_name + " " + cisco_interface)
        print(cisco_output)
        return -1
    
    # print(data)
    cisco_int["cisco_name"] = cisco_name
    cisco_int["cisco_interface"] = cisco_interface
    cisco_int["size_I_queue"] = data[0]
    cisco_int["max_I_queue"] = data[1]
    cisco_int["drops_I_queue"] = data[2]
    cisco_int["flushes_I_queue"] = data[3]
    cisco_int["O_drop"] = data[4]
    cisco_int["I_rate_bit"] = data[5]
    cisco_int["I_rate_packet"] = data[6]
    cisco_int["O_rate_bit"] = data[7]
    cisco_int["O_rate_packet"]  = data[8]
    cisco_int["Unknown_protocol"] = data[9]
    return cisco_int

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

# cmd = ["sh int Gi1/0/1 | inc drops|bits"]
cmd = ["sh int Gi1/0/1 | inc drops|bits", "sh int Gi1/0/2 | inc drops|bits"]
for i in range(len(cmd)):
    output = list((sdw1_connect.send_command(cmd[i])).split('\n'))
    for j in range(len(output)):
        output[j] = output[j].strip()
    print(parser_int("sdwan1", "Gi1/0/" + str(i+1), output))

for i in range(len(cmd)):
    output = list((sdw2_connect.send_command(cmd[i])).split('\n'))
    for j in range(len(output)):
        output[j] = output[j].strip()
    print(parser_int("sdwan2", "Gi1/0/" + str(i+1) ,output))

# print(parse("Input queue: {}/{}/{}/{} (size/max/drops/flushes); Total output drops: {}", "Input queue: 0/375/0/0 (size/max/drops/flushes); Total output drops: 0"))
# bande passante : "BW 1000000 Kbit/sec"
# Délais : "DLY 10 usec"
# Bande passante dispo et total (réel vs. théorique)
# IP : "Internet address is 192.168.8.197/24"
# 1000Mb/s
# input flow-control is on, output flow-control is unsupported
# I/O 117000 bits/sec /  0 bits/sec
# , débit (packet entré sortie
# délais, latence