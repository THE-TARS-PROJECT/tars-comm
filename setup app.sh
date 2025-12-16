git clone https://github.com/THE-TARS-PROJECT/tars-comm.git
cd tars-comm

echo "Creating virtual environment..."
apt install python3-virtualenv
virtualenv env
source env/bin/activate

apt install python3-pyaudio
pip3 install -r requirements.txt
