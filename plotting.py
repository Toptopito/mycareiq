# contains functions for displaying charts for My Care IQ

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# import seaborn as sns

import uuid # to generate random file names


def display_cheapest_hospitals(cheapest_5_hospitals):
    
    # generate the plot
    plt.figure()
    cheapest_5_hospitals.sort_values(ascending=False).plot.barh(x='Rndrng_Prvdr_Org_Name', title='Most affordable hospitals', color='blue')
    plt.xlabel('Average charges in USD')
    plt.ylabel('Provider')
    
    # generate random filename then save the plot to a file
    returnfilename = "images/" + str(uuid.uuid4()) + ".png"
    tempfilename = "./static/" + returnfilename
    plt.savefig(tempfilename, bbox_inches='tight')
    
    return returnfilename


def display_cheapest_insurance(cheapest_5_insurance):
    
    # generate the plot
    plt.figure()
    cheapest_5_insurance.sort_values(ascending=False).plot.barh(x='Issuer Name', title='Most affordable insurance providers', color='blue')
    plt.xlabel('Average premiums in USD')
    plt.ylabel('Insurer')
    
    # generate random filename then save the plot to a file
    returnfilename = "images/" + str(uuid.uuid4()) + ".png"
    tempfilename = "./static/" + returnfilename
    plt.savefig(tempfilename, bbox_inches='tight')
    
    return returnfilename