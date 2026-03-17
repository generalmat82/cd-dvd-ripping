import time
import json
import subprocess
class DVD_DISK():
    #- to obtain info, use lsdvd
    def __init__(self,drive):
        self.title = None
        self.status = None
        self.drive = drive
        self.additional_info = None

class CD_DISK():
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