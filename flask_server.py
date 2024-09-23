from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/')
def serve_chat():
    return send_from_directory('', 'index.html')

if __name__ == "__main__":
    app.run(host='192.168.1.83', port=5000)
