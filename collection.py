import App

def collect_notraffic(ip_src, ip_dest):
    sdw2_connect = App.create_SSH(2)
    #set ACL1
    App.set_ACL(sdw2_connect, 101, ip_src, "0.0.0.255", ip_dest, "0.0.0.255", [])
    # tracert
    App.get_int("sdwan2_1", "Gi1/0/1", sdw2_connect)
    App.get_int("sdwan2_2", "Gi1/0/2", sdw2_connect)
    App.get_latency("sdwan2_1", ip_src, ip_dest, sdw2_connect)
    #set ACL2
    
    App.delete_SSH(sdw2_connect)

def collect_():
    sdw1_connect, sdw2_connect = App.create_SSH()
    

    App.delete_SSH(sdw1_connect, sdw2_connect)
