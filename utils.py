from enum import Enum
from supabase import create_client, Client

class CLIENT_STATUS(Enum):
    ONLINE = 1
    OFFLINE = 2
    BUSY = 3

class ClientManager:
    def __init__(self):
        super(ClientManager, self).__init__()

        self.clients = {}

        self.url = "https://wtmxnlnqpcunnykgvmgt.supabase.co"
        self.key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind0bXhubG5xcGN1bm55a2d2bWd0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA1MDkyNDIsImV4cCI6MjA3NjA4NTI0Mn0.xjRy5qyYsrXjMa8y1B0jZHTLlKXSvi_o8qcLEeJuBdU"

        self.client: Client = create_client(self.url, self.key)

    """
    auth_client
    authenticate client, return true if registered else return false
    """
    def auth_client(self, sid, phone_no: str, token: str):
        res = self.client.auth.get_user(token)
        if res.user.aud == "authenticated":
            self.clients[phone_no] = {'room': '', "sid": sid}
            return True
        else:
            return False
        
    """
    client_lookup

    check if client is connected to the master socket
    """
    def client_lookup(self, phone_no: str):
        try:
            if self.clients[phone_no]:
                if self.clients[phone_no]['room']:
                    return CLIENT_STATUS.BUSY
                else:
                    return CLIENT_STATUS.ONLINE
                
            else:
                return CLIENT_STATUS.OFFLINE

        except KeyError as not_found:
            return CLIENT_STATUS.OFFLINE
        

    def get_client_sid(self, phone_no: str):
        sid = self.clients[phone_no]['sid']
        return sid
        