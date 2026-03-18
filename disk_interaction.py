import time
import json
import subprocess
from drive_interaction import DVD_DRIVE
class DVD_DISK():
    """Class for a DVD disk.
    """
    #- to obtain info, use lsdvd
    def __init__(self,drive: DVD_DRIVE):
        """
        Args:
            drive (DVD_DRIVE): The optical drive instance
        """
        self.title = None
        self.status = None
        self.drive = drive
        self.additional_info = None
    def get_metadata(self):
        """Gathers DVD metadata using lsdvd.
        """
        self.status = "gathering metadata"
        self.drive.status = "gathering metadata"
        data={
            "device" : str,
            "title" : str,
            "vmg_id" : str,
            "provider_id" : str,
            "track" : [
                {
                "ix" : int,
                "length" : float,
                "vts_id" : str
                }
            ],
            "dvddiscid" : str,
            "longest_track" : int
        }
        result = subprocess.run(["lsdvd","-Oj",self.drive.path], capture_output=True, text=True)
        data = json.loads(result.stdout)
        self.title = data["title"]
        self.additional_info = data
        self.status = "metadata gathered"
        self.drive.status = None



class CD_DISK():
    """Class for a CD disk.
    """
    #- to obtain info, use cd-info
    def __init__(self,drive):
        self.title = None
        self.status = None
        self.drive = drive
        self.additional_info = {"tracks":[dir,dir,...],"performer":str,}
    def get_metadata(self):
        result = subprocess.run(["cd-info",self.drive], capture_output=True, text=True)
        result= result.split("CD-TEXT")
        print("hello world")


x = CD_DISK("/dev/sr2")
x.get_metadata()