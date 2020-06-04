import threading
from turnip_head import TurnipHead


class TurnipThread():

    def __init__(self):
        self.turnip: TurnipHead = TurnipHead()
        self.threadStart: threading.Thread = threading.Thread(target=self.turnip.run, daemon=True)
        self.threadStop: threading.Thread = threading.Thread(target=self.turnip.stop, daemon=True)

    def start(self, event):
        if self.threadStart.isAlive():
            print("Thread is already running")
            return

        self.threadStart = threading.Thread(target=self.turnip.run)
        self.threadStart.start()
        print("Starting thread")

    def stop(self, event):
        self.threadStop = threading.Thread(target=self.turnip.stop)
        self.threadStop.start()
        self.threadStart.join()
        print("Sent stop signal")