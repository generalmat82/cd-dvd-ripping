import subprocess
import json
from drive_interaction import DVD_DRIVE
drive1 = DVD_DRIVE()
drive2 = DVD_DRIVE("/dev/sr1")
drive3 = DVD_DRIVE("/dev/sr2")

def calibration():
    """Calibrates the drives
    Obtains the states of each drives
    After will open one drive at a time asking user which one it is
    """
    positions=[]
    drive1.get_state()
    drive2.get_state()
    drive3.get_state()
    drive1.open_door()
    positions.append(input("Which drive is open? (1,2,3)"))
    drive1.close_door()
    drive2.open_door()
    positions.append(input("Which drive is open? (1,2,3)"))
    drive2.close_door()
    drive3.open_door()
    positions.append(input("Which drive is open? (1,2,3)"))
    drive3.close_door()
    return positions
input("Press enter to calibrate drives")
positions = calibration()

result = subprocess.run(["lsdvd","-Oj","/dev/sr0"], capture_output=True, text=True)
data = json.loads(result.stdout)

