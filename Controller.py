import NetPBR as npr
import time
import random


def collect_notraffic(ip_src, ip_dest):
    sdw1_connect = npr.create_SSH(1)
    #set ACL1
    npr.set_ACL(sdw1_connect, 101, ip_src, "0.0.0.255", ip_dest, "0.0.0.255", [])
    # tracert
    A = npr.get_int("sdwan2_1", "Gi1/0/1", sdw1_connect)
    B = npr.get_int("sdwan2_2", "Gi1/0/2", sdw1_connect)
    C = npr.get_latency("sdwan2_1", ip_src, ip_dest, sdw1_connect)
    return A,B,C
    #set ACL2
    
    npr.delete_SSH(sdw2_connect)

def collect_():
    sdw1_connect, sdw2_connect = npr.create_SSH()
    
    npr.delete_SSH(sdw1_connect, sdw2_connect)

def loop_collection(child_conn):
    msg = "Hello"
    child_conn.send(msg)
    child_conn.close()

class Stage1:
    def stage1(self, queueS1, queueS2):
        print("stage1")
        lala = []
        lis = [1, 2, 3, 4, 5]
        for i in range(len(lis)):
          # to avoid unnecessary waiting
            if not queueS2.empty():
                msg = queueS2.get()    # get msg from s2
                print("! ! ! stage1 RECEIVED from s2:", msg)
                lala = [6, 7, 8] # now that a msg was received, further msgs will be different
            time.sleep(1) # work
            random.shuffle(lis)
            A, B, C = collect_notraffic("192.168.4.1", "192.168.140.1")
            A = str(A)
            # queueS1.put(lis + lala)
            queueS1.put(A)
        queueS1.put('s1 is DONE')

if __name__ == "__main__":
    A, B, C = collect_notraffic("192.168.4.1", "192.168.140.1")
    print(A)