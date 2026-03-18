import subprocess
import fcntl
import os

class DVD_DRIVE():
    """Optical Drive class
    Gathers and stores data related to optical drives.
    """
    def __init__(self,path="/dev/sr0"):
        """
        Args:
            path (str, optional): path of the drive. Defaults to "/dev/sr0".
        """
        self.path = path
        self.door = bool
        self.has_disc = bool
        self.status = None
        self.name = str
        self.disk = None
        self.initialized = False
    def get_state(self):
        """detect_tray reads status of the CDROM_DRIVE.
        Statuses:
        1 = no disk in tray
        2 = tray open
        3 = reading tray
        4 = disk in tray
        """
        fd = os.open(self.path, os.O_RDONLY | os.O_NONBLOCK)
        rv = fcntl.ioctl(fd, 0x5326)
        os.close(fd)
        print(rv)
        if rv == 1:
            self.door = False
            self.has_disc = False
        elif rv == 2:
            self.door = True
            self.has_disc = False
        elif rv == 3:
            self.door = False
            self.has_disc = True
        elif rv == 4:
            self.door = False
            self.has_disc = True
        print(self.door,self.has_disc)
        return rv
    def open_door(self):
        """Opens/Eject the drive
        """
        subprocess.run(["eject",self.path])
        self.door = True
    def close_door(self):
        """Closes the drive
        """
        subprocess.run(["eject",self.path,"-t"])
        self.door = False

