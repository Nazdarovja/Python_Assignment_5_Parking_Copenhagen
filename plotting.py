import matplotlib.pyplot as plt
import numpy as np


def plot_bar(public_df,private_df):
    
    p1 = plt.bar(public_df.index.tolist(),public_df.tolist())
    p2 = plt.bar(private_df.index.tolist(),private_df.tolist(), bottom=public_df.tolist())
    
    plt.legend((p1[0], p2[0]), ('Public', 'Private'))
    plt.show()