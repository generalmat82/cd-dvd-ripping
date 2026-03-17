import subprocess
import fcntl
import os

class DVD_DRIVE():
    def __init__(self,drive="/dev/sr0"):
        self.drive = drive
        self.door = True
        self.disc = False
    def get_state(self):
        """detect_tray reads status of the CDROM_DRIVE.
        Statuses:
        1 = no disk in tray
        2 = tray open
        3 = reading tray
        4 = disk in tray
        """
        fd = os.open(self.drive, os.O_RDONLY | os.O_NONBLOCK)
        rv = fcntl.ioctl(fd, 0x5326)
        os.close(fd)
        print(rv)
        if rv == 1:
            self.door = False
            self.disc = False
        elif rv == 2:
            self.door = True
            self.disc = False
        elif rv == 3:
            self.door = False
            self.disc = True
        elif rv == 4:
            self.door = False
            self.disc = True
        print(self.door,self.disc)
        return rv
    def open_door(self):
        subprocess.run(["eject",self.drive])
    def close_door(self):
        subprocess.run(["eject",self.drive,"-t"])

