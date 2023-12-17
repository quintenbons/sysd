"""API Wrapper for Flask API (flase_server.py)"""
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
