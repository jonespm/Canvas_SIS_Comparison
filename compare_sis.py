#!/usr/bin/python

import argparse, logging, os, sys, zipfile

import pandas as pd

logger = logging.getLogger(__name__)

# Parse command line arguments to variables
def parse_args():
    parser = argparse.ArgumentParser(description='Compare SIS files')
    parser.add_argument('csv_name', help='CSV Name in Extract')
    parser.add_argument('extract_file', help='Extract File')
    return parser.parse_args()

args = parse_args()

data = dict()

# First read the zip file specificed in the second argument into a pandas dataframe
with zipfile.ZipFile(args.extract_file) as z:    
    for zip_filename in z.namelist():
        # If lowercase csv_name is in filename, then we have a match
        if args.csv_name in zip_filename.lower():
            # Read the file from the zip archive to a dataframe
            extract_data = pd.read_csv(z.open(zip_filename))

# Find any files in this directory that are after this files date, and read them into a dataframe
for extract_filename in os.listdir("."):
    if extract_filename.endswith(".zip"):
        if extract_filename > args.extract_file:
            with zipfile.ZipFile(extract_filename) as z:
                for zip_filename in z.namelist():
                    if args.csv_name in zip_filename.lower():
                        data[extract_filename] = pd.read_csv(z.open(zip_filename))

print(data)
