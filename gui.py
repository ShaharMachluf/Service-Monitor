import tkinter.simpledialog
from tkinter import *
from tkinter import ttk
import tkinter as tk
from monitor import Monitor
from manual_mode import Manual
from threading import Thread
import tkinter.scrolledtext


# this is the main class that activate the GUI
class Gui:
    def __init__(self):
        self.root = Tk()
        self.root.title("monitor")
        self.root.geometry("850x850")
        self.root.resizable(1, 1)
        self.frm = ttk.Frame(self.root, padding=10)
        self.frm.grid()
        self.flag = 1
        self.my_time = 0
        self.time1 = ""
        self.time2 = ""
        ttk.Button(self.frm, text="monitor mode", command=self.monitor_mode).grid(column=1, row=0)
        ttk.Button(self.frm, text="manual_mode", command=self.enter_time).grid(column=1, row=3)
        self.txt_area = tkinter.scrolledtext.ScrolledText(self.frm, wrap=tk.WORD, width=70, heigh=9, font=("ariel", 11))
        self.txt_area.grid(column=20, pady=10, padx=10)
        self.txt_area.focus()
        ttk.Label(self.root, text="manual mode:", font=("ariel", 12), foreground="black").grid(column=0, row=0)
        self.txt_area2 = tkinter.scrolledtext.ScrolledText(self.frm, wrap=tk.WORD, width=70, heigh=10,
                                                           font=("ariel", 11))
        self.txt_area2.grid(column=20, pady=30, padx=10)
        self.txt_area2.focus()
        self.root.mainloop()

    # this function activate the monitor mode
    def monitor_mode(self):
        self.my_time = tkinter.simpledialog.askfloat("set time", "please enter period of time in seconds:",
                                                     parent=self.root)
        monitor = Monitor(self.my_time)
        Thread(target=monitor.monitoring).start()
        Thread(target=self.write_changes, args=[monitor]).start()
        self.root.protocol("WM_DELETE_WINDOW", lambda: [monitor.exit_monitor(), self.exit_program()])

    # this function exit from the program
    def exit_program(self):
        self.root.destroy()
        exit(0)

    # this function write on the screen
    def write_changes(self, monitor):
        prev_line = ""
        while True:
            if monitor.current_change != prev_line:
                prev_line = monitor.current_change
                self.txt_area.insert('end', monitor.current_change)
                self.txt_area.yview('end')

    # this function activate the manual mode
    def manual_mode(self, year, year2, month, month2, day, day2, hour, hour2, minute, minute2, sec, sec2):
        self.time1 += "$" + year.get() + "-"
        mon_str = "0" + month.get() if (len(month.get()) == 1) else month.get()
        self.time1 += mon_str + "-"
        day_str = "0" + day.get() if (len(day.get()) == 1) else day.get()
        self.time1 += day_str + " "
        hour_str = "0" + hour.get() if (len(hour.get()) == 1) else hour.get()
        self.time1 += hour_str + ":"
        min_str = "0" + minute.get() if (len(minute.get()) == 1) else minute.get()
        self.time1 += min_str + ":"
        sec_str = "0" + sec.get() if (len(sec.get()) == 1) else sec.get()
        self.time1 += sec_str
        self.time2 += "$" + year2.get() + "-"
        mon_str2 = "0" + month2.get() if (len(month2.get()) == 1) else month2.get()
        self.time2 += mon_str2 + "-"
        day_str2 = "0" + day2.get() if (len(day2.get()) == 1) else day2.get()
        self.time2 += day_str2 + " "
        hour_str2 = "0" + hour2.get() if (len(hour2.get()) == 1) else hour2.get()
        self.time2 += hour_str2 + ":"
        min_str2 = "0" + minute2.get() if (len(minute2.get()) == 1) else minute2.get()
        self.time2 += min_str2 + ":"
        sec_str2 = "0" + sec2.get() if (len(sec2.get()) == 1) else sec2.get()
        self.time2 += sec_str2
        print(self.time1)
        print(self.time2)
        manual = Manual(self.time1, self.time2)
        # results = []
        Thread(target=manual.monitoring).start()
        while True:
            # print(self.results)
            if len(manual.results) >= 1:
                self.txt_area2.insert('end', str(manual.results))
                self.txt_area2.yview('end')
                break

    # this function get from the user 2 dates to the manual mode
    def enter_time(self):
        man_root = Tk()
        man_root.title("set date")
        man_root.geometry("500x500")
        man_frm = ttk.Frame(man_root, padding=10)
        man_frm.grid()
        ttk.Label(man_root, text="please enter the first time:").grid(column=1, row=0)
        ttk.Label(man_root, text="year:").grid(column=1, row=8)
        years = [i for i in range(2010, 2031)]
        year = StringVar(man_root)
        w = OptionMenu(man_root, year, *years).grid(column=1, row=12)
        ttk.Label(man_root, text="month:").grid(column=4, row=8)
        months = [i for i in range(1, 13)]
        month = StringVar(man_root)
        w = OptionMenu(man_root, month, *months).grid(column=4, row=12)
        ttk.Label(man_root, text="day:").grid(column=7, row=8)
        days = [i for i in range(1, 32)]
        day = StringVar(man_root)
        w = OptionMenu(man_root, day, *days).grid(column=7, row=12)
        ttk.Label(man_root, text="hour:").grid(column=1, row=18)
        hours = [i for i in range(0, 24)]
        hour = StringVar(man_root)
        w = OptionMenu(man_root, hour, *hours).grid(column=1, row=22)
        ttk.Label(man_root, text="minuet:").grid(column=4, row=18)
        minutes = [i for i in range(0, 60)]
        minute = StringVar(man_root)
        w = OptionMenu(man_root, minute, *minutes).grid(column=4, row=22)
        ttk.Label(man_root, text="second:").grid(column=7, row=18)
        secondes = [i for i in range(0, 60)]
        sec = StringVar(man_root)
        w = OptionMenu(man_root, sec, *secondes).grid(column=7, row=22)
        ttk.Label(man_root, text="please enter the second time:").grid(column=1, row=30)
        ttk.Label(man_root, text="year:").grid(column=1, row=38)
        year2 = StringVar(man_root)
        w = OptionMenu(man_root, year2, *years).grid(column=1, row=42)
        ttk.Label(man_root, text="month:").grid(column=4, row=38)
        month2 = StringVar(man_root)
        w = OptionMenu(man_root, month2, *months).grid(column=4, row=42)
        ttk.Label(man_root, text="day:").grid(column=7, row=38)
        day2 = StringVar(man_root)
        w = OptionMenu(man_root, day2, *days).grid(column=7, row=42)
        ttk.Label(man_root, text="hour:").grid(column=1, row=48)
        hour2 = StringVar(man_root)
        w = OptionMenu(man_root, hour2, *hours).grid(column=1, row=52)
        ttk.Label(man_root, text="minuet:").grid(column=4, row=48)
        minute2 = StringVar(man_root)
        w = OptionMenu(man_root, minute2, *minutes).grid(column=4, row=52)
        ttk.Label(man_root, text="second:").grid(column=7, row=48)
        sec2 = StringVar(man_root)
        w = OptionMenu(man_root, sec2, *secondes).grid(column=7, row=52)
        ttk.Button(man_frm, text="OK", command=lambda: [man_root.destroy(),
                                                        self.manual_mode(year, year2, month, month2, day, day2, hour,
                                                                         hour2, minute, minute2, sec, sec2)]).grid(
            column=15, row=60)
        man_root.mainloop()


if __name__ == '__main__':
    Gui()
