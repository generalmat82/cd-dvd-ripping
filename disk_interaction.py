import time
import json
import subprocess
import yaml
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
        self.metadata = False
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
        self.metadata = True



class CD_DISK():
    """Class for a CD disk.
    """
    #- to obtain info, use cd-info
    def __init__(self,drive: DVD_DRIVE):
        """
        Args:
            drive (DVD_DRIVE): The optical drive instance
        """
        self.title = None
        self.status = None
        self.drive = drive
        self.additional_info = None
        self.metadata = False
    def sanitize_cdtext(text, replacement=" -"):
        """
        Replace ':' inside values (not keys) with a safe separator.
        Disclamer: This was made using chatGPT cus I couldn't figure it out myself.
        
        Args:
            text (str): raw CD-TEXT string
            replacement (str): what to replace inner colons with
        
        Returns:
            str: sanitized string
        """
        def fix_line(line):
            # Only process lines that contain a key:value pair
            if ":" in line:
                key, value = line.split(":", 1)  # split only on FIRST colon
                # Replace any additional colons in the value
                value = value.replace(":", replacement)
                return f"{key}:{value}"
            return line
        return "\n".join(fix_line(line) for line in text.splitlines())
    def get_metadata(self):
        self.status = "gathering metadata"
        self.drive.status = "gathering metadata"
        result = subprocess.run(["cd-info",self.drive.path], capture_output=True, text=True)
        result = result.split("CD-TEXT ",1)
        self.num_tracks = int(result[0].splitlines()[44].split("(")[1].split(" - ")[1][:-1])
        result.pop(0)
        result[0] = result[0].replace("\t","    ")
        sanitized = self.sanitize_cdtext(result[0])
        metadata = yaml.load(sanitized, Loader=yaml.Loader)
        self.title = metadata["for Disc"]["TITLE"]
        self.additional_info = metadata
        self.status = "metadata gathered"
        self.drive.status = None
        self.metadata = True
        print("hello world")
    def rip(self):
        """Rips the CD
        While the CD is being ripped, the program will make a file alongside the ISO
        This file will have the metadata of the CD in JSON format.
        After, the user will be able to return to menu and perform other actions while the CD is being ripped.
        """

