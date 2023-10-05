#!/usr/bin/env python3
"""
This script is using the already installed assetfinder script.
Based on the result it searches for only result which have the given domain url.
"""

import subprocess
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-u", dest="url", help="Enter valid url (tesla.com)", required=True)
parsed_args = parser.parse_args()

output = subprocess.Popen(["assetfinder", parsed_args.url], stdout=subprocess.PIPE).communicate()[0]

output = output.decode("utf-8")
name_of_file = parsed_args.url

with open(f"{name_of_file}.txt", "w") as f:
    output_list = output.replace("\n", ":").split(":")

    unique_urls = set()

    for url in output_list:
        if parsed_args.url in url:
            unique_urls.add(url)

    for unique_url in unique_urls:
        f.write(unique_url + "\n")

