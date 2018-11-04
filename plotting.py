import matplotlib.pyplot as plt
import numpy as np
"""
Plotting module used in statistics.py
"""

def plot_bar(public_percentile_list,private_percentile_list, districts_list):
    """
    Given lists with percentiles, and a list of districts, plots a stacked bar-plot with data
    """
    # Create plots
    p1 = plt.bar(districts_list, public_percentile_list)
    p2 = plt.bar(districts_list, private_percentile_list, bottom=public_percentile_list)
    
    ## Add plot options
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
    