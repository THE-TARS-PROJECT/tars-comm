from os import path, getenv
from json import loads, dump
from socketio.async_client import AsyncClient

from client_auth import Authenticator


class ClientSocket(AsyncClient):
    def __init__(self):
        super(ClientSocket, self).__init__()

        self.config_path = getenv("HOME")
        self.auth = Authenticator()

        self.config = None

        self.main()
        
    """
    main 

    socketio loop, take user commands - temporary, until gui is developed
    """
    def main(self):
        while True:
            cmd = str(input("Enter command: "))

            # login
            if cmd.lower() == "login":
                email = str(input("Enter your email: "))
                pass_ = str(input("Enter your password: "))
                auth_res = self.auth.login_user(email, pass_)
                if auth_res != "":
                    self.edit_config('token', auth_res)
                else:
                    print('login failed')


sock = ClientSocket()
