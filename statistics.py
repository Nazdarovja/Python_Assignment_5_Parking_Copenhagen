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
    districts_list = private_by_district_df.index.tolist()
    avg_income_per_district = calculate_income_per_district(brutto_income_df, True)

    plt.private_electric_avg_income_multi_plot(districts_list, private_by_district_df.tolist(), electric_by_district_df.tolist(), avg_income_per_district)

#6. Farvekod på et kort bydelene i København, ud fra den gennemsnitlige bruttoindkomst. Plot markers med private (P) og el-bil-parkeringspladser (EL)
def plot_and_color_parking_by_private_and_electric(parking_df, brutto_income_df, cph_map_json):
    private_spots_df = parking_df[parking_df['vejstatus'] == 'Privat fællesvej']
    electric_spots_df = parking_df[parking_df['p_ordning'] == 'El-Bil plads']

    # Creates lists of tuples with coordinates ex. (12.333, 32.34343)
    private_coor_list = private_spots_df['wkb_geometry'].apply(create_coordinates)
    electric_coor_list = electric_spots_df['wkb_geometry'].apply(create_coordinates)

    # Create avg income df
    avg_income_df = calculate_income_per_district(brutto_income_df, False)

    plt.plot_geo_json(avg_income_df,cph_map_json, private_coor_list, electric_coor_list)


def create_coordinates(row): 
    row = str(row)
    if len(row) > 10:
        row = row.replace('(','').split(' ')
        row[2] = row[2].replace(',','')
        x = float(row[1])
        y = float(row[2])
        return (x,y)
    return (0,0)

def clean_up_names(name):
    split_nr = 3
    if name.startswith('10'):
        split_nr = 4
    
    return name[split_nr:]

def calculate_income_per_district(brutto_income_df, sorted):
    # Get only year 2014
    brutto_income_df = brutto_income_df[brutto_income_df['AAR'] == 2014]
    
    # Remove bydel 99 (unknown)
    brutto_income_df = brutto_income_df[brutto_income_df['BYDEL'] != 99]
    
    # # String manipulate names to use.
    brutto_income_df['DISTRIKTSNAVN'] = brutto_income_df['DISTRIKTSNAVN'].map(clean_up_names)
    

    ## income groups and their avarage salary
    income_groups = {
        1: 25000,
        2: 75000,
        3: 125000,
        4: 175000,
        5: 250000,
        6: 350000,
        7: 450000,
        8: 550000,
        9: 650000,
        10: 700000
    }

    # uses the dictionary above to create a numeric value for the average income
    brutto_income_df['average_income'] = pd.Series([income_groups[value] for _, value in brutto_income_df['BRUTTOINDKOM'].iteritems()])
    # Sort alphabeticly for one use case of the method
    if sorted:
        brutto_income_df = brutto_income_df.sort_values('DISTRIKTSNAVN')
    # Calculates to sum of all "hustande"'s income for each line
    brutto_income_df['income_times_houses'] = brutto_income_df['average_income'] * brutto_income_df['HUSTANDE']
    # Calculates the amount of houses per district
    houses_per_district = brutto_income_df.groupby('BYDEL')['HUSTANDE'].sum()
    # Calculates the sum of an entire district's income
    income_sum_per_district = brutto_income_df.groupby('BYDEL')['income_times_houses'].sum()
    # Returns the average income for each district
    return income_sum_per_district / houses_per_district