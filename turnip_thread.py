import threading
from turnip_head import TurnipHead

class TurnipThread():

    def __init__(self):
        self.turnip: TurnipHead = TurnipHead()
        self.threadStart: threading.Thread = threading.Thread(target=self.turnip.run, daemon=True)
        self.threadStop: threading.Thread = threading.Thread(target=self.turnip.stop, daemon=True)

    def start(self):
        self.threadStart.start()

    def stop(self):
        self.threadStop.start()
        self.threadStart.join()
