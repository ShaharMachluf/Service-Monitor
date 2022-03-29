# Services-Monitor
This program is about monitoring the services that are running on the computer. Both show all the services running and checking the diffrences in the services between two diffrent times.

## Stracture
The program is seperated to 3 main classes:
### GUI:
The main class of the program. The gui first opens a page with 2 buttons- monitor and manual (can't start the manual before starting the monitor).  
By pressing on monitor it first asks the user to enter the number of seconds he wants between the service checks and then creates a thread that operates the monitor with the given time.  
By pressing on manual it opens a window that lets the user input the times he wants to compare between and then creates a thread that operates the manual mode with the given times.
### Monitor Mode:
Check the current services that are running in the computer and writes it to the file "ServiceList.txt" (it does that every number of seconds as the user entered).  
It also check the difference between two following time stamps, write it to the file "Status_Log.txt" and show it to the user.  
### Manual Mode:
Check the diffrences between the two time stamps the user entered and show them to the user.  

## Libraries
- os- This module provides a portable way of using operating system dependent functionality. We used it to get the service lists from the operating system in Linux.
- subprocess- The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes. We used it to get the service lists from the operating system in Windows.
- platform- Access to underlying platform’s identifying data. We used it to know in what operating system the program is running on.
- datetime- For the time stamps for the files.
- tkinter- To present the gui.
- hashlib- to monitor the changes in the files.

## Defence from hackers
After writing to the file we check the files current hash code using the method hash_file. Before we change the file again we check the hash code of the file again to see if any changes was made in the meantime. If so it means that someone else 
modified the file so we show an error message that ket the user know it happend.

*the program runs in python 3.8
