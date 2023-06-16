import NetPBR as npr
import time
import random
import numpy
import logging
import signal
import sys
import ast

end = False

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    end = True
    sys.exit(0) # To be remove


def collect_notraffic(sdw1_connect, ip_src, ip_dest):
    A = npr.get_int("sdwan2_1", "Gi1/0/1", sdw1_connect)
    B = npr.get_int("sdwan2_2", "Gi1/0/2", sdw1_connect)
    C = npr.get_latency_3(ip_dest)
    logging.info("collect_notraffic -> C = " + str(C))
    return A,B,C

def loop_collection(child_conn):
    msg = "Hello"
    child_conn.send(msg)
    child_conn.close()

class StageController:
    ACL_SET = False
    def __init__(self):
        logging.basicConfig(filename="src/logs/Controller.log",
                             level=logging.INFO,
                             format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        signal.signal(signal.SIGINT, signal_handler)
        self.SetACL = False
        
    def stageCTR(self, queueSCTR, queueSAI):
        print("stage1")
        latency_data = [1, 1, 1 , 1 , 1, 1, 1, 1, 1]
        idx = 0
        while not end:
            # Check if Request is receive 
            sdw1_connect = npr.create_SSH(1)
            Cport = []

            # Perform Action
            if not queueSAI.empty():
                msg = queueSAI.get()    # get msg from SAI
                if (msg == "update lists"):
                    print("! ! ! SController RECEIVED from SAI:", msg)
                elif(msg.isnumeric()):
                    if (self.SetACL):
                        self.SetACL = False
                        Cport = ["NOACL"]
                    else:
                        self.SetACL = True
                        Cport = ["80", "443"]
                else :
                    Cport = msg.split('|') ## example : 80|40
            npr.set_ACL(sdw1_connect, 101, cisco_addr_src = "192.168.4.0", cisco_mask_src = "0.0.0.255", port=Cport)
            if Cport == [] or Cport[0] == "NOACL":
                ACL_SET = False
            else:
                ACL_SET = True
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
                A, B, C = collect_notraffic(sdw1_connect, "192.168.8.254", "192.168.50.9")
                if A["I_rate_bit"] and B["I_rate_bit"]:
                    throughput_I[0] = A["I_rate_bit"]
                    throughput_I[1] = B["I_rate_bit"]
                if A["O_rate_bit"] and B["O_rate_bit"]:
                    throughput_O[0] = A["O_rate_bit"]
                    throughput_O[1] = B["O_rate_bit"]
                if A["O_drop"] and B["O_drop"]:
                    pck_loss[0] = A["O_drop"]
                    pck_loss[1] = B["O_drop"]
                if C != []:
                    logging.info("C = " + str(C))
                    bandwidth = C["ABw"]
                    if idx == 9:
                        idx = 0
                    latency_data[idx] = float(C["RTT-min"])
                    latency_data[idx+1] = float(C["RTT-avg"])
                    latency_data[idx+2] = float(C["RTT-max"])
                    idx += 3
                    logging.info("latency_data = " + str(latency_data))
                    latency_avg = numpy.average(latency_data)
                    latency_sigma = numpy.std(latency_data)
                    latency_max = max(latency_data)
                PreQueue = str(str(lst_service_channel) + "|" + str(throughput_I) + "|" + str(throughput_O) + "|" + str(pck_loss) + "|" + str(latency_avg)  + "|" + str(latency_sigma) + "|" + str(latency_max)  + "|"  + str(bandwidth))
                logging.info(PreQueue)
            except Exception as error:
                PreQueue = "ERR_DATA"
                logging.error(error)
            
            # Prepare Data
            
            # Send Data
            queueSCTR.put(PreQueue)
            npr.remove_SSH(sdw1_connect)
        print(end)
        queueSCTR.put('s1 is DONE')

if __name__ == "__main__":
    sdw1_connect = npr.create_SSH(1)
    A, B, C = collect_notraffic(sdw1_connect, "192.168.8.254", "192.168.50.9")
    # A, B, C = collect_notraffic("192.168.4.22", "192.168.140.10")
    print(A)
    print(B)
    print(C)
    npr.remove_SSH(sdw1_connect)