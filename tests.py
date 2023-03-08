import unittest
import time
from multiprocessing import Process
from socket import socket, AF_INET, SOCK_STREAM

from app import machine

class TestLogicalClockSetup(unittest.TestCase):

    def setUp(self):
        self.p1 = Process(target=machine, args=([localHost, port1, port2, port3]))
        self.p2 = Process(target=machine, args=([localHost, port2, port3, port1]))
        self.p3 = Process(target=machine, args=([localHost, port3, port1, port2]))
        self.p1.start()
        self.p2.start()
        self.p3.start()

    def tearDown(self):
        self.p1.terminate()
        self.p2.terminate()
        self.p3.terminate()

    def test_message_passing(self):
        """
        Tests that messages can be sent between the machines.
        """
        sock1 = socket(AF_INET, SOCK_STREAM)
        sock2 = socket(AF_INET, SOCK_STREAM)
        sock1.connect((localHost, port1))
        sock2.connect((localHost, port2))

        sock1.send(b"test message")
        time.sleep(1) # give some time for message to be processed

        self.assertFalse(msg_queue.empty())
        self.assertEqual(msg_queue.get(), "test message")

        sock1.close()
        sock2.close()

    def test_logical_clock(self):
        """
        Tests that the logical clock is working correctly.
        """
        sock1 = socket(AF_INET, SOCK_STREAM)
        sock2 = socket(AF_INET, SOCK_STREAM)
        sock1.connect((localHost, port1))
        sock2.connect((localHost, port2))

        # send messages from both machines
        sock1.send(b"message 1")
        sock2.send(b"message 2")
        time.sleep(1) # give some time for messages to be processed

        # make sure the logical clock was incremented and that the correct messages were received
        self.assertEqual(msg_queue.get(), "message 1")
        self.assertEqual(msg_queue.get(), "message 2")
        self.assertTrue(msg_queue.empty())
        self.assertEqual(logical_clock, 3)

        sock1.close()
        sock2.close()

class TestClockSynchronization(unittest.TestCase):
    # setup the three processes before running tests
    def setUp(self):
        self.localHost = "127.0.0.1"
        self.port1 = 2056
        self.port2 = 3056
        self.port3 = 4056
        
        # configuration of the three machines which can interact with the others
        self.config1 = [self.localHost, self.port1, self.port2, self.port3]
        self.p1 = Process(target=machine, args=(self.config1,))
        self.p1.start()
        
        self.config2 = [self.localHost, self.port2, self.port3, self.port1]
        self.p2 = Process(target=machine, args=(self.config2,))
        self.p2.start()
        
        self.config3 = [self.localHost, self.port3, self.port1, self.port2]
        self.p3 = Process(target=machine, args=(self.config3,))
        self.p3.start()
        
        # delay to allow the processes to initialize
        sleep(5)
        
    # terminate the processes after running tests
    def tearDown(self):
        self.p1.terminate()
        self.p2.terminate()
        self.p3.terminate()

    # test if messages are correctly added to the queue by the consumer thread
    def test_consumer_thread(self):
        s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s1.connect((self.localHost, self.port1))
        s1.sendall(b"test message")
        
        # wait for the message to be added to the queue
        sleep(0.1)
        
        # check if the message is in the queue
        self.assertFalse(msg_queue.empty())
        self.assertEqual(msg_queue.get(), "test message")

    # test if the producer thread sends messages correctly
    def test_producer_thread(self):
        # create a socket connection to one of the producer's sockets
        s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s1.connect((self.localHost, self.port1))
        
        # send a message to the producer
        s1.sendall(b"test message")
        
        # wait for the message to be added to the queue and processed by the producer
        sleep(0.1)
        
        # check if the message was sent to the correct socket and if the logical clock was incremented
        self.assertIn("Message sent to:", open(str(self.port2)+'.log').read())
        self.assertIn("local logical clock time:", open(str(self.port2)+'.log').read())
        
    # test if the producer thread synchronizes logical clocks correctly
    def test_clock_synchronization(self):
        # create a socket connection to one of the producer's sockets
        s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s1.connect((self.localHost, self.port1))
        
        # send a message to the producer with a logical clock value of 10
        s1.sendall(b"10")
        
        # wait for the message to be added to the queue and processed by the producer
        sleep(0.1)
        
        # check if the logical clock was incremented to 11
        self.assertIn("local logical clock time: 11", open(str(self.port2)+'.log').read())

if __name__ == '__main__':
    unittest.main()
