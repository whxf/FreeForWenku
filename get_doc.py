import argparse

import requests
from utils.url_to_txt import DOC
session = requests.session()

parser = argparse.ArgumentParser()
parser.add_argument('-url',type = str, required=True, help="baidu doc url")
parser.add_argument('-out',type = str, required=True, help="output directory")
args = parser.parse_args()

DOC(session, args.url, args.out)