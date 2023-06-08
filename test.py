import App

def set_ACL_test():
    sdw1_connect, sdw2_connect = App.create_SSH()
    
    App.set_ACL(App.links[0][0], "0.0.0.255", App.links[0][1], "0.0.0.255", 102, sdw1_connect)
    App.unset_ACL(sdw1_connect, 102)
    cmd = "traceroute " + App.links[0][1]
    cisco_output = list((sdw1_connect.send_command(cmd, read_timeout=75)).split('\n'))
    print(cisco_output)

    App.set_ACL(App.links[0][0], "0.0.0.255", App.links[1][1], "0.0.0.255", 102, sdw1_connect)
    App.unset_ACL(sdw1_connect, 102)
    cmd = "traceroute " + App.links[0][1]
    cisco_output = list((sdw1_connect.send_command(cmd, read_timeout=75)).split('\n'))
    print(cisco_output)

    App.delete_SSH(sdw1_connect, sdw2_connect)

set_ACL_test()