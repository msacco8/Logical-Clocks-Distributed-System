# Sample Code in Python
from multiprocessing import Process, Queue
import os
import socket
from _thread import *
import threading
import time
from threading import Thread
import random
 

def consumer(conn):
    print("consumer accepted connection" + str(conn)+"\n")
    sleepVal = 0.1
    while True:
        time.sleep(sleepVal)
        data = conn.recv(1024)
        dataVal = data.decode('ascii')
        if dataVal != '':
            msg_queue.put(dataVal)
 

def producer(portVals):
    host = "127.0.0.1"
    logical_clock = 0
    port1, port2 = int(portVals[0]), int(portVals[1])
    sock1, sock2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM), socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    clock_speed = random.randint(1,6)
    #sema acquire
    try:
        sock1.connect((host,port1))
        print("Client-side connection success to port val:" + str(port1) + "\n")
        sock2.connect((host,port2))
        print("Client-side connection success to port val:" + str(port2) + "\n")

        ######## probably delete -- want to send messages randomly according to RNG
        # while True:
        #     codeVal = str(1)
        #     time.sleep(sleepVal)
        #     s.send(codeVal.encode('ascii'))
        #     print("msg sent", codeVal)

        while True:
            time.sleep(1.0/clock_speed)
            if msg_queue.empty():
                logical_clock += 1
                code = random.randint(1,10)
                if code == 1:
                    sock1.send(str(logical_clock).encode('ascii'))
                    # LOG

                if code == 2:
                    sock2.send(str(logical_clock).encode('ascii'))
                    # LOG

                if code == 3:
                    sock1.send(str(logical_clock).encode('ascii')) 
                    sock2.send(str(logical_clock).encode('ascii'))

                else:
                    pass
                    # INTERNAL EVENT: DO NOTHING BUT LOG

            else:
                msg = msg_queue.get()
                print(msg)
                logical_clock = max(logical_clock+1, int(msg))
                # LOG THIS
    
    except socket.error as e:
        print ("Error connecting producer: %s" % e)
    

def init_machine(config):
    HOST = str(config[0])
    PORT = int(config[1])
    print("starting server| port val:", PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        start_new_thread(consumer, (conn,))
 

def machine(config):
    config.append(os.getpid())

    global msg_queue
    msg_queue = Queue()

    #print(config)
    init_thread = Thread(target=init_machine, args=(config,))
    init_thread.start()
    #add delay to initialize the server-side logic on all processes
    time.sleep(5)
    # extensible to multiple producers
    prod_thread = Thread(target=producer, args=(config[2:],))
    prod_thread.start()


localHost= "127.0.0.1"
    
if __name__ == '__main__':
    port1 = 2056
    port2 = 3056
    port3 = 4056
    
    config1=[localHost, port1, port2, port3]
    p1 = Process(target=machine, args=(config1,))
    config2=[localHost, port2, port3, port1]
    p2 = Process(target=machine, args=(config2,))
    config3=[localHost, port3, port1, port2]
    p3 = Process(target=machine, args=(config3,))
    
    p1.start()
    p2.start()
    p3.start()
    
    p1.join()
    p2.join()
    p3.join()