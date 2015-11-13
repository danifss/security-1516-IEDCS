import sys
import fcntl
import struct
import os
import socket

# adapted from http://stackoverflow.com/questions/4193514/how-to-get-hard-disk-serial-number-using-python


def hwFingerprint():

    """
    if os.geteuid() > 0:
        # print("ERROR: Must be root to use")
        return None

    # us, gets always from /dev/sda
    with open("/dev/sda", "rb") as fd:
        # tediously derived from the monster struct defined in <hdreg.h>
        # see comment at end of file to verify
        hd_driveid_format_str = "@ 10H 20s 3H 8s 40s 2B H 2B H 4B 6H 2B I 36H I Q 152H"
        # Also from <hdreg.h>
        HDIO_GET_IDENTITY = 0x030d
        # How big a buffer do we need?
        sizeof_hd_driveid = struct.calcsize(hd_driveid_format_str)

        # ensure our format string is the correct size
        # 512 is extracted using sizeof(struct hd_id) in the c code
        assert sizeof_hd_driveid == 512

        # Call native function
        buf = fcntl.ioctl(fd, HDIO_GET_IDENTITY, " " * sizeof_hd_driveid)
        fields = struct.unpack(hd_driveid_format_str, buf)
        #model = fields[15].strip()
        serial_no = fields[10].strip()
    """
    mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
    host = socket.gethostname()

    #return serial_no+str(host)+str(mem_bytes)
    return str(host)+str(mem_bytes)
