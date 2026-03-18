from textual import on
from drive_interaction import DVD_DRIVE
from disk_interaction import DVD_DISK, CD_DISK
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static, Label
from textual.containers import HorizontalGroup, VerticalGroup
from textual.screen import Screen

def calibration(drive1,drive2,drive3):
    """Calibrates the drives
    Obtains the states of each drives
    After will open one drive at a time asking user which one it is
    """
    drive1.get_state()
    drive2.get_state()
    drive3.get_state()
    drive1.open_door()
    drive1.name = input("Which drive is opened? ")
    drive1.close_door()
    drive2.open_door()
    drive2.name = input("Which drive is opened? ")
    drive2.close_door()
    drive3.open_door()
    drive3.name = input("Which drive is opened? ")
    drive3.close_door()



class Disk_management(Screen):
    """Disk management screen
    This screen will be responsible for displaying the status of the disks and allowing the user to perform actions on them.
    """
    BINDINGS = [
        ("b", "back", "Back to main screen")
    ]
    def compose(self) -> ComposeResult:
        yield Label("Disk management screen")
        yield Button("Back", id="back")
    @on(Button.Pressed, "#back")
    def action_back(self):
        self.app.pop_screen()


class Drive_control(HorizontalGroup):
    BINDINGS = [
        ("r", "refresh", "Refresh drive state")
    ]
    def compose(self) -> ComposeResult:
        self.door_prefix="Drive Door Status: "
        self.disc_prefix="Drive Disc Status: "
        yield Label("Drive: "+self.name, id="drive_name")
        yield Button("Open Drive", id="open_drive")
        yield Button("Close Drive", id="close_drive")
        yield VerticalGroup(Label(self.door_prefix+str(drives[int(self.name)].door), id="drive_door_status"),Label(self.disc_prefix+str(drives[int(self.name)].disc), id="drive_disc_status"))
        yield Button("Manage Disk", id="manage_disk")
    @on(Button.Pressed, "#manage_disk")
    def manage_disk(self):
        self.app.push_screen(Disk_management())
    @on(Button.Pressed, "#open_drive")
    def open_drive(self):
        drives[int(self.name)].open_door()
        self.get_widget_by_id("drive_door_status").update(self.door_prefix+str(drives[int(self.name)].door))
    @on(Button.Pressed, "#close_drive")
    def close_drive(self):
        drives[int(self.name)].close_door()
        drives[int(self.name)].get_state()
        self.get_widget_by_id("drive_door_status").update(self.door_prefix+str(drives[int(self.name)].door))
        self.get_widget_by_id("drive_disc_status").update(self.disc_prefix+str(drives[int(self.name)].disc))
    def action_refresh(self):
        drives[int(self.name)].get_state()
        self.get_widget_by_id("drive_door_status").update(self.door_prefix+str(drives[int(self.name)].door))
        self.get_widget_by_id("drive_disc_status").update(self.disc_prefix+str(drives[int(self.name)].disc))

class dashboard(App):
    """Dashboard class
    This class will be responsible for the user interface of the program.
    It will display the status of the drives and the disks, and will allow the user to perform actions on them.
    """
    BINDINGS = [
        ("d", "dark_mode_toggle", "Toggle dark mode"),
        ("q", "quit", "Quit the app")
    ]
    def compose(self):
        """Composes the user interface
        """
        yield Header(show_clock=True)
        yield Footer()
        yield Drive_control(name="1")
        yield Drive_control(name="2")
        yield Drive_control(name="3")
    def action_dark_mode_toggle(self):
        self.theme = "textual-dark" if self.theme == "textual-light" else "textual-light"
    def action_quit(self):
        self.app.exit()

if __name__ == "__main__":
    drive1 = DVD_DRIVE()
    drive2 = DVD_DRIVE("/dev/sr1")
    drive3 = DVD_DRIVE("/dev/sr2")
    drive1.get_state()
    drive2.get_state()
    drive3.get_state()
    drives=["",drive1,drive2,drive3]
    # calibration(drive1,drive2,drive3)
    dashboard().run()
