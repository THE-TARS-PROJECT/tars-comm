from client_auth import Authenticator

auth = Authenticator()

res = auth.login_user("kumaraghav079@gmail.com", "HelloKumar@2025")
auth.edit_config("name", res[0])
auth.edit_config("ph_no", res[1])
auth.edit_config("access_token", res[2])
auth.edit_config("refresh_token", res[3])

