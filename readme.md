# TARS COMMUNICATION PROTOCOL

Terminal is cool, like super cool. What if you make calls from your terminal giving you a sci-fi feel. Isn't that crazy. Yess, it is.

TARS COMMUNICATION PROTOCAL is **terminal based VoIP app**. It works like just another VoIP client but in your terminal.

![ss](https://raw.githubusercontent.com/THE-TARS-PROJECT/tars-comm/refs/heads/main/screenshots/Screenshot%20from%202025-11-14%2012-17-17.png)

![ss](https://raw.githubusercontent.com/THE-TARS-PROJECT/tars-comm/refs/heads/main/screenshots/Screenshot%20from%202025-11-14%2012-17-22.png)

## Features
 - Terminal based sci-fi aesthetics
 - Save contacts
 - Call Logs
 - Audio input / output visualisation

 - Lightweight, runs in the background (no need to keep your terminal open)
 - Rich shortcuts, perfect for terminal lovers.

## Installation
To install tars-comm project.

- Download and unpack the latest release from Releases section.

- Install required packages
```bash
pip3 install textual requests sounddevice numpy
sudo apt install python3-pyaudio
pip3 install PyAudio
```

- Run the app
```
cd client/
python3 app.py
```

I will post a setup.sh script soon. This script will install tars-comm as linux service and it will simplify installation process.

## HOW TO:
 - make an account ?

    Go to https://tars-comm.onrender.com/auth/signup , make an account, login to verify and you will redirected to a dashboard after that just put your email and password in the terminal app.

    **NOTE: APIs hosted on Render go inactive after inactivity**

 - add contact ?

    Use tab to navigate between widget. Once, the Contact List widget is highlighted press **"a"** to add contact and put the details. This can be anything for now

 - delete contact ?
    
    Simply press **"d"** on the highlight contact item.

 - call my friend ?

    haha!! wait for sometime, my nest request is not approved yet. But still press **"c"** and enter the number and press **enter**.

## Author
Raghav Kumar (@Raghav67816)
