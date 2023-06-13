import NetPBR as npr
import time
import random


def collect_notraffic(sdw1_connect, ip_src, ip_dest):
    #set ACL1
    # npr.set_ACL(sdw1_connect, 101, ip_src, "0.0.0.255", ip_dest, "0.0.0.255", [])
    # tracert
    A = npr.get_int("sdwan2_1", "Gi1/0/1", sdw1_connect)
    B = npr.get_int("sdwan2_2", "Gi1/0/2", sdw1_connect)
    #C = npr.get_latency("sdwan2_1", ip_src, ip_dest, sdw1_connect)
    C = npr.get_latency_2(ip_dest)
    return A,B,C
    #set ACL2

def collect_():
    sdw1_connect, sdw2_connect = npr.create_SSH()
    
    npr.delete_SSH(sdw1_connect, sdw2_connect)

def loop_collection(child_conn):
    msg = "Hello"
    child_conn.send(msg)
    child_conn.close()

class StageController:
    def stageCTR(self, queueSCTR, queueSAI):
        print("stage1")
        while True:
            sdw1_connect = npr.create_SSH(1)
          # to avoid unnecessary waiting
            if not queueSAI.empty():
                msg = queueSAI.get()    # get msg from SAI
                Cport = []
                if (msg == "update lists"):
                    print("! ! ! SController RECEIVED from SAI:", msg)
                else :
                    Cport = msg.split('|') ## example : 80|40
            npr.set_ACL(sdw1_connect, 101, cisco_addr_src = "192.168.4.1", cisco_mask_src = "255.255.255.0", port=Cport)
            time.sleep(1) # work
            PreQueue = ""
            try:
                A, B, C= collect_notraffic("192.168.4.1", "192.168.140.1")
                PreQueue = str(A) + "|" + str(B) + "|" + str(C)
            except:
                PreQueue = "ERR_DATA"
            queueSCTR.put(PreQueue)
            npr.delete_SSH(sdw1_connect)
        queueS1.put('s1 is DONE')

if __name__ == "__main__":
    A, B, C = collect_notraffic("192.168.4.1", "192.168.140.1")
    A, B, C = collect_notraffic("192.168.4.22", "192.168.140.10")
    print(A)
    print(B)
    print(C)