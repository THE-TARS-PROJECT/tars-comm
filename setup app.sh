git clone https://github.com/THE-TARS-PROJECT/tars-comm.git
cd tars-comm

echo "Creating virtual environment..."
apt install python3-virtualenv
virtualenv env
source env/bin/activate

apt install python3-pyaudio
pip3 install -r requirements.txt

uvicorn master_socket:app --reload --port 8000 &&
ngrok http 8000

