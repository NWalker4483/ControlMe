from threading import Thread
import time 
class Engine(Thread):
    def __init__(self,socket):
        Thread.__init__(self)
        self.flow = {}
        self.socket=socket

    def run(self):
        display = ""
        while True:
            time.sleep(0.1)
            #self.flow["Time"] = time.time()
            for i in self.flow:
                flowstr = str(self.flow[i])
                flowstr = flowstr.replace("{","")
                flowstr = flowstr.replace("}","")
                flowstr = flowstr.replace('"',"")
                self.socket.emit("flow",
                            {"data":[i,flowstr]},
                            namespace="/test")	
