import hashlib
import platform
import os
import subprocess
import time
from datetime import datetime
import tkinter
from tkinter import messagebox


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
            prev_hash = ""
            prev_hash2 = ""
            while True:
                curr_hash = self.hash_file(self.serviceList)
                curr_hash2 = self.hash_file(self.status_log)
                if prev_hash != "" and prev_hash != curr_hash:
                    messagebox.showerror("error", self.serviceList + " was changed by unknown user")
                if prev_hash2 != "" and prev_hash2 != curr_hash2:
                    messagebox.showerror("error", self.status_log + " file was changed by unknown user")
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
                    except UnicodeEncodeError:
                        continue
                file.write("\n~\n")
                prev_hash = self.hash_file(self.serviceList)
                prev_hash2 = self.hash_file(self.status_log)
                time.sleep(float(self.my_time))

    # this function check if something changes
    def compare(self, curr, prev, curr_time):
        prev_list = prev.split('\n')  # split the process list by lines
        curr_list = curr.split('\n')
        prev_id_list = [1, 1]
        curr_id_list = [1, 1]
        if self.system == "Linux":
            for i in range(2, len(prev_list)):  # get process by ID
                try:
                    prev_id_list.append(prev_list[i].split(" ")[2])
                except IndexError:
                    continue
                if prev_list[i][0] != " ":
                    break
            for i in range(2, len(curr_list)):
                try:
                    curr_id_list.append(curr_list[i].split(" ")[2])  # get process by ID
                except IndexError:
                    continue
                if curr_list[i][0] != " ":
                    break
            curr_list = curr_id_list
            prev_list = prev_id_list
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

    # this function return the hash of the file
    def hash_file(self, filename):
        # make a hash object
        h = hashlib.sha1()

        # open file for reading in binary mode
        with open(filename, 'rb') as file:
            # loop till the end of the file
            chunk = 0
            while chunk != b'':
                # read only 1024 bytes at a time
                chunk = file.read(1024)
                h.update(chunk)

        # return the hex representation of digest
        return h.hexdigest()
