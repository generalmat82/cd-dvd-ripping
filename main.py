from textual import on
from drive_interaction import DVD_DRIVE
from disk_interaction import DVD_DISK, CD_DISK
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static, Label
from textual.containers import HorizontalGroup

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

class Drive_control(HorizontalGroup):
    def compose(self) -> ComposeResult:
        self.prefix="Drive Door Status: "
        yield Label("Drive: "+self.name, id="drive_name")
        yield Button("Open Drive", id="open_drive")
        yield Button("Close Drive", id="close_drive")
        yield Label(self.prefix+str(drives[int(self.name)].door), id="drive_status")
    @on(Button.Pressed, "#open_drive")
    def open_drive(self):
        drives[int(self.name)].open_door()
        self.get_widget_by_id("drive_status").update(self.prefix+str(drives[int(self.name)].door))
    @on(Button.Pressed, "#close_drive")
    def close_drive(self):
        drives[int(self.name)].close_door()
        self.get_widget_by_id("drive_status").update(self.prefix+str(drives[int(self.name)].door))

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
