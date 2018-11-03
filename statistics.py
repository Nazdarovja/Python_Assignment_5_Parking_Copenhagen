import pandas as pd
import numpy as np
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