import Pyro4
import ping_ack.server as detector
import subprocess
import pyro_failure as failure
import datetime
import time
import threading

def get_server():
    #ganti "localhost dengan ip yang akan anda gunakan sebagai server" 
    uri = "PYRONAME:greetserver@localhost:7777"
    gserver = Pyro4.Proxy(uri)
    return gserver

if __name__=='__main__':
    server = get_server()
    if server == None:
        exit()
    connected = True
    while connected:
        req = input ("> ").lower()
        req_split = req.split()
        if req_split[0] == 'list':
            print(server.get_list_dir(req))
        elif req_split[0] == 'create':
            print(server.create_handler(req))
        elif req_split[0] == 'delete':
            print(server.delete_handler(req))
        elif req_split[0] == 'read':
            print(server.read_handler(req))
        elif req_split[0] == 'update':
            print(server.update_handler(req))
        elif req_split[0] == 'exit':
            print(server.bye())
            connected = False
        else:
            print(server.command_not_found())


@Pyro4.expose
class FailureDetectorServer(failure.PyroFailureDetector):
    def __init__(self, deltaTime: datetime.timedelta, identifier="MAIN-FD", broadcastTargets=[], pingTargets=[]):
        self.broadcastTargets = broadcastTargets
        self.pingTargets = pingTargets
        self.deltaTime = deltaTime
        super().__init__(identifier, deltaTime)
        self.__run__daemon__()
        thread = threading.Thread(target=self.__check__daemon__)
        thread.daemon = True
        thread.start()

    def __check__daemon__(self):
        print("Daemon is running")
        sleepDuration = self.deltaTime.total_seconds()
        while True:
            time.sleep(sleepDuration)
            self.Broadcast(self.broadcastTargets)
            currentTime = datetime.datetime.now()
            for target in self.pingTargets:
                if not self.Ping(target):
                    print("[%s][PING] Service %s is down!" % (currentTime.strftime("%m/%d/%Y, %H:%M:%S"), target))

    def Ack(self):
        return super().Ack()

    def OnNotify(self, host, sequence):
        return super().OnNotify(host, sequence)