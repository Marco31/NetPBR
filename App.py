from netmiko import ConnectHandler
from parse import *

def get_int(cisco_name, cisco_interface, sdw_connect):
    cmd = "sh int " + cisco_interface + " | inc drops|bits"
    cisco_output = list((sdw_connect.send_command(cmd)).split('\n'))
    for j in range(len(cisco_output)):
        cisco_output[j] = cisco_output[j].strip()

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

# Lien haut : SDWAN1 (10.1.1.1) <-> ... <-> SDWAN2 (10.2.3.2) : ping ip 10.2.3.2 source 10.1.1.1
# Lien bas : SDWAN1 (10.2.1.1) <-> ... <-> SDWAN2 (10.3.3.2) : ping ip 10.3.3.2 source 10.2.1.1
def get_latency(cisco_name, cisco_addr_src, cisco_addr_dest, sdw_connect):
    cmd = "ping ip " + cisco_addr_dest + " source " + cisco_addr_src
    cisco_output = list((sdw_connect.send_command(cmd)).split('\n'))
    for j in range(len(cisco_output)):
        cisco_output[j] = cisco_output[j].strip()

    cisco_ping = {
    "cisco_name" : "SDWAN99",
    "cisco_addr_src" : "10.0.0.0",
    "cisco_addr_dest" : "10.0.0.0",
    "nb_packet_sent" : -1,
    "size_ICMP_packet" : -1,
    }
    template = ["Type escape sequence to abort.",
    "Sending {}, {}-byte ICMP Echos to {}, timeout is {} seconds:",
    "Packet sent with a source address of {}",
    "!!!!!",
    "Success rate is {} percent ({}/{}), round-trip min/avg/max = {}/{}/{} ms"
    ]
    parsed = []
    data = []
    for i in range(len(template)):
        # print(cisco_output[i])
        # print(template[i])
        parsed.append(parse(template[i], cisco_output[i]))
    # print(list(parsed[0].fixed))
    # print(parsed[0])
    for i in range(len(parsed)):
        if (parsed[i] == None):
            continue
        data0 = list(parsed[i].fixed)
        for j in range(len(data0)):
            data.append(data0[j])
    
    # print(data)
    cisco_ping["cisco_name"] = cisco_name
    cisco_ping["cisco_addr_src"] = cisco_addr_src # =data[2]
    cisco_ping["cisco_addr_dest"] = cisco_addr_dest # =data[4]
    cisco_ping["nb_packet_sent"] = data[0] # = data[7]
    cisco_ping["size_ICMP_packet"] = data[1]
    cisco_ping["timeout"] = data[3]
    cisco_ping["Success_rate_percent"] = data[5]
    cisco_ping["Success_packet"] = data[6]
    cisco_ping["round_trip_min"] = data[8]
    cisco_ping["round_trip_avg"]  = data[9]
    cisco_ping["round_trip_max"] = data[10]
    return cisco_ping

def set_ACL():
    #TODO
    return 0

def set_PBR(sdw_connect, cisco_interface):
    # Device# configure terminal
    # Device(config)# interface gigabitethernet 1/0/0
    # Device(config-if)# no switchport
    # Device(config-if)# ip policy route-map equal-access       Identifies a route map to use for policy routing on an interface.
    # Device(config-if)# exit       
    # Device(config)# route-map equal-access permit 10          Defines the conditions for redistributing routes from one routing protocol into another routing protocol or enables policy-based routing and enters route-map configuration mode.
    # Device(config-route-map)# match ip address 1              Define the criteria by which packets are examined to learn if they will be policy-based routed.
    # Device(config-route-map)# set ip next-hop 172.16.6.6      Specifies where to output packets that pass a match clause of a route map for policy routing.
    # Device(config-route-map)# end
    cmd = ["int " + cisco_interface, "no switchport", "ip policy route-map" + name_pbr, "exit",
            "route-map " + name_pbr + " permit 10", "match ip address" + nb_ACL, "set ip next-hop" + addr_route]
    for i in range(len(cmd))
        cisco_output = list((sdw_connect.send_command(cmd[i])).split('\n'))

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

# create SSH connexion
sdw1_connect = ConnectHandler(**sdwan1)
sdw1_connect.enable()
sdw2_connect = ConnectHandler(**sdwan2)
sdw2_connect.enable()

machine = ["sdwan1", "sdwan2"]
int_lst = ["Gi1/0/1", "Gi1/0/2"]
links = [["10.1.1.1", "10.2.3.2"], ["10.2.1.1", "10.3.3.2"]] #[src, dst], ...]

for i in range(len(int_lst)):
    print(get_int("sdwan1", int_lst[i], sdw1_connect))
for i in range(len(int_lst)):
    print(get_int("sdwan2", int_lst[i], sdw2_connect))

for i in range(len(links)):
    print(get_latency("sdwan1", links[i][0], links[i][1], sdw1_connect))
