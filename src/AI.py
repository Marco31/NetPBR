"""Module AI Manage AI thread and communicate with Controller thread."""

__author__ = 'Marc VEYSSEYRE'

import time
import ast
import logging

DEBUG = True

class StageAI:
    """Class representing a AI thread"""
    def __init__(self):
        logging.basicConfig(filename="src/logs/AI.log",
            level=logging.INFO,
            format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
        logging.info("Init AI...")
        print("Init AI...")
        self.loop_nb = 0
        self.set_ACL = False
        self.lst_service_channel = None
        self.throughput_input = None
        self.throughput_output = None
        self.pck_loss = None
        self.latency_avg = None
        self.latency_sigma = None
        self.latency_max = None
        self.bandwidth_before_after = None

    def pased_q_list(self, qlst):
        """Function to parse queue list send from Controler into data useful for AI."""
        # latency_sdw1_2_sdw2 = q_list[2]
        self.lst_service_channel = ast.literal_eval(qlst[0])
         # throughput_input by interface (bit/s) [Gi1/0/1, Gi1/0/2]
        self.throughput_input = ast.literal_eval(qlst[1])
        self.throughput_output = ast.literal_eval(qlst[2])
        self.pck_loss = ast.literal_eval(qlst[3])
        self.latency_avg = float(qlst[4])
        self.latency_sigma = float(qlst[5])
        self.latency_max = float(qlst[6])
        self.bandwidth = float(qlst[7])
        self.latency_avg_before_after = []
        self.bandwidth_before_after = []

    def stage4AI(self, queueS1, queueS2):
        """Function where AI thread is start."""
        print("stage2")
        while True:
            # Check if Request is receive
            pre_queue = "update lists"
            msg = queueS1.get()    # wait till there is a msg from sController

            if msg == "ERR_CISCO":
                print("Cisco switch disconnect")
            elif msg == "ERR_DATA":
                print("Data not ready")
            elif msg == 's1 is DONE ':
                break # ends While loop
            elif(self.loop_nb == 0):
                pre_queue = "NOACL"
            else:
                # Perform Action
                q_list = msg.split('|')
                self.pased_q_list(q_list)
                if len(self.latency_avg_before_after) == 1:
                    self.latency_avg_before_after.append(self.latency_avg)
                    self.bandwidth_before_after.append(self.bandwidth)
                elif len(self.latency_avg_before_after) == 2:
                    self.latency_avg_before_after = []
                    self.bandwidth_before_after = []

                print("- - - sAI RECEIVED from sController:")
                print(self.lst_service_channel)
                print(self.throughput_input) # by interface
                print(self.throughput_output) # by interface
                print(self.pck_loss) # by interface
                print(self.latency_avg)
                print(self.latency_sigma)
                print(self.latency_max)
                print(self.bandwidth)
                # if network is not full do
                # pre_queue = "NOACL"
                # otherwise if you want  for example to reroute http (80) and https (443) do
                # pre_queue = "80|443"

                if DEBUG:
                    print("self.loop_nb :" + str(self.loop_nb))
                    if self.loop_nb % 2 == 0:
                        if self.set_ACL:
                            self.set_ACL = not self.set_ACL
                            self.latency_avg_before_after = [self.latency_avg]
                            self.bandwidth_before_after = [self.bandwidth]
                            # pre_queue = "80|443|1000"
                            # print("Set ACL for port 80 and 443 (2)...")
                            pre_queue = "NOACL"
                            print("No ACL")
                            logging.info("No ACL")
                        else:
                            self.set_ACL = not self.set_ACL
                            self.latency_avg_before_after = [self.latency_avg]
                            self.bandwidth_before_after = [self.bandwidth]
                            # pre_queue = "1"
                            pre_queue = "80|443|1000"
                            print("Switch ACL mode")
                            logging.info("Switch ACL mode")
                    else :
                        pre_queue = "0"
            self.loop_nb +=1
            time.sleep(1) # work
            # Send Request
            queueS2.put(pre_queue)
            print("Applied")
            time.sleep(7) # work

if __name__ == '__main__':
    print("Start AI")
