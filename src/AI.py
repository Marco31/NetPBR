import time
import ast
import logging

DEBUG = True

class StageAI:
    def __init__(self):
        logging.basicConfig(filename="src/logs/AI.log",
                             level=logging.INFO,
                             format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        logging.info("Init AI...")
        print("Init AI...")
        self.loop_nb = 0
        self.SetACL = False
    def stage4AI(self, queueS1, queueS2):
        print("stage2")
        while True:
            # Check if Request is receive 
            PreQueue = "update lists"
            msg = queueS1.get()    # wait till there is a msg from sController

            if (msg == "ERR_CISCO"):
                print("Cisco switch disconnect")
            elif (msg == "ERR_DATA"):
                print("Data not ready")
            elif msg == 's1 is DONE ':
                break # ends While loop
            elif(self.loop_nb == 0):
                PreQueue = "NOACL"
            else:
                # Perform Action
                Qlist = msg.split('|')
                # int_sdwan_1 = ast.literal_eval(Qlist[0])
                # int_sdwan_2 = ast.literal_eval(Qlist[1])
                # latency_sdw1_2_sdw2 = Qlist[2]
                lst_service_channel = ast.literal_eval(Qlist[0])
                throughput_I = ast.literal_eval(Qlist[1]) # throughput_Input by interface (bit/s) [Gi1/0/1, Gi1/0/2]
                throughput_O = ast.literal_eval(Qlist[2])
                pck_loss = ast.literal_eval(Qlist[3])
                latency_avg = float(Qlist[4])
                latency_sigma = float(Qlist[5])
                latency_max = float(Qlist[6])
                bandwidth = float(Qlist[7])

                print("- - - sAI RECEIVED from sController:")
                print(lst_service_channel)
                print(throughput_I) # by interface
                print(throughput_O) # by interface
                print(pck_loss) # by interface
                print(latency_avg)
                print(latency_sigma)
                print(latency_max)
                print(bandwidth)
                # if network is not full do
                # PreQueue = "NOACL"
                # otherwise if you want  for example to reroute http (80) and https (443) do
                # PreQueue = "80|443"

                if DEBUG:
                    if self.loop_nb % 1000:
                        if self.SetACL:
                            self.SetACL = False
                            PreQueue = "NOACL"
                            print("Unset ACL...")
                            logging.info("Unset ACL...")
                        else:
                            self.SetACL = True
                            PreQueue = "80|443"
                            print("Set ACL for port 80 and 443...")
                            logging.info("Set ACL for port 80 and 443...")
            self.loop_nb +=1
            time.sleep(1) # work
            # Send Request
            queueS2.put(PreQueue)

if __name__ == '__main__':
    print("Start AI")