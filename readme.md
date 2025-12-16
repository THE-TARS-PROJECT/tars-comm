# TARS COMMUNICATION PROTOCOL

**This project is under development, and is it is not at all recommended to put any sensitive info.**

Terminal is cool, like super cool. What if you make calls from your terminal giving you a sci-fi feel. Isn't that crazy. Yess, it is.

TARS COMMUNICATION PROTOCAL is **terminal based VoIP app**. It works like just another VoIP client but in your terminal.

![ss](https://raw.githubusercontent.com/THE-TARS-PROJECT/tars-comm/refs/heads/main/screenshots/Screenshot%20from%202025-11-14%2012-17-17.png)

![ss(https://raw.githubusercontent.com/THE-TARS-PROJECT/tars-comm/refs/heads/main/screenshots/Screenshot%20from%202025-11-14%2012-17-22.png)

## Features
 - Terminal based sci-fi aesthetics
 - Save contacts
 - Call Logs
 - Audio input / output visualisation

 - Lightweight, runs in the background (no need to keep your terminal open)
 - Rich shortcuts, perfect for terminal lovers.

## Installation
To install tars-comm project.

 - Download the installation script.
 ```bash
 wget https://raw.githubusercontent.com/THE-TARS-PROJECT/tars-comm/refs/heads/main/setup%20app.sh
 ```

 - Give permission and run
 ```bash
 chmod +x ./setup\ app.sh
 bash ./setup\ app.sh
 ```

 Now you are in the project root directory. Run the app and please pay close attention to print messages.

 - Run the server
 ```bash
 chmod +x ./run\ server.sh
 bash ./run\ server.sh
 ```

 **NOTE: You will see a like url https://xyz123.ngrok.free.app copy this url and paste it in *client/config.env (URL Variable)***

 Now open another terminal in the project root folder.
 ```bash
 chmod +x ./run\ app.sh
 bash ./run\ app.sh
 ```

 **Don't forget to make an account: Go to http://127.0.0.1:8000/auth/signup and make your account.**

## Keymap
 - `a`:  Add a new contact
 - `d`: Delete contact
 - `c`: Open dialer
 - `up/down arrow key and TAB` : Navigate
 - `Ctrl + Q`: Exit

## Troubleshooting
You might encounter the following issues:

 - errors related to 'new token' or "Revalidating JWT":

   To fix run 
   ```bash
   python3 client/force_manual_login.py
   ```

 - .service file not provided:
   
   This means that DBUS service was not found. To start it manually, go to project root and activate the Python virtual environment and run.

   ```bash
   python3 client/dbus_interface.py
   ```

 - NGROK account error
 You will need to setup your ngrok account. Check this [page](https://ngrok.com/docs/getting-started#2-connect-your-account).

 - Address already in use

   For initial ease of use, the server runs on port 8000, other services might be running on the same port. Terminate other process and run the server again.

## Author
Raghav Kumar (@Raghav67816)
