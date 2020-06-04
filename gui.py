import tkinter as tk
import threading
from turnip_head import TurnipHead
from turnip_thread import TurnipThread


class TurnipGUI():
    """
    Threaded Turnip GUI.

    Support stopping and starting of the turnip scraper.
    """

    def __init__(self):
        self.root = tk.Tk()
        self.root.wm_title("Turnip")
        self.root.wm_iconbitmap("turnip.ico")

        frame = tk.Frame(master=self.root, width=100, height=100, padx=5, pady=5)
        frame.grid(row=0, column=0)

        label = tk.Label(master=frame, text="Interval (seconds)")
        label.grid(row=0, column=0)

        self.entry = tk.Entry(master=frame)
        self.entry.grid(row=1, column=0)

        start_button = tk.Button(
            master=self.root,
            relief=tk.RAISED,
            text="Start",
            width=10,
            height=2,
        )
        start_button.grid(row=0, column=1, padx=5, pady=5)
        start_button.bind("<Button-1>", self.handle_start_button)

        stop_button = tk.Button(
            master=self.root,
            relief=tk.RAISED,
            text="Stop",
            width=10,
            height=2,
        )
        stop_button.grid(row=0, column=2, padx=5, pady=5)
        stop_button.bind("<Button-1>", self.handle_stop_button)

        self.turnip: TurnipHead = TurnipHead()
        self.threadStart: threading.Thread = threading.Thread(target=self.turnip.run)
        self.threadStop: threading.Thread = threading.Thread(target=self.turnip.stop)


    def handle_start_button(self, event):
        """Handle logic for start button"""
        
        try:
            self.turnip.INTERVAL = int(self.entry.get())
            print(f"Setting interval to {self.turnip.INTERVAL}")
        except ValueError:
            print("Input is not an integer")

        try:
            if self.threadStart.is_alive():
                print("Thread is already running")
                return

            self.threadStart.start()
            print("Starting thread")
        except RuntimeError:
            self.threadStart = threading.Thread(target=self.turnip.run)
            self.threadStart.start()
            print("Starting thread")
        

    def handle_stop_button(self, event):
        """Handle logic for stop button"""

        try:
            # Turnip is already stopped
            if not self.turnip.TURNIP_RUNNING:
                print("Turnip will no longer loop")
            
            # Stop turnip
            self.threadStop.start()
            print("Sent stop signal")

        except RuntimeError:
            # Turnip is in the middle of stopping
            if self.threadStart.is_alive():
                print("Thread is still stopping")
                return

            # Stop turnip
            self.threadStop = threading.Thread(target=self.turnip.stop)
            self.threadStop.start()
            print("Sent stop signal")


    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    turnipGui = TurnipGUI()
    turnipGui.run()
