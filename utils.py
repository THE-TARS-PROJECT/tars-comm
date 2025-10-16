from supabase import create_client, Client

class ClientManager:
    def __init__(self):
        super(ClientManager, self).__init__()

        self.clients = []

        self.url = "https://wtmxnlnqpcunnykgvmgt.supabase.co"
        self.key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind0bXhubG5xcGN1bm55a2d2bWd0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA1MDkyNDIsImV4cCI6MjA3NjA4NTI0Mn0.xjRy5qyYsrXjMa8y1B0jZHTLlKXSvi_o8qcLEeJuBdU"

        self.client: Client = create_client(self.url, self.key)

    """
    auth_client
    authenticate client, return true if registered else return false
    """
    def auth_client(self, client_id: str, token: str):
        res = self.client.auth.get_user(token)
        if res.user.aud == "authenticated":
            self.clients.append(client_id)
            return True
        else:
            return False
        