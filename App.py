from multiprocessing import Process, Queue
import collection
import AI

if __name__ == '__main__':
    s1= collection.Stage1()
    s2= AI.Stage2()

    # collection to AI communication
    queueS1 = Queue()  # s1.stage1() writes to queueS1

    # AI to collection communication
    queueS2 = Queue()  # s2.stage2() writes to queueS2

    # start AI as another process
    s2 = Process(target=s2.stage2, args=(queueS1, queueS2))
    s2.daemon = True
    s2.start()     # Launch the AI process

    s1.stage1(queueS1, queueS2) # start sending stuff from s1 to s2 
    s2.join() # wait till s2 daemon finishes
