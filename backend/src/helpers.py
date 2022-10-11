import os
from csv import field_size_limit
from sys import maxsize

import requests

from backend_config import print_logs


def download_csv(url, fp):
    response = requests.get(url)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "wb") as f:
        f.write(response.content)


def log(message):
    if print_logs:
        print(message)


def maximise_csv_field_size_limit(maxInt=maxsize):

    while True:
        try:
            field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt / 10)
