#!"C:/Users/vladc/AppData/Local/Programs/Python/Python311/python.exe"
#!/usr/bin/env python3

from flask import Flask, render_template, request # for flask web server
import os # delete graphs after after they have been displayed
import glob # to delete graphs using a pattern

# import functions from other python files
from data_processing import find_zip_codes_and_county_within_radius, find_cheapest_5_hospitals, find_cheapest_5_insurance
from plotting import display_cheapest_hospitals, display_cheapest_insurance


app = Flask(__name__)
app.config['SECRET_KEY'] ='MyCareIQ#key#202307172018'


# Main page logic to get zip code and display relevant charts
@app.route('/', methods=('GET', 'POST'))
def mycareiq():
      
    # initialize
    hospital_graph = ''
    insurance_graph = ''
    message = ''
    radius_miles = 15 # set to the range miles within a given zip code to search for hospitals

    # clear directory of .png files
    # watchout this might cause a bug in production for simultaneous usage 
    # can be replaced by a server cleanup script
    images = glob.glob('./static/images/*.png', recursive=True)
    
    for image in images:
        try:
            os.remove(image)
        except OSError as e:
            message += f' Error: {e.strerror}. '
            return render_template('results.html', hospital_graph=hospital_graph, insurance_graph=insurance_graph, message=message)
    
    if request.method == 'POST':
        zip_code = request.form['zip_code']
        if not 'zip_code':
            message += ' A zip code entry is required. '
        else:
            # Find zip codes and county fips codes within a 5-mile radius
            zip_codes_list, county_fips_list = find_zip_codes_and_county_within_radius(zip_code, radius_miles)  
            
            # get the result cheapest hospitals and insurance for the entered zip code and surrounding areas
            if len(zip_codes_list) > 0 and len(county_fips_list) > 0:
                
                cheapest_5_hospitals = find_cheapest_5_hospitals(zip_codes_list)
                cheapest_5_insurance = find_cheapest_5_insurance(county_fips_list)
                
                if cheapest_5_hospitals.empty == False:
                    hospital_graph = display_cheapest_hospitals(cheapest_5_hospitals)
                else:
                    message += ' No hospitals found within your zip code in our dataset. '
                    
                if cheapest_5_insurance.empty == False:
                    insurance_graph = display_cheapest_insurance(cheapest_5_insurance)
                else:
                    message += ' No insurance providers found within your zip code in our dataset. '

            else:
                message += f' No matches found for zip code: {zip_code}. '         
                
    return render_template('results.html', hospital_graph=hospital_graph, insurance_graph=insurance_graph, message=message)


def main():
    mycareiq()

    
if __name__ == "__main__":
    main()
