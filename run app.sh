source env/bin/activate

echo "If DBUS Interface fails to start, run client/force_manual_login.py"

python3 client/dbus_interface.py &&
python3 client/app.py