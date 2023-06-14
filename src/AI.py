import time
import ast

class StageAI:
    def stageAI(self, queueS1, queueS2):
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
            else:
                # Perform Action
                Qlist = msg.split('|')
                # int_sdwan_1 = ast.literal_eval(Qlist[0])
                # int_sdwan_2 = ast.literal_eval(Qlist[1])
                # latency_sdw1_2_sdw2 = Qlist[2]
                lst_service_channel = list(Qlist[0])
                throughput_I = int(Qlist[1]) # throughput_Input by interface (bit/s) [Gi1/0/1, Gi1/0/2]
                throughput_O = int(Qlist[2])
                pck_loss = list(Qlist[3])
                latency_avg = int(Qlist[4])
                latency_sigma = int(Qlist[5])
                latency_max = int(Qlist[6])
                bandwidth = int(Qlist[7])

                print("- - - sAI RECEIVED from sController:")
                print(lst_service_channel)
                print(throughput_I)
                print(throughput_O)
                print(pck_loss)
                print(latency_avg)
                print(latency_sigma)
                print(latency_max)
                print(bandwidth)
                # if network is not full do
                # PreQueue = "NOACL"
                # otherwise if you want to for example to reroute http (80) and https (443) do
                # PreQueue = "80|443"
                
            time.sleep(1) # work
            # Send Request
            queueS2.put(PreQueue)

if __name__ == '__main__':
    print("Start AI")