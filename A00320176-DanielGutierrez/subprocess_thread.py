import threading
import time

class Concur(threading.Thread):

    def __init__(self):
        #super(Concur, self).__init__()
        self.iter = 0
        #self.agg = 0
        self.daemon = True
        #self.stopped = True  # start out paused
        self.stoprequest = threading.Event()

    def run(self):
        #self.resume() # unpause self
        while not self.stoprequest.isSet():
            #self.agg += 1

            # do stuff
            #time.sleep(.1)
            self.iter += 1
            time.sleep(.1)

    #def resume(self):
        #with self.state:
        #self.stopped = False
            #self.state.notify()  # unblock self if waiting

    def stop(self, timeout):
        #with self.state:
        self.stoprequest.set()
        #super(Concur, self).join(timeout)
        #self.stopped = True  # make self block and wait

    def iterations(self):
        print(self.iter)
