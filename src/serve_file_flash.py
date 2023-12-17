from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/files/<filename>')
def serve_file(filename):
    return send_from_directory(os.environ['HOME'], 'sysd', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)   #  threading=True, even if enabled bydefault
