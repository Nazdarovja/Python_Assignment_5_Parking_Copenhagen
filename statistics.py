import pandas as pd
import numpy as np
import plotting as plt
"""
Methods to handle statistics and plots.
"""
### HEADERS ###
# 'FID', 'vejkode', 'vejnavn', 'antal_pladser', 'restriktion',
# 'vejstatus', 'vejside', 'bydel', 'p_ordning', 'p_type', 'rettelsedato',
# 'oprettelsesdato', 'bemaerkning', 'id', 'taelle_id',
# 'startdato_midlertidigt_nedlagt', 'slutdato_midlertidigt_nedlagt',
# 'wkb_geometry'


#Hvor mange p-pladser er der i Indre By? 
def spots_in_cetre_of_town(parking_df):
    """
    Given dataframe, returns the total of spots in 'Indre by' and the street with most spots in touple.
    """
    spots_in_centre_df = parking_df[parking_df['bydel']  == 'Indre By'] # Get dataframe with all p-spots in Indre By
    spot_sum = spots_in_centre_df['antal_pladser'].sum()                # Count the total

        # - Hvilken vej har flest?
    # Group by streetnames, then sum the spot count columns and return df with the highest number.
    street = spots_in_centre_df.groupby('vejnavn')['antal_pladser'].agg(np.sum).nlargest(1) 
    ## create return tuple (middle value is complex because the value is the index value of the df... could probably been prettier)
    return (spot_sum, street.index.tolist()[0], street[0])

#2. Er der i København flest p-pladser i den side af vejen med lige eller ulige husnumre?
def parity_roadside_spots_in_copenhagen(parking_df):
    even = parking_df[parking_df['vejside']  == 'Lige husnr.']
    uneven = parking_df[parking_df['vejside']  == 'Ulige husnr.']
    # - Hvilken side har flest afmærkede parkeringsbåse?
    even_marked_parking = even[even['p_type'] == 'Afmærket parkering']
    uneven_marked_parking = uneven[uneven['p_type'] == 'Uafmærket parkering']
    return (len(even), len(uneven), len(even_marked_parking), len(uneven_marked_parking))

#3. Vis med et splittet bar-plot den procentvise fordeling(y-aksen) af private og offentlige p-pladser i hver by-del(x-aksen)
def private_public_spots_per_district(parking_df):
    """
    Given pandas df, returns a barplot with percentage of types of parkingspots per district
    """
    # Sort by vejstatus, then group by city districts, and sum all of the parking spots (first public then private)
    public_by_district_df = parking_df[parking_df['vejstatus'] == 'Kommunevej'].groupby('bydel')['antal_pladser'].agg(np.sum)
    private_by_district_df = parking_df[parking_df['vejstatus'] == 'Privat fællesvej'].groupby('bydel')['antal_pladser'].agg(np.sum)
    
    # Calculate the percentile for plotting
    totals = [i+j for i,j in zip(public_by_district_df.tolist(), private_by_district_df.tolist())]  # Total spots
    public_percentile = [i/j * 100 for i,j in zip(public_by_district_df.tolist(), totals)]          # % of public spots
    private_percentile = [i/j * 100 for i,j in zip(private_by_district_df.tolist(), totals)]        # % of private spots
    
    # Plot
    plt.plot_bar(public_percentile, private_percentile, public_by_district_df.index.tolist())

#5. Vis fordelingen af private parkeringspladser og parkeringsmuligheder for el-biler ift hver bydels gennemsnitlige bruttoindkomst.
def private_electric_spots_by_avg_brutto_income(parking_df, brutto_income_df):
    """
    Given parking_df and brutto_income_df returns a multi plot with private and electric parking as stacked bar plots,
    and a line plot with the avg brutto income of citizens per district.
    """
    private_by_district_df = parking_df[parking_df['vejstatus'] == 'Privat fællesvej'].groupby('bydel')['antal_pladser'].agg(np.sum)
    electric_by_district_df = parking_df[parking_df['p_ordning'] == 'El-Bil plads'].groupby('bydel')['antal_pladser'].agg(np.sum)