from utils.downloader import download_as_file
import pandas as pd
import statistics
import json

"""
To run project `$python main.py`
"""
URL_PARKING_DATA = 'http://wfs-kbhkort.kk.dk/k101/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=k101:p_pladser&outputFormat=csv&SRSNAME=EPSG:4326'
URL_BRUTTO_INCOME_DATA = 'https://data.kk.dk/dataset/e734af29-4e40-4754-9cce-789a7513dd8a/resource/bd5b19ee-cedd-4b69-9272-532a1bce1eee/download/indkomstbruttohustypev.csv'
URL_P_PLADSER_GEOJSON = 'http://wfs-kbhkort.kk.dk/k101/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=k101:p_pladser&outputFormat=json&SRSNAME=EPSG:4326&maxfeatures=1000000'
URL_P_BYDEL_GEOJSON = 'http://wfs-kbhkort.kk.dk/k101/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=k101:bydel&outputFormat=json&SRSNAME=EPSG:4326'
PARKING_DATA_FILE_NAME = 'parking_data.csv'
BRUTTO_INCOME_FILE_NAME = 'brutto_income.csv'
GEOJSON_BYDELE_FILE_NAME = 'geo_json_bydele.json'

if __name__ == '__main__':
    download_as_file(URL_PARKING_DATA, PARKING_DATA_FILE_NAME)
    download_as_file(URL_BRUTTO_INCOME_DATA, BRUTTO_INCOME_FILE_NAME)
    download_as_file(URL_P_BYDEL_GEOJSON, GEOJSON_BYDELE_FILE_NAME)

    ## read the csv files to dataframes, filter away all error prone lines.
    parking_df = pd.read_csv(PARKING_DATA_FILE_NAME, encoding='utf-8', low_memory=False, error_bad_lines=False)
    brutto_income_df = pd.read_csv(BRUTTO_INCOME_FILE_NAME, encoding='utf-8', low_memory=False, error_bad_lines=False)

    ## Read json files to memory
    # load GeoJSON geometries for Copenhagen
    with open(GEOJSON_BYDELE_FILE_NAME) as data_file:
        cph_map_json = json.load(data_file)

#1. Hvor mange p-pladser er der i Indre By? 
    spot_count, street, street_count = statistics.spots_in_cetre_of_town(parking_df)
#    - Hvilken vej har flest?
    print(f'There is {spot_count} in `Indre By` and the street with most spots is {street} with {street_count} spots')
    
#2. Er der i København flest p-pladser i den side af vejen med lige eller ulige husnumre?
#    - Hvilken side har flest afmærkede parkeringsbåse?
    even, uneven,even_marked_parking,uneven_marked_parking = statistics.parity_roadside_spots_in_copenhagen(parking_df)
    print(f'There are {even} even spots and {uneven} uneven spots in Copenhagen; Most spots at the even side of the road.')
    print(f'- There are {even_marked_parking} even marked spots and {uneven_marked_parking} uneven marked spots; Most marked spots at the uneven side of the road.')

#3. Vis med et splittet bar-plot den procentvise fordeling(y-aksen) af private og offentlige p-pladser i hver by-del(x-aksen)

    statistics.private_public_spots_per_district(parking_df)

#4. Hvilken familietype har de bedste parkeringsmuligheder?

 ################# IKKE RIGTIG DATA TIL AT LAVE DENNE PLOT #############################

#5. Vis fordelingen af private parkeringspladser og parkeringsmuligheder for el-biler ift hver bydels gennemsnitlige bruttoindkomst.
    statistics.private_electric_spots_by_avg_brutto_income(parking_df, brutto_income_df)

#6. Farvekod på et kort bydelene i København, ud fra den gennemsnitlige bruttoindkomst. Plot markers med private (P) og el-bil-parkeringspladser (EL)
    statistics.plot_and_color_parking_by_private_and_electric(parking_df, brutto_income_df, cph_map_json)