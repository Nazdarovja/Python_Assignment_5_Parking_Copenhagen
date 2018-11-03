from utils.downloader import download_as_file
import pandas as pd
import statistics
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

#1. Hvor mange p-pladser er der i Indre By? 
    spot_count, street, street_count = statistics.spots_in_cetre_of_town(parking_df)
#    - Hvilken vej har flest?
    print(f'There is {spot_count} in `Indre By` and the street with most spots is {street} with {street_count} spots')
    
#2. Er der i København flest p-pladser i den side af vejen med lige eller ulige husnumre?
#    - Hvilken side har flest afmærkede parkeringsbåse?

#3. Vis med et splittet bar-plot den procentvise fordeling(y-aksen) af private og offentlige p-pladser i hver by-del(x-aksen)

#4. Hvilken familietype har de bedste parkeringsmuligheder?

#5. Vis fordelingen af private parkeringspladser og parkeringsmuligheder for el-biler ift hver bydels gennemsnitlige bruttoindkomst.

#6. Farvekod på et kort bydelene i København, ud fra den gennemsnitlige bruttoindkomst. Plot markers med private (P) og el-bil-parkeringspladser (EL)
