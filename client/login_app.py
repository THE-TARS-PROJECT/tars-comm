from json import loads, dump
from PySide6.QtWidgets import QApplication, QDialog

from gui.login_ui import Ui_Dialog
from client_auth import Authenticator

class LoginApp(QDialog):
    def __init__(self):
        super(LoginApp, self).__init__()

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowTitle("User Login")

        self.auth = Authenticator()

        # connections
        self.ui.submitBtn.clicked.connect(self.on_submit)

    """
    config_client

    check default config values
    check if user is authenticated or not
    """
    def is_configured(self):
        try:
            with open(f"{self.config_path}/tars/comm/config.json", "r") as config_file:
                data = loads(config_file.read())
                if data['token'] != "":
                    self.config = data

        except FileNotFoundError:
            with open(f"{self.config_path}/tars/comm/config.json", "w") as config_file:
                dump({
                    "name": "",
                    "email": "",
                    "token": ""
                }, config_file)
                config_file.close()


    """
    on_submit

    login user when submit is clicked
    """
    def on_submit(self):
        res = self.auth.login_user(
            self.ui.emailInput.text(),
            self.ui.passwordInput.text()
        )
        if res != "":
            self.auth.edit_config("name", res[0])
            self.auth.edit_config("ph_no", res[1])
        else:
            print("login failed")


app = QApplication()
win = LoginApp()
win.show()
app.exec()
