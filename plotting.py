import matplotlib.pyplot as plt
import numpy as np
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


def private_electric_avg_income_multi_plot(districts_list, private_by_district_list, electric_by_district_list, avg_income_per_district):
    red = 'tab:red'
    blue = 'tab:blue'
    fig, ax1 = plt.subplots()
    ax1.set_ylabel('Parking spots', color=blue)
    ax1.bar(districts_list, private_by_district_list)
    ax1.bar(districts_list, electric_by_district_list,
                 bottom=private_by_district_list)
    
    ax2 = ax1.twinx()
    ax2.plot(avg_income_per_district, color=red)
    ax2.set_ylabel('Income per house', color=red)
    fig.tight_layout()
    plt.show()


def plot_geo_json(avg_income_df, cph_map_json, private_coor, electric_coor):
    # instantiate a Folium map over DK
    map = folium.Map(location=[55.671544394943105,
                               12.559142958299361], zoom_start=12)

    # apply geoJSON overlay on the map
    map.choropleth(geo_data=cph_map_json, data=avg_income_df,
                   columns=['index', 'bydel'],
                   key_on='properties.bydel_nr',
                   legend_name="Parking per district",
                   fill_color='YlGn', fill_opacity=0.7, line_opacity=0.2,
                   highlight=True)

    for plot in private_coor:
        if not plot[0] == 0:
            # Privat
            folium.Marker( 
                [plot[1], plot[0]],
                tooltip="Privat",
                icon=folium.Icon(color='red', icon='info-sign')).add_to(map)

    for plot in electric_coor:
        if not plot[0] == 0:
            # el-bil
            folium.Marker(
            [plot[1], plot[0]],
            tooltip="el-bil",
            icon=folium.Icon(color='green')).add_to(map)

    # save map as html
    map.save('plots_6.html')
