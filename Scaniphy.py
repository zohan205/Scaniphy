#!/usr/bin/env python
import socket
import sys
import time
import threading
from __version__ import VERSION

lt = []
usage = "Usage: python Scaniphy.py TARGET START_PORT[option] END_PORT[option]"

def banner(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)
print(banner(0,255,0,"""
   _____                 _       _
  / ____|               (_)     | |
 | (___   ___ __ _ _ __  _ _ __ | |__  _   _
  \___ \ / __/ _` | '_ \| | '_ \| '_ \| | | |
  ____) | (_| (_| | | | | | |_) | | | | |_| |
 |_____/ \___\__,_|_| |_|_| .__/|_| |_|\__, |
                          | |           __/ |
                          |_|          |___/

📡A simple TCP network scanning tool.
#########################################################
# Project: https://github.com/zohan205/Scaniphy         #
# Creator: Zohan_404                                    #
# Version: {}                                        #
#########################################################
""").format(VERSION))

start_time = time.time()

if(len(sys.argv) < 2):
    print(usage)
    sys.exit()

try:
    target = socket.gethostbyname(sys.argv[1])
except socket.gaierror:
    print("Name resoulution error")
    sys.exit()

if len(sys.argv) ==2:
    start_port,end_port = 0,1024
    print("Default scanning",end="")
else:
    start_port = int(sys.argv[2])
    end_port = int(sys.argv[3])
    print("Scanning",end="")

total_ports = end_port-start_port+1
print(" {} ports on {}".format(total_ports,target))

def scan_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    conn = s.connect_ex((target, port))
    if(not conn):
        print("[+] Port {} is OPEN".format(port))
        lt.append(1)
    s.close()

for port in range(start_port,end_port+1):
    thread = threading.Thread(target = scan_port, args = (port,))
    thread.start()

thread.join()
end_time = time.time()
open = len(lt)
print("{} ports open, {} ports closed.".format(open,total_ports-open))
print("Time elapsed: {}s".format(round(end_time-start_time,2)))
