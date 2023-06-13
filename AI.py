import time
import ast

class StageAI:
    def stageAI(self, queueS1, queueS2):
        print("stage2")
        while True:
            msg = queueS1.get()    # wait till there is a msg from sController
            if (msg == "ERR_CISCO"):
                print("Cisco switch disconnect")
            elif (msg == "ERR_DATA"):
                print("Data not ready")
            else:
                Qlist = msg.split('|')
                int_sdwan_1 = ast.literal_eval(Qlist[0])
                int_sdwan_2 = ast.literal_eval(Qlist[1])
                latency_sdw1_2_sdw2 = Qlist[2]
                print("- - - sAI RECEIVED from sController:")
                print(int_sdwan_1)
                print(int_sdwan_2)
                print(latency_sdw1_2_sdw2)
                # print(int_sdwan_1["cisco_name"])
                if msg == 's1 is DONE ':
                    break # ends loop
            time.sleep(1) # work
            queueS2.put("update lists")

def training():
    print("training...")
    # AI stuffs

if __name__ == '__main__':
    print("Start AI")