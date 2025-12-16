echo "Starting server...."
uvicorn master_socket:app --reload --port 8000 &&

echo "Starting ngrok. Please make sure to change client/config.env and update URL with ngrok url below"
ngrok http 8000

