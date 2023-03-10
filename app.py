# Continuation of the skeleton code posted to Ed
from multiprocessing import Process, Queue
import os
import socket
from _thread import *
import logging
import time
from threading import Thread
import random
 

# consumer thread which is almost constantly adding messages into the message queue
def consumer(conn):
    # arbitrary sleep value -- can be changed, however we wanted it to be less than the quickest possible clock rate
    sleepVal = 0.05
    while True:
        time.sleep(sleepVal)
        data = conn.recv(1024)
        dataVal = data.decode('ascii')
        # only add non-empty messages to the queue
        if dataVal != '':
            msg_queue.put(dataVal)
 

# producer thread handles most of the logic
def producer(portVals):
    # one producer thread connects to both other machines through sockets
    host = "127.0.0.1"
    hostPort, port1, port2 = portVals[1], portVals[2], portVals[3]
    sock1, sock2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM), socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # initiate the logical clock to 0 and set the clock speed randomly
    logical_clock = 0
    clock_speed = random.randint(1,6)

    # setting up basic logging, always includes system time
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        filename=(str(hostPort)+'.log'), 
        level=logging.DEBUG, 
        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info("Starting processes for host " + str(hostPort) + " with " + str(clock_speed) + " operations per second.")

    try:
        sock1.connect((host,port1))
        logging.info("Client-side connection success to port val:" + str(port1) + "\n")
        sock2.connect((host,port2))
        logging.info("Client-side connection success to port val:" + str(port2) + "\n")

        while True:
            # sleep to emulate the correct amount of actions per second according to the clock speed
            time.sleep(1.0/clock_speed)
            if msg_queue.empty():
                # always increment logical clock on every action, then enter main logic flow
                logical_clock += 1
                code = random.randint(1,10)
                if code == 1:
                    sock1.send(str(logical_clock).encode('ascii'))
                    logging.info("Message sent to: " + str(port1) + " | local logical clock time: " + str(logical_clock))

                if code == 2:
                    sock2.send(str(logical_clock).encode('ascii'))
                    logging.info("Message sent to: " + str(port2) + " | local logical clock time: " + str(logical_clock))

                if code == 3:
                    sock1.send(str(logical_clock).encode('ascii')) 
                    sock2.send(str(logical_clock).encode('ascii'))
                    logging.info("Messages sent to: " + str(port1) + " and " + str(port2) + " | local logical clock time: " + str(logical_clock))

                # internal event should do nothing but log
                else:
                    logging.info("Internal event | local logical clock time: " + str(logical_clock))

            # when we receive a message, we want to synchronize with other clocks in the system by taking the maximum
            # value of the current clock and the one we receive a message from
            else:
                msg = msg_queue.get()
                logical_clock = max(logical_clock, int(msg))+1
                logging.info("Message received: " + msg + " | local logical clock time: " + str(logical_clock) + " | length of message queue: " + str(msg_queue.qsize()))
    
    except socket.error as e:
        print ("Error connecting producer: %s" % e)
    

# basic machine initalization -- specifies host and port and creates the consumer thread
def init_machine(config):
    HOST = str(config[0])
    PORT = int(config[1])
    print("starting server | port val: ", PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, _ = s.accept()
        start_new_thread(consumer, (conn,))
 

def machine(config):
    config.append(os.getpid())

    # initalize a global message queue for each machine
    global msg_queue
    msg_queue = Queue()

    init_thread = Thread(target=init_machine, args=(config,))
    init_thread.start()

    # add delay to initialize the server-side logic on all processes
    time.sleep(5)
    # one producer handles both other machines
    prod_thread = Thread(target=producer, args=(config,))
    prod_thread.start()
    

# main block
if __name__ == '__main__':
    localHost= "127.0.0.1"
    port1 = 2056
    port2 = 3056
    port3 = 4056
    
    # configuration of the three machines which can interact with the others
    config1=[localHost, port1, port2, port3]
    p1 = Process(target=machine, args=(config1,))
    config2=[localHost, port2, port3, port1]
    p2 = Process(target=machine, args=(config2,))
    config3=[localHost, port3, port1, port2]
    p3 = Process(target=machine, args=(config3,))
    
    # starting up all processes
    p1.start()
    p2.start()
    p3.start()
    
    p1.join()
    p2.join()
    p3.join()