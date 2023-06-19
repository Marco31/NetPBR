"""Module AI Manage AI thread and communicate with Controller thread."""
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
                # int_sdwan_1 = ast.literal_eval(q_list[0])
                # int_sdwan_2 = ast.literal_eval(q_list[1])
                # latency_sdw1_2_sdw2 = q_list[2]
                lst_service_channel = ast.literal_eval(q_list[0])
                 # throughput_input by interface (bit/s) [Gi1/0/1, Gi1/0/2]
                throughput_input = ast.literal_eval(q_list[1])
                throughput_output = ast.literal_eval(q_list[2])
                pck_loss = ast.literal_eval(q_list[3])
                latency_avg = float(q_list[4])
                latency_sigma = float(q_list[5])
                latency_max = float(q_list[6])
                bandwidth = float(q_list[7])

                print("- - - sAI RECEIVED from sController:")
                print(lst_service_channel)
                print(throughput_input) # by interface
                print(throughput_output) # by interface
                print(pck_loss) # by interface
                print(latency_avg)
                print(latency_sigma)
                print(latency_max)
                print(bandwidth)
                # if network is not full do
                # pre_queue = "NOACL"
                # otherwise if you want  for example to reroute http (80) and https (443) do
                # pre_queue = "80|443"

                if DEBUG:
                    if self.loop_nb % 1000:
                        if self.set_ACL:
                            self.set_ACL = False
                            pre_queue = "NOACL"
                            print("Unset ACL...")
                            logging.info("Unset ACL...")
                        else:
                            self.set_ACL = True
                            pre_queue = "80|443"
                            print("Set ACL for port 80 and 443...")
                            logging.info("Set ACL for port 80 and 443...")
            self.loop_nb +=1
            time.sleep(1) # work
            # Send Request
            queueS2.put(pre_queue)

if __name__ == '__main__':
    print("Start AI")
