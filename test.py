import App

def set_ACL_test():
    sdw1_connect, sdw2_connect = App.create_SSH(2)
    
    App.set_ACL(sdw1_connect, 102, App.links[0][0], "0.0.0.255", App.links[0][1], "0.0.0.255")
    App.unset_ACL(sdw1_connect, 102)
    cmd = "traceroute " + App.links[0][1]
    cisco_output = list((sdw1_connect.send_command(cmd, read_timeout=75)).split('\n'))
    print(cisco_output)

    App.set_ACL(sdw1_connect, 102, App.links[0][0], "0.0.0.255", App.links[1][1], "0.0.0.255")
    App.unset_ACL(sdw1_connect, 102)
    cmd = "traceroute " + App.links[0][1]
    cisco_output = list((sdw1_connect.send_command(cmd, read_timeout=75)).split('\n'))
    print(cisco_output)

    App.delete_SSH(sdw1_connect)
    App.delete_SSH(sdw2_connect)

set_ACL_test()

#SDWAN1 -> PBR sur le Gi1/0/24
#SDWAN1 -> ACL 
#SDWAN2 -> PBR sur le Gi1/0/24
#SDWAN1 -> ACL 


    # for i in range(len(int_lst)):
    #     print(get_int("sdwan1", int_lst[i], sdw1_connect))
    # for i in range(len(int_lst)):
    #     print(get_int("sdwan2", int_lst[i], sdw2_connect))

    # for i in range(len(links)):
    #     print(get_latency("sdwan1", links[i][0], links[i][1], sdw1_connect))

    # set_ACL(links[0][0], "0.0.0.255", links[0][1], "0.0.0.255", 102, sdw1_connect)
    # set_ACL(links[0][0], "0.0.0.255", links[0][1], "0.0.0.255", 102, sdw1_connect)
    # set_ACL(links[1][0], "0.0.0.255", links[1][1], "0.0.0.255", 103, sdw1_connect)

    # set_PBR(sdw1_connect, int_lst[0], "testpbr1", 102, links[0][0])
    # set_PBR(sdw1_connect, int_lst[0], "testpbr2", 102, links[0][0])
    # set_PBR(sdw1_connect, int_lst[0], "testpbr", 103, links[1][0])

    # unset_PBR(sdw1_connect, int_lst[0], "testpbr", 102, links[0][0])
    # unset_PBR(sdw1_connect, int_lst[0], "testpbr", 103, links[1][0])

    # unset_ACL(sdw1_connect, 102)
    # unset_ACL(sdw1_connect, 103)
