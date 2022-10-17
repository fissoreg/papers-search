import os
from argparse import ArgumentTypeError
from csv import field_size_limit
from sys import maxsize

import requests

from config import config


def download_csv(url, fp):
    response = requests.get(url)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "wb") as f:
        f.write(response.content)


def log(message):
    if config["print_logs"].get():
        print(message)


def maximise_csv_field_size_limit(maxInt=maxsize):
    while True:
        try:
            field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt / 10)


# boolean args:
# https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse/36031646
def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise ArgumentTypeError("Boolean value expected.")
