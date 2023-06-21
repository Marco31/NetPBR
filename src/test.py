"""Module test, as it's name suggest, test NetPBR library"""

__author__ = 'Marc VEYSSEYRE'

import NetPBR as npr

def set_ACL_test():
    """Function to test if ACL can be set and unset."""
    sdw1_connect = npr.create_ssh(1)
    sdw2_connect = npr.create_ssh(2)

    npr.set_ACL(sdw1_connect, 102, npr.links[0][0], "0.0.0.255", [80])
    npr.unset_ACL(sdw1_connect, 102)
    cmd = "traceroute " + npr.links[0][1]
    cisco_output = list((sdw1_connect.send_command(cmd, read_timeout=75)).split('\n'))
    print(cisco_output)

    npr.set_ACL(sdw1_connect, 102, npr.links[0][0], "0.0.0.255", [80])
    npr.unset_ACL(sdw1_connect, 102)
    cmd = "traceroute " + npr.links[0][1]
    cisco_output = list((sdw1_connect.send_command(cmd, read_timeout=75)).split('\n'))
    print(cisco_output)

    npr.remove_ssh(sdw1_connect)
    npr.remove_ssh(sdw2_connect)

if __name__ == "__main__":
    set_ACL_test()
