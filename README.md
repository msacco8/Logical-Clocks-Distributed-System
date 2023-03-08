# Scale Models and Logical Clocks
By Michael Sacco and John Minicus

To run the application:

```
python3 app.py
```

Log files will be created in the home directory, logs that were used in the discussion of observations are in the logs directory.

### Lab Notebook

We started off this project by using the skeleton code provided on Canvas -- our first task was to understand exactly how this code worked so that we know how to refactor it to fit the project. Here are the design choices we made during this refactoring:
- Initially, the skeleton code was only able to produce messages for one other machine, so we knew that we would have to somehow allow each machine to talk to two others. We first tried to do this by creating two producer threads (one for each of the other two machines) in the machine() function, however this ran into a problem -- since we wanted to include the logic for sending messages within the function for the producer thread (the actions based on the random number from 1-10), there was no way to send a message to machine 3 (if the random number told us to) if we were already in machine 2's producer thread. We fixed this by creating one producer thread for each machine with two sockets, one for each of the other two machines. That way, we can run the random number generator within the producer thread and then just choose which socket to send with if we need to send a message.
- We needed an object for a message queue for each machine. Originally, we just used an  empty list that was held globally and intiated by the machine() function, however we learned of the more useful multiprocessing.Queue class which was a safer option when using multiple threads. This is stored globally as well, and the consumer thread for each machine repeatedly checks for new messages to put in the queue much quicker than the machine's clock speed, as these are unrelated processes.
- We create the logical clock for each machine by intiating a counter to 0 at the start of each machine's producer thread. It made sense to us to put the clock here (rather than at the machine's intialization) because the only functionality which should increase the logical clock is located within the producer function. If the queue is empty, every following action increases the clock by 1. However if the queue has a message, to avoid clock drift and keep the system as synchronized as possible, we set the logical clock to the maximum between the current clock and the clock of the machine the message was sent from (given by the text of the message itself).

Other than these main bulletpoints, the project was pretty straightforward and we did not run into much issue.

### Observations

Our first trial gave us a rate of 1 cycle per second for all the machines, which was not of much use to us but allowed us to contextualize the rest of the trials. As expected, there were very few jumps in each machine's logs because they were cycling relatively slow and at the same rate. Our second trial tested the had the 3 machines timing's set to 4, 5 and 6. The machine with the highest rate had a local clock that was frequently ahead of the messages received, and had very few jumps. There was often a large spread between the messages received from the other machines and the local clock but not to the degree present in some of the other trials with a greater difference between rates. An interesting case occurred where two machines had a higher and equal rate, while the 3rd had a rate of 1 cycle per second. Both of the higher rate machines acted similarly, receiving occasional messages that were 4 or 5 cycles behind their own local clock. The 3rd machine's message queue kept growing and it didn't appear that it would stop. The jumps in time grew from around 4-5 to 6-8 as the message queue remained full and this growth appeared to continue as its queue became more backed up. After this trial, we received another that was not useful and discarded it, where the rates we got were 2, 2 and 1. Similar to the trial in which we had high rates that were separated by 1, we had a trial with rates of 3, 2 and 1. This was the first instance of noticing waves of message queue length, where it would grow and shrink in a short period many times throughout the trial. This occurred for the machine with the slowest rate. Both other machines had very few jumps, and this was likely due to a lesser allowance for variance given the overall lower rate in the machines. Our final trial without modifying the original factors had a leading machine at a rate of 6 operations per second, with the two other machines at 2 and 1. The machine with the greatest rate rarely received any messages and was constantly updating the other machines with times that were very spread out from their own local clocks. For the slowest machine, the only operations that occurred were the receptions of messages, and the message queue instantly began growing rapidly and with no sign of stopping. Jumps of up to 20 cycles occurred, and this number would likely only continue to grow if left running. The middle machine exhibited the behavior in which the message queue would swell, and there were frequent large jumps of up to 8-10 cycles per.

1 operation - 2056 - no jumps, at one point received message from both ports of the same logical clock time obviously makes sense that clocks would be synchronized when they all have the same clock rate
1 operation - 3056 - 1 small jump of 1 cycle
1 operation - 4056 - no jumps, similar to 2056 in that there was one message received in which local clock time was the maximum

5 operations - 2056 - frequent jumps of 1 or 2, frequent messages received that are 1 or 2 behind
6 operations - 3056 - frequently ahead of messages received, almost no jumps, large spread between message and local clock at 5 cycles
4 operations - 4056 - frequent jumps, rarely ahead, jumps often in the range of 2-5 cycles

4 operations - 2056 - occassionally receives a message that is 4-5 cycles behind, mostly on time with little to no jumps
1 operation - 3056 - expectation that it frequently receives jumps of 3-4 cycles. Message queue seemed to start growing and didn't look like it was going to stop. Jumps were of 3-4. When the message queue was constantly full jumps became up to 6-8
4 operations - 4056 - occassionally receives a message that is 4-5 cycles behind, mostly on time with little to no jumps

<!-- NOT USEFUL
2 operations - 2056
2 operations -3056
1 operations - 4056 -->

3 operations - 2056 - Very few, if any, jumps. Often received messages from behind which makes sense given the other clock rates of the ports
2 operations - 3056 - Interestingly no jumps, probably the proximity of the clock rates, frequently lagged behind even to a greater extent than the 3 cycles per second machine. Seems to be unexpected behavior.
1 operations - 4056 - large and frequent jumps message queue often got large but then shrunk back down unlike the other scenario in which it seemed it would grow forever. Jumps occurred at 4-5 cycles per.

1 operation - 2056 - every cycle a message was received, and because of the cycle rate of the consumer the length of the message queue from the perspective of the log jumped between lines. Large jumps up to 20 cycles occurred in this run and it appears if given enough time the message queue would grow infinitely
2 operations - 3056 - Frequent large jumps, message queue would grow and shrink to empty in many swells throughout the log. Jumps could be as big as 8-10 and occurred frequently.
6 operations - 4056 - Rarely received messages, but received lower clock rates usually by around 8-10 cycles. Driving force of the 3 machines communicating due to its cycle rate, constantly sending messages to other machines updating their logical clocks with its rate

Once you have run this on three virtual machines that can vary their internal times by an order of magnitude, try running it with a smaller variation in the clock cycles and a smaller probability of the event being internal. What differences do those variations make? Add these observations to your lab notebook. Play around, and see if you can find something interesting.









words.