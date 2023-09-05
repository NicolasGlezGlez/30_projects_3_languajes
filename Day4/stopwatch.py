import tkinter as tk

class StopwatchApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Stopwatch")
        
        # Initialize the label to display the stopwatch time
        self.label = tk.Label(self.master, text="00:00:000", font=("Arial", 48))
        self.label.pack()
        
        # Initialize buttons and attach functions to them
        tk.Button(self.master, text="Start", command=self.start_timer).pack(side="left")
        tk.Button(self.master, text="Stop", command=self.stop_timer).pack(side="left")
        tk.Button(self.master, text="Reset", command=self.reset_timer).pack(side="left")
        
        # Initialize variables to keep track of the time and the state of the stopwatch
        self.running = False
        self.counter = 0

    def update_label(self):
        """Updates the stopwatch label."""
        if self.running:
            mins, rest_secs = divmod(self.counter, 60000)
            secs, millis = divmod(rest_secs, 1000)
            time_format = "{:02d}:{:02d}:{:03d}".format(mins, secs, millis)
            self.label.config(text=time_format)
        
        # Update every 100 milliseconds
        self.label.after(10, self.update_label)
        self.counter += 100

    def start_timer(self):
        """Starts the stopwatch."""
        self.running = True
        self.update_label()
        
    def stop_timer(self):
        """Stops the stopwatch."""
        self.running = False
        
    def reset_timer(self):
        """Resets the stopwatch to zero."""
        self.counter = 0
        time_format = "{:02d}:{:02d}:{:03d}".format(0, 0, 0)
        self.label.config(text=time_format)

if __name__ == "__main__":
    root = tk.Tk()
    app = StopwatchApp(root)
    root.mainloop()
