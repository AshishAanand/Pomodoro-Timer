from tkinter import *
import time
import threading
from playsound import playsound

class Timer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("500x400")
        self.root.configure(bg="#2C3E50")  # Dark background

        self.running = False
        self.paused = False
        self.promodoro_cycle = 0
        self.set_ui()

    def start_timer(self, seconds, label, session_type):
        self.running = True
        self.paused = False

        def timer_thread():
            nonlocal seconds
            while seconds > 0 and self.running:
                if not self.paused:
                    mins, secs = divmod(seconds, 60)
                    self.update_label(label, f"{session_type}: {mins:02d}:{secs:02d}")
                    time.sleep(1)
                    seconds -= 1
                else:
                    time.sleep(1)

            if self.running and not self.paused:
                playsound("Alert.wav")  # Play sound when timer ends
                self.transition_to_next_session(session_type)

        threading.Thread(target=timer_thread, daemon=True).start()

    def update_label(self, label, text):
        self.root.after(0, lambda: label.config(text=text))

    def transition_to_next_session(self, session_type):
        if session_type == "Work":
            self.promodoro_cycle += 1
            self.update_label(self.state_label, "Break Time! Rest and recharge.")
            break_duration = int(self.break_entry.get()) * 60
            self.start_timer(break_duration, self.state_label, "Break")
        elif session_type == "Break":
            self.update_label(self.state_label, "Work Session! Time to focus.")
            work_duration = int(self.work_entry.get()) * 60
            self.start_timer(work_duration, self.state_label, "Work")
        self.update_label(self.pomo_cycle, f"Pomodoro Cycle: {self.promodoro_cycle}")

    def pause_resume_timer(self):
        self.paused = not self.paused
        self.update_label(self.state_label, "Paused" if self.paused else "Resumed")

    def reset_timer(self):
        self.running = False
        self.update_label(self.state_label, "Timer Reset.")
        self.promodoro_cycle = 0
        self.update_label(self.pomo_cycle, "Pomodoro Cycle: 0")

    def set_ui(self):
        # Header Label
        header = Label(self.root, text="Pomodoro Timer", font=("Helvetica", 24, "bold"), bg="#2C3E50", fg="#ECF0F1")
        header.pack(pady=20)

        # Input Frame
        input_frame = Frame(self.root, bg="#2C3E50")
        input_frame.pack(pady=10)

        Label(input_frame, text="Work Duration (min):", font=("Arial", 12), bg="#2C3E50", fg="#ECF0F1").grid(row=0, column=0, padx=10, pady=5)
        self.work_entry = Entry(input_frame, width=5, font=("Arial", 12))
        self.work_entry.grid(row=0, column=1, padx=10)
        self.work_entry.insert(0, "25")

        Label(input_frame, text="Break Duration (min):", font=("Arial", 12), bg="#2C3E50", fg="#ECF0F1").grid(row=1, column=0, padx=10, pady=5)
        self.break_entry = Entry(input_frame, width=5, font=("Arial", 12))
        self.break_entry.grid(row=1, column=1, padx=10)
        self.break_entry.insert(0, "5")

        # Timer State Label
        self.state_label = Label(self.root, text="Welcome to the Pomodoro Timer!", font=("Helvetica", 14), bg="#2C3E50", fg="#1ABC9C")
        self.state_label.pack(pady=20)

        # Pomodoro Cycle Label
        self.pomo_cycle = Label(self.root, text="Pomodoro Cycle: 0", font=("Helvetica", 12), bg="#2C3E50", fg="#ECF0F1")
        self.pomo_cycle.pack(pady=10)

        # Button Frame
        button_frame = Frame(self.root, bg="#2C3E50")
        button_frame.pack(pady=20)

        self.start_button = Button(button_frame, text="Start Timer", font=("Arial", 12), bg="#27AE60", fg="#ECF0F1", command=self.start_work_session)
        self.start_button.grid(row=0, column=0, padx=10)

        self.pause_button = Button(button_frame, text="Pause/Resume", font=("Arial", 12), bg="#F39C12", fg="#ECF0F1", command=self.pause_resume_timer)
        self.pause_button.grid(row=0, column=1, padx=10)

        self.reset_button = Button(button_frame, text="Reset Timer", font=("Arial", 12), bg="#C0392B", fg="#ECF0F1", command=self.reset_timer)
        self.reset_button.grid(row=0, column=2, padx=10)

    def start_work_session(self):
        self.update_label(self.state_label, "Work Session! Time to focus.")
        work_duration = int(self.work_entry.get()) * 60
        self.start_timer(work_duration, self.state_label, "Work")

if __name__ == "__main__":
    root = Tk()
    timer = Timer(root)
    root.mainloop()
