from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)

@app.route('/files/<filename>', methods=['GET'])
def serve_file(filename):
    return send_from_directory(os.environ['HOME'], 'sysd', filename)

@app.route('/files', methods=['POST'])
def upload_file():
    file = request.files['file']
    file.save(os.path.join(os.environ['HOME'], 'sysd', file.filename))
    return 'File uploaded successfully'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
