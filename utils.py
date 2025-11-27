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

    def auth_client(self, sid: str, phone_no: str, token: str):
        res = self.client.auth.get_user(token)
        if res.user.aud == "authenticated":
            self.clients[sid] = {
                "phone_no": phone_no,
                "room": ""
            }
            return True
        else:
            return False

    """
    client_lookup

    check if client is connected to the master socket
    """

    def client_lookup(self, phone_no: str):
        sid = self.get_sid_by_phone_no(phone_no)
        if not self.clients[sid]:
            return CLIENT_STATUS.OFFLINE
        elif self.clients[sid]['room'] == "":
            return CLIENT_STATUS.ONLINE
        else:
            return CLIENT_STATUS.BUSY

    def get_sid_by_phone_no(self, phone_no: str):
        for sid in self.clients:
            if self.clients[sid]['phone_no'] == phone_no:
                return sid

    def update_room(self, sid: str, room_id: str):
        self.clients[sid]['room'] = room_id
    
    def remove_client(self, sid: str):
        self.clients.pop(sid)
