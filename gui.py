import tkinter as tk
import threading
from turnip_head import TurnipHead


class TurnipGUI():
    def __init__(self):
        self.turnip: TurnipHead = TurnipHead()
        self.threadStart: threading.Thread = threading.Thread(target=self.turnip.run)
        self.threadStop: threading.Thread = threading.Thread(target=self.turnip.stop)

    def handle_start_button(self, event):
        self.threadStart.start()
        print("Starting thread")

    def handle_stop_button(self, event):
        self.threadStop.start()
        print("Stopping threads")

    def run(self):
        window = tk.Tk()

        entry = tk.Entry(
            master=window
        )
        entry.grid(row=0, column=0, padx=5, pady=5)

        start_button = tk.Button(
            master=window,
            relief=tk.RAISED,
            text="Start",
            width=10,
            height=2,
        )
        start_button.grid(row=0, column=1, padx=5, pady=5)
        start_button.bind("<Button-1>", self.handle_start_button)

        stop_button = tk.Button(
            master=window,
            relief=tk.RAISED,
            text="Stop",
            width=10,
            height=2,
        )
        stop_button.grid(row=0, column=2, padx=5, pady=5)
        stop_button.bind("<Button-1>", self.handle_stop_button)

        window.mainloop()

if __name__ == "__main__":
    turnipGui = TurnipGUI()
    turnipGui.run()
