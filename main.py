from utils.downloader import download_as_file
import pandas as pd
"""
To run project `$python main.py`
"""
URL_PARKING_DATA = 'http://wfs-kbhkort.kk.dk/k101/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=k101:p_pladser&outputFormat=csv&SRSNAME=EPSG:4326'
URL_BRUTTO_INCOME_DATA = 'https://data.kk.dk/dataset/e734af29-4e40-4754-9cce-789a7513dd8a/resource/bd5b19ee-cedd-4b69-9272-532a1bce1eee/download/indkomstbruttohustypev.csv'
PARKING_DATA_FILE_NAME = 'parking_data.csv'
BRUTTO_INCOME_FILE_NAME = 'brutto_income.csv'

if __name__ == '__main__':
    download_as_file(URL_PARKING_DATA, PARKING_DATA_FILE_NAME)
    download_as_file(URL_BRUTTO_INCOME_DATA, BRUTTO_INCOME_FILE_NAME)

    ## read the csv files to dataframes, filter away all error prone lines.
    parking_df = pd.read_csv(PARKING_DATA_FILE_NAME, encoding='utf-8', low_memory=False, error_bad_lines=False)
    brutto_income_df = pd.read_csv(BRUTTO_INCOME_FILE_NAME, encoding='utf-8', low_memory=False, error_bad_lines=False)
