import matplotlib.pyplot as plt
import numpy as np
import json
import folium as folium

"""
Plotting module used in statistics.py
"""


def plot_bar(public_percentile_list, private_percentile_list, districts_list):
    """
    Given lists with percentiles, and a list of districts, plots a stacked bar-plot with data
    """
    # Create plots
    p1 = plt.bar(districts_list, public_percentile_list)
    p2 = plt.bar(districts_list, private_percentile_list,
                 bottom=public_percentile_list)

    # Add plot options
    plt.legend((p2[0], p1[0]), ('Private', 'Public'))
    plt.title('Distribution of parking spots, per district')
    plt.ylabel('%')
    plt.xticks(rotation=75)
    # Show plot
    plt.show()


def private_electric_avg_income_multi_plot(districts_list, private_by_district_list, electric_by_district_list):

    p1 = plt.bar(districts_list, private_by_district_list)
    p2 = plt.bar(districts_list, electric_by_district_list, bottom=private_by_district_list)

    plt.show()
    


def plot_geo_json(data_df):

    # load GeoJSON geometries for Copenhagen
    with open('geo_json.json') as data_file:
        cph_map = json.load(data_file)

    from_df = data_df[data_df['vejstatus'] == 'Kommunevej']  # Bare til testing, der skal bruges gennemsnit af indkomst pr bydel
    df = from_df['bydel'].value_counts().reset_index()

    # instantiate a Folium map over DK
    map = folium.Map(location=[55.671544394943105,12.559142958299361], zoom_start=12)

    # apply geoJSON overlay on the map
    map.choropleth(geo_data=cph_map, data=df,
                   columns=['index', 'bydel'],
                   key_on='feature.id',
                   legend_name="Parking per district",
                   fill_color='YlGn', fill_opacity=0.7, line_opacity=0.2,
                   highlight=True)

    # save map as html
    map.save('plots_6.html')