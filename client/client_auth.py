from requests import post
from json import loads, dump
from os import getenv, makedirs, path

class Authenticator:
    def __init__(self):
        
        self.endpoint = "https://504904ef718e.ngrok-free.app"
        self.home = getenv('HOME')
        self.config = self.read_config()

    """
    read_config

    read user config and create file if not exists
    """
    def read_config(self):
        try:
            with open(f"{self.home}/tars/comm/config.json", "r") as config_file:
                data = loads(config_file.read())
                return data

        except FileNotFoundError:
            print("cannot found file, making one")
            makedirs(path.dirname(f"{self.home}/tars/comm/config.json"), exist_ok=True)
            with open(f"{self.home}/tars/comm/config.json", "w") as config_file:
                data = {
                    "ph_no": "",
                    "name": "",
                    "access_token": "",
                    "refresh_token": ""
                }
                dump(data, config_file)
                config_file.close()
                return data
        

    """
    login_user
    
    login user with email and password
    returns token
    """
    def login_user(self, email: str, password: str):
        req = post(f"{self.endpoint}/auth/login_client", params={
            "email": email,
            "password": password
        })
        if req.status_code == 200 and req.json()['msg'] == "success":
            res = req.json()
            return res["name"], res["ph_no"], res["access_token"], res['refresh_token']
            
        else:
            print(req.json()['msg'])
        
    """
    login_with_token
    """
    def login_with_token(self):
        req = post(f"{self.endpoint}/auth/verify_jwt", params={
            "jwt": self.config['access_token'],
            "refresh_token": self.config['refresh_token']            
        })
        if req.ok:
            self.edit_config("access_token", req.json()['new_token'])
        
    """
    logout_user
    logout user from client
    """
    def logout_user(self, config: dict):
        for key in config.keys():
            config[key] = ""


    """
    edit_config
    edit config params
    """
    def edit_config(self, key: str, value: str):
        try:
            self.config[key] = value
            with open(f"{self.home}/tars/comm/config.json", "w") as config_file:
                dump(self.config, config_file)
                config_file.close()
                
        except KeyError:
            print(f"invalid param {key}")
            return
