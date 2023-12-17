from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)

@app.route('/files/<filename>', methods=['GET'])
def serve_file(filename):
    realpath = os.path.realpath(os.path.curdir)
    return send_from_directory(realpath, filename)

@app.route('/files', methods=['POST'])
def upload_file():
    file = request.files['file']
    file.save(file.filename)
    return 'File uploaded successfully'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
