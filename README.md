# Scale Models and Logical Clocks
By Michael Sacco and John Minicus

### Lab Notebook

We started off this project by using the skeleton code provided on Canvas -- our first task was to understand exactly how this code worked so that we know how to refactor it to fit the project. Here are the design choices we made during this refactoring:
- Initially, the skeleton code was only able to produce messages for one other machine, so we knew that we would have to somehow allow each machine to talk to two others. We first tried to do this by creating two producer threads (one for each of the other two machines) in the machine() function, however this ran into a problem -- since we wanted to include the logic for sending messages within the function for the producer thread (the actions based on the random number from 1-10), there was no way to send a message to machine 3 (if the random number told us to) if we were already in machine 2's producer thread. We fixed this by creating one producer thread for each machine with two sockets, one for each of the other two machines. That way, we can run the random number generator within the producer thread and then just choose which socket to send with if we need to send a message.
- We needed an object for a message queue for each machine. Originally, we just used an  empty list that was held globally and intiated by the machine() function, however we learned of the more useful multiprocessing.Queue class which was a safer option when using multiple threads. This is stored globally as well, and the consumer thread for each machine repeatedly checks for new messages to put in the queue much quicker than the machine's clock speed, as these are unrelated processes.
- We create the logical clock for each machine by intiating a counter to 0 at the start of each machine's producer thread. It made sense to us to put the clock here (rather than at the machine's intialization) because the only functionality which should increase the logical clock is located within the producer function. If the queue is empty, every following action increases the clock by 1. However if the queue has a message, to avoid clock drift and keep the system as synchronized as possible, we set the logical clock to the maximum between the current clock and the clock of the machine the message was sent from (given by the text of the message itself).

Other than these main bulletpoints, the project was pretty straightforward and we did not run into much issue.

### Observations

words.