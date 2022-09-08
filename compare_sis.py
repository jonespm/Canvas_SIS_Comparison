#!/usr/bin/python

import argparse, logging, os, zipfile
from glob import glob

import pandas as pd

logger = logging.getLogger(__name__)

# Parse command line arguments to variables
def parse_args():
    parser = argparse.ArgumentParser(description='Compare SIS files')
    parser.add_argument('csv_name', help='CSV Name in Extract')
    parser.add_argument('extract_file', help='Extract File')
    parser.add_argument('archive_directory', help='Archive Directory')
    return parser.parse_args()

def compare_dataframes(extract_data, archive_data):
    # Compare dataframes
    if extract_data.equals(archive_data):
        logger.info('Dataframes are equal')
    else:
        logger.info('Dataframes are not equal')

def process_csvs(args):
    archive_data = dict()
    # First read the zip file specificed in the second argument into a pandas dataframe
    with zipfile.ZipFile(args.extract_file) as z:    
        for zip_filename in z.namelist():
            # If lowercase csv_name is in filename, then we have a match
            if args.csv_name in zip_filename.lower():
                # Read the file from the zip archive to a dataframe
                extract_data = pd.read_csv(z.open(zip_filename))

    # Get all sorted zip files in archive directory
    archive_files = sorted(glob(os.path.join(args.archive_directory, '*.zip')))

    # Find any files in this directory that are after this files date, and read them into a dataframe
    for archive_filename in archive_files:
        if archive_filename > args.extract_file:
            with zipfile.ZipFile(archive_filename) as z:
                for zip_filename in z.namelist():
                    if args.csv_name in zip_filename.lower():
                        print (f"Reading {archive_filename}")
                        try:
                            archive_data[archive_filename] = pd.read_csv(z.open(zip_filename))
                        except UnicodeDecodeError as e:
                            print (f"Error reading {archive_filename}")

    return(extract_data, archive_data)

def __main__():
    # Parse command line arguments
    args = parse_args()

    # Setup logging
    logging.basicConfig(level=logging.INFO)

    # Process CSVs
    (extract_data, archive_data) = process_csvs(args)
    compare_dataframes(extract_data, archive_data)

if __name__ == '__main__':
    __main__()
