# import sys
# import fcntl
# import struct
import os
import socket
import subprocess


# hostname + ram_size + cpu_name + disk_serial (first disk)
def hwFingerprint():

    mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
    host = socket.gethostname()

    # cpu_name
    command = "cat /proc/cpuinfo"
    cpu_info = subprocess.check_output(command, shell=True).strip()

    for line in cpu_info.split("\n"):
        if "model name" in line:
            cpu_raw =  line.strip("model name	:")
            cpu_name = cpu_raw.replace(' ', '')
            break

    command = ' /sbin/udevadm info --query=property --name=sda | grep -i "ID_SERIAL_SHORT" | cut -d \'=\' -f 2'
    disk_serial = subprocess.check_output(command, shell=True).strip()

    return host + str(mem_bytes) + cpu_name + disk_serial
