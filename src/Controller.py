import NetPBR as npr
import time
import random
import numpy


def collect_notraffic(sdw1_connect, ip_src, ip_dest):
    A = npr.get_int("sdwan2_1", "Gi1/0/1", sdw1_connect)
    B = npr.get_int("sdwan2_2", "Gi1/0/2", sdw1_connect)
    C = npr.get_latency_2(ip_dest)
    return A,B,C

def loop_collection(child_conn):
    msg = "Hello"
    child_conn.send(msg)
    child_conn.close()

class StageController:
    def stageCTR(self, queueSCTR, queueSAI):
        print("stage1")
        latency_data = []
        while True:
            # Check if Request is receive 
            sdw1_connect = npr.create_SSH(1)
            Cport = []

            # Perform Action
            if not queueSAI.empty():
                msg = queueSAI.get()    # get msg from SAI
                if (msg == "update lists"):
                    print("! ! ! SController RECEIVED from SAI:", msg)
                else :
                    Cport = msg.split('|') ## example : 80|40
            npr.set_ACL(sdw1_connect, 101, cisco_addr_src = "192.168.4.1", cisco_mask_src = "255.255.255.0", port=Cport)
            time.sleep(1) # work

            # Collect & Prepare Data
            PreQueue = ""
            lst_service_channel = []
            throughput_I = [-1, -1]
            throughput_O = [-1, -1]
            pck_loss = [-1.0, -1.0]
            latency_avg = -1
            latency_sigma = -1
            latency_max = -1
            bandwidth = -1
            try:
                A, B, C= collect_notraffic(sdw1_connect, "192.168.4.1", "192.168.50.1")
                if A["I_rate_bit"] and B["I_rate_bit"]:
                    throughput_I[0] = A["I_rate_bit"]
                    throughput_I[1] = B["I_rate_bit"]
                if A["O_rate_bit"] and B["O_rate_bit"]:
                    throughput_O[0] = A["O_rate_bit"]
                    throughput_O[1] = B["O_rate_bit"]
                if A["O_drop"] and B["O_drop"]:
                    pck_loss[0] = A["O_drop"]
                    pck_loss[0] = B["O_drop"]
                if C != []:
                    latency_data.append(C[0])
                    latency_data_work = latency_data[-5:]
                    latency_avg = numpy.average(latency_data_work)
                    latency_sigma = numpy.std(latency_data_work)
                    latency_max = max(latency_data_work)
                # PreQueue = str(A) + "|" + str(B) + "|" + str(C)
                PreQueue = str(lst_service_channel + "|" + throughput_I + "|" + throughput_O + "|" + pck_loss + "|" + latency_avg  + "|" + latency_sigma + "|" + latency_max  + "|"  + bandwidth)
            except:
                PreQueue = "ERR_DATA"
            
            # Prepare Data
            
            # Send Data
            queueSCTR.put(PreQueue)
            npr.remove_SSH(sdw1_connect)

        queueS1.put('s1 is DONE')

if __name__ == "__main__":
    sdw1_connect = npr.create_SSH(1)
    A, B, C = collect_notraffic(sdw1_connect, "192.168.4.1", "192.168.50.1")
    # A, B, C = collect_notraffic("192.168.4.22", "192.168.140.10")
    print(A)
    print(B)
    print(C)
    npr.remove_SSH(sdw1_connect)