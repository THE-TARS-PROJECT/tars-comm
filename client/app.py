from textual.app import App
from asyncio import create_task
from client_auth import Authenticator
from dbus_interface import exec_interface
from client_utils import AudioUtils, ContactsManager, ClientDBUS
from screens import DialerScreen, HomeScreen, AddContactDialog, LoginScreen

"""
main app
dont touch
"""
class App_(App):
    SCREENS = {
        "login": LoginScreen,
        "home": HomeScreen,
        "add_contact": AddContactDialog,
        'dialer': DialerScreen
    }

    CSS_PATH = "style.tcss"

    async def on_mount(self):
        self.auth = Authenticator()
        self.audio_helper = AudioUtils()
        self.contacts_manager = ContactsManager()

        self.dbus = ClientDBUS()

        await self.dbus.setup()

        self.shared_instances = {
            "audio_helper": self.audio_helper,
            "contacts_manager": self.contacts_manager,
            "auth": self.auth,
            "dbus_interface": self.dbus.get_interface()
        }
        self.screen.title = "TARS COMMUNICATION PROTOCOL"

        data = self.auth.config
        if data["ph_no"] == "":
            self.push_screen("login")
            self.screen.title = "PROTOCOL AUTHENTICATION"

        else:
            self.push_screen("home")
            self.screen.title = "TARS COMMUNICATION PROTOCOL"

if __name__ == "__main__":
    App_().run()
