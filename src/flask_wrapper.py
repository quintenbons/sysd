"""API Wrapper for Flask API (flase_server.py)"""
import os
import sys
import requests

class APIWrapper:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_file(self, filename):
      url = f"{self.base_url}/files/{filename}"
      response = requests.get(url)
      if response.status_code == 200:
        with open(filename, 'wb') as file:
          file.write(response.content)
        return True
      else:
        return False

    def upload_file(self, file):
      url = f"{self.base_url}/files"
      files = {'file': file}
      response = requests.post(url, files=files)
      if response.status_code == 200:
        return True
      else:
        return False

if __name__ == '__main__':
    target = "http://localhost:5000"
    if len(sys.argv) >= 2:
        target=sys.argv[1]
    api = APIWrapper(target)
    input("Some files will be downloaded from the server. Press enter to continue...")
    # Create temp file
    with open('temp.txt', 'w') as file:
        file.write("Hello World!")

    if api.upload_file(open('temp.txt', 'rb')):
        print("File uploaded successfully")
    else:
        print("File upload failed")

    os.remove('temp.txt')
    if api.get_file('temp.txt'):
        print("File downloaded successfully")
    else:
        print("File download failed")

    with open('temp.txt', 'r') as file:
        print(file.read())
