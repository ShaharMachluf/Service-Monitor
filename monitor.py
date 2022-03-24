import platform
import os
import subprocess
import time
from datetime import datetime


class Monitor:
    def __init__(self, my_time):
        self.my_time = my_time
        self.system = platform.system()
        self.serviceList = "serviceList.txt"
        self.status_log = "Status_Log.txt"
        self.flag = 1
        self.current_change = ""

    # this function monitor the active processes and write them to file
    def monitoring(self):
        curr_proc = ""
        try:  # check if this files already exist
            f = open(self.serviceList)
            f.close()
            os.remove(self.serviceList)
        except IOError:
            pass
        try:
            f = open(self.status_log)
            f.close()
            os.remove(self.status_log)
        except IOError:
            pass
        with open(self.serviceList, "a") as file:
            file.write(str(self.my_time) + "\n")
            while True:
                if self.flag == 0:
                    return
                curr_time = "\n$" + str(datetime.now()) + "\n"
                prev_proc = curr_proc
                if self.system == "Windows":
                    try:
                        curr_proc = subprocess.check_output("net start", shell=True, encoding="unicode_escape")
                    except AttributeError:
                        pass
                elif self.system == "Linux":
                    curr_proc = os.popen("systemctl list-units --type=service").read()
                self.compare(curr_proc, prev_proc, curr_time)
                file.write(curr_time)
                curr_list = curr_proc.split("\n")
                for i in range(len(curr_list) - 3):
                    try:
                        file.write(curr_list[i] + "\n")
                        print("##\n" + curr_list[i])
                    except UnicodeEncodeError:
                        continue
                file.write("\n~\n")
                time.sleep(float(self.my_time))

    # this function check if something changes
    def compare(self, curr, prev, curr_time):
        prev_list = prev.split('\n')  # split the process list by lines
        curr_list = curr.split('\n')
        prev_id_list = [1, 1, 1, 1]
        curr_id_list = [1, 1, 1, 1]
        if self.system == "Linux":
            for i in range(4, len(prev_list)):  # get process by ID
                prev_id_list.append(prev_list[i][8:16])
            for i in range(4, len(curr_list)):
                curr_id_list.append(curr_list[i][8:16])  # get process by ID
        with open(self.status_log, "a") as file:  # write the differences between the files
            file.write('\n' + curr_time + '\n')
            self.current_change = '\n' + curr_time + '\n'
            print('\n' + curr_time + '\n')
            for i in range(len(prev_list) - 3):
                if prev_list[i] not in curr_list:
                    try:
                        file.write("stopped:" + '\t' + prev_list[i] + '\n')
                        self.current_change = "stopped:" + '\t' + prev_list[i] + '\n'
                        print("stopped:" + '\t' + prev_list[i] + '\n')
                    except UnicodeEncodeError:
                        continue
            for i in range(len(curr_list) - 3):
                if curr_list[i] not in prev_list:
                    try:
                        file.write("started:" + '\t' + curr_list[i] + '\n')
                        self.current_change = "started:" + '\t' + curr_list[i] + '\n'
                        print("started:" + '\t' + curr_list[i] + '\n')
                    except UnicodeEncodeError:
                        continue

    def exit_monitor(self):
        self.flag = 0
