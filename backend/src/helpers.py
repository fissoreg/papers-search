import requests
import os

from backend_config import print_logs

def download_csv(url, fp):
    response = requests.get(url)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "wb") as f:
        f.write(response.content)

def log(message):
    if print_logs:
        print(message)
