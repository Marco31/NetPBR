from netmiko import ConnectHandler
from parse import *
from tcp_latency import measure_latency
import subprocess

DEBUG = True

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
    """
    Return parse of ping request
    """
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
    "timeout" : -1,
    "Success_rate_percent" : -1,
    "Success_packet" : -1,
    "round_trip_min" : -1,
    "round_trip_avg" : -1,
    "round_trip_max" : -1
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

    ACL = "access-list 102 permit ip " + cisco_addr_src + " " + cisco_mask_src +" " + cisco_addr_dest + " " + cisco_mask_dest

def get_latency_2(cisco_addr_dest):
    """
    Return of tcplatency request
    """
    A = measure_latency(host=cisco_addr_dest, runs=1, timeout=2)
    return A

def get_latency_3(cisco_addr_dest):
    """
    Return parse of abing request (https://github.com/RichardWithnell/abing)
    This function is not 
    """
    abing = {
    "ID" : "SDWAN99",
    "addr_dest" : "10.0.0.0",
    "ABw" : -1,
    "Xtr" : -1,
    "DBC" : -1,
    "RTT-min" : -1,
    "RTT-avg" : -1,
    "RTT-max" : -1,
    "RTT-timeout" : -1,
    }
    B = ""
    if not DEBUG:
        A = subprocess.run(['abing', '-d', 'cisco_addr_dest'], stdout=subprocess.PIPE)
        B = A.stdout
    else:
        B = """1686830131 T: 192.168.50.9 ABw-Xtr-DBC:  10.7   0.4  11.1 ABW:  10.7 Mbps RTT: 7.322 7.550 7.913 ms 20 20
    1686830131 F: 192.168.50.9 ABw-Xtr-DBC:   9.7   0.1   9.8 ABW:   9.7 Mbps RTT: 7.322 7.550 7.913 ms 20 20"""
    B = list(B.split('\n'))
    for j in range(len(B)):
            B[j] = B[j].strip()

    template = ["{} T: {} ABw-Xtr-DBC:  {}   {}  {} ABW:  {} Mbps RTT: {} {} {} ms {} {}",
                "{} F: {} ABw-Xtr-DBC:   {}   {}  {} ABW:   {} Mbps RTT: {} {} {} ms {} {}"]
    parsed = []
    data = []
    for i in range(len(template)):
        # print(cisco_output[i])
        # print(template[i])
        parsed.append(parse(template[i], B[i]))
    # print(list(parsed[0].fixed))
    # print(parsed[0])
    for i in range(len(parsed)):
        if (parsed[i] == None):
            continue
        data0 = list(parsed[i].fixed)
        for j in range(len(data0)):
            data.append(data0[j])

    abing["ID"] = data[0]
    abing["addr_dest"] = data[1]
    abing["ABw"] = data[2]
    abing["Xtr"] = data[3]
    abing["DBC"] = data[4]
    abing["RTT-min"] = data[6]
    abing["RTT-avg"] = data[7]
    abing["RTT-max"] = data[8]
    abing["RTT-timeout"] = data[9]

    return abing


def set_ACL(sdw_connect, nb_ACL, cisco_addr_src = "-1", cisco_mask_src = "-1", port=[]):
    """
    this function set ACL on cisco router
    """
    ACL1_0 = "no access-list " + str(nb_ACL)
    if (port == ["NACL"]):
        cisco_output = list((sdw_connect.send_config_set(ACL1_0)).split('\n'))
        set_PBR_2(sdw_connect, "test", -1)
        config_commands = [ACL1_1, ACL1_2, ACL1_3, ACL2_1, ACL1_2]
        ACL1_1 = "int Gi1/0/1"
        ACL1_2 = "no ip policy route-map test"
        ACL1_3 = "exit"
        ACL2_1 = "int Gi1/0/12"
        ACL1_2 = "no ip policy route-map test"

        for i in range(len(config_commands)):
            cisco_output = list((sdw_connect.send_config_set(config_commands[i])).split('\n'))
        return
    ACL1_1 = ""
    if (cisco_addr_src == "-1" or cisco_mask_src == "-1" or port == []):
        return
    else:
        config_commands = [ACL1_0]
        for pt in port:
            config_commands.append("access-list " + str(nb_ACL) + " permit ip " + cisco_addr_src + " " + cisco_mask_src +" any" + " eq " + pt)
        ACL1_2 = "access-list " + str(nb_ACL) + " deny ip any any "
        config_commands.append(ACL1_2)
        for i in range(len(config_commands)):
            cisco_output = list((sdw_connect.send_config_set(config_commands[i])).split('\n'))
        set_PBR_2(sdw_connect, "test", 101)
        config_commands = ["int Gi1/0/1", "ip policy route-map test", "exit", "int Gi1/0/12", "no ip policy route-map test"]
        for i in range(len(config_commands)):
            cisco_output = list((sdw_connect.send_config_set(config_commands[i])).split('\n'))
        return

def unset_ACL(sdw_connect, nb_ACL):
    """
    this function unset ACL on cisco router
    """
    ACL1_0 = "no access-list " + str(nb_ACL)
    send_config_set = [ACL1_0]
    for i in range(len(send_config_set)):
        cisco_output = list((sdw_connect.send_config_set(send_config_set[i])).split('\n'))
    return


def set_PBR(sdw_connect, cisco_interface, name_pbr, nb_ACL, addr_route):
    """
    This function set PBR configuration on an interface
    """
    config_commands = ["int " + cisco_interface, "no switchport", "ip policy route-map " + name_pbr, "exit",
            "route-map " + name_pbr + " permit 10", "match ip address " + str(nb_ACL), "set ip next-hop " + addr_route]
    cisco_output = list((sdw_connect.send_config_set(config_commands)).split('\n'))
    return

def set_PBR_2(sdw_connect, name_pbr, nb_ACL):
    """
    This function set PBR configuration on an interface
    """
    config_commands = []
    if nb_ACL == -1:
            config_commands = ["route-map " + name_pbr + " permit 10", "no match ip address"]
    else:
        config_commands = ["route-map " + name_pbr + " permit 10", "no match ip address", "match ip address " + str(nb_ACL)]
    cisco_output = list((sdw_connect.send_config_set(config_commands)).split('\n'))
    return

def unset_PBR(sdw_connect : ConnectHandler, cisco_interface, name_pbr, nb_ACL, addr_route):
    """
    This function remove previous PBR configuration on an interface
    """
    config_commands = ["int " + cisco_interface, "switchport", "no route-map " + name_pbr, "exit",
            "route-map " + name_pbr + " permit 10", "match ip address " + str(nb_ACL), "set ip next-hop " + addr_route]
    cisco_output = list((sdw_connect.send_config_set(config_commands)).split('\n'))
    return

# Following IP need to be change

# ssh cisco@192.168.8.254
sdwan1 = {
    'device_type': 'cisco_ios',
    'host':   '192.168.8.254', #  192.168.4.1 192.168.8.254 
    'username': 'cisco',
    'password': 'ping123',
    # 'port' : 22,          # optional, defaults to 22
    'secret': 'ping123',     # optional, defaults to ''
    "session_log": 'src/logs/netmiko_session1.log',
}

# ssh cisco@192.168.8.218
sdwan2 = {
    'device_type': 'cisco_ios',
    'host':   '192.168.8.218',
    'username': 'cisco',
    'password': 'ping123',
    # 'port' : 22,          # optional, defaults to 22
    'secret': 'ping123',     # optional, defaults to ''
    "session_log": 'src/logs/netmiko_session2.log',
}

machine = ["sdwan1", "sdwan2"]
int_lst = ["Gi1/0/1", "Gi1/0/2"]
links = [["10.1.1.1", "10.2.3.2"], ["10.2.1.1", "10.3.3.2"], ["192.168.4.1", "192.168.8.218"]] #[src, dst], ...]
protocols = [
    ["Echo", [7]],
    ["FTP", [21,20]],
    ["SSH", [22]],
    ["Telnet", [23]],
    ["SMTP", [25]],
    ["TFTP", [69]],
    ["HTTP", [80, ]],
    ["POP", [109, 110]],
    ["SQL", [118]],
    ["IMAP", [143]],
    ["LDAP", [389]],
    ["HTTPS", [443]],
    ["TLS-SSL", [465]],
    ["DHCPS", [546, 547]],
    ["IMAPS", [585]],
    ["SMTP", [587]],
    ["LDAPS", [636]],
    ["Cisco", [5004]] # UDP
]

def create_SSH(s : int):
    """
    Return ConnectHandler object to control cisco device
    """
    if (s == 1):
        sdw1_connect = ConnectHandler(**sdwan1)
        sdw1_connect.enable()
        return sdw1_connect
    elif (s == 2):
        sdw2_connect = ConnectHandler(**sdwan2)
        sdw2_connect.enable()
        return sdw2_connect
    else:
        return 0

def remove_SSH(sdw_connect):
    """
    remove SSH connexion
    """
    sdw_connect.disconnect()

if __name__ == "__main__":
    # sdw1_connect, sdw2_connect = create_SSH(2)
    # set_PBR(sdw1_connect, "Gi1/0/24", "pbrsdw1", "192.168.4.1")
    # set_PBR(sdw2_connect, "Gi1/0/24", "pbrsdw2", "192.168.8.218")

    # set_ACL(links[0][0], "0.0.0.255", links[0][1], "0.0.0.255", 102, sdw1_connect)
    # set_ACL(links[0][0], "0.0.0.255", links[0][1], "0.0.0.255", 102, sdw1_connect)
    # remove_SSH(sdw1_connect)
    # remove_SSH(sdw2_connect)
    # C = get_latency_2("192.168.50.1")
    C = get_latency_3("192.168.50.9")
    print(C)
