from client_auth import Authenticator

auth = Authenticator()


username = input("Enter your username: ")
password = input("Enter your password: ")

res = auth.login_user(str(username), str(password))
print(res)
auth.edit_config("name", res[0])
auth.edit_config("ph_no", res[1])
auth.edit_config("access_token", res[2])
auth.edit_config("refresh_token", res[3])

