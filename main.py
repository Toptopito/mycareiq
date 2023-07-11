#!"C:/Users/vladc/AppData/Local/Programs/Python/Python311/python.exe"
#!/usr/bin/env python3

import cgi # for python cgi programming
import pandas as pd # to use dataframes for data processing
from pyzipcode import ZipCodeDatabase # to generate zip codes within a radius
import os
import uuid

# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt
# import mpld3

#from matplotlib.figure import Figure


# remember to remove test and debug codes in productions
test = False
debug = True


# find list of zip codes and county fips codes within a radius
def find_zip_codes_and_county_within_radius(zip_code, radius_miles):
    # constant
    zipdb_file_path = "./files/uszips.csv"
    
    # Create a ZipCodeDatabase instance
    zcdb = ZipCodeDatabase()
    
    # Query for the entered zip code if it exists
    try:
        zcdb[zip_code]
    except:
        return [],[] # return empty lists to signify no matches

    # make sure zip code has 5 digits as required by get_zipcodes_around_radius()
    zip_code = zip_code.rjust(5, '0')

    # Search for zip codes that are near (within a radius in miles) the given zip code
    try:
        nearest_zipcodes = [z.zip for z in zcdb.get_zipcodes_around_radius(zip_code, radius_miles)]
    except:
        return [],[] # return empty lists to signify no matches
    
    # Remove leading zeroes in zip codes
    for i in range(len(nearest_zipcodes)):
        nearest_zipcodes[i] = int(nearest_zipcodes[i])
        nearest_zipcodes[i] = str(nearest_zipcodes[i])
   
    # create list of relevant county FIPS codes for nearest zip codes
    df_zipdb = pd.read_csv(zipdb_file_path)
    df_zipdb['zip'] = df_zipdb['zip'].astype(str)
    df_zipdb_nearest = df_zipdb[df_zipdb['zip'].isin(nearest_zipcodes)]
    df_zipdb_nearest['county_fips'] = df_zipdb_nearest['county_fips'].astype(str)
    nearest_county_fips = df_zipdb_nearest['county_fips'].values.tolist()

    # remove duplicate county FIPS then change back to list
    nearest_county_fips = set(nearest_county_fips)
    nearest_county_fips = list(nearest_county_fips)
    
    return nearest_zipcodes, nearest_county_fips


def find_cheapest_5_hospitals(zip_codes_list):
    # constant
    hospital_charges_path = "./files/Medicare_Inpatient_Hospital_by_Provider_and_Service_2021.csv"
    
    # list hospitals in the zip codes list
    df_hospitals = pd.read_csv(hospital_charges_path)
    df_hospitals['Rndrng_Prvdr_Zip5'] = df_hospitals['Rndrng_Prvdr_Zip5'].astype(str)
    df_hospitals_nearest = df_hospitals[df_hospitals['Rndrng_Prvdr_Zip5'].isin(zip_codes_list)]
    
    if df_hospitals_nearest.empty:
        return pd.DataFrame() # empty dataframe
    else:
        # get average cost by hospital
        df_hospitals_average_cost = df_hospitals_nearest.groupby(['Rndrng_Prvdr_Org_Name'])['Avg_Tot_Pymt_Amt'].mean()
        
        # sort then get top 5 most affordable
        sorted_hospitals = df_hospitals_average_cost.sort_values()
        cheapest_5_hospitals = sorted_hospitals.head(5)
        return cheapest_5_hospitals
        
    return pd.DataFrame() # empty dataframe


def find_cheapest_5_insurance(county_fips_list):
    return []


def display_cheapest_hospitals(cheapest_5_hospitals):
    return ""


def display_cheapest_insurance(cheapest_5_insurance):
    return ""


# HTML template
def create_html_template():
    return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Care IQ</title>
    <!-- bootstrap css -->
    <link rel="stylesheet" href="css/hightech/css/bootstrap.min.css">
    <!-- style css -->
    <link rel="stylesheet" href="css/hightech/css/style.css">
    <!-- responsive-->
    <link rel="stylesheet" href="css/hightech/css/responsive.css">
    <!-- awesome fontfamily -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <!--[if lt IE 9]>
    <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
    <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script><![endif]-->   
</head>
<body>
    <div class="container">
        <h1>What are my most affordable care options?</h1>
        <form method="post">
            <div class="mb-3">
                <label for="zip_code" class="form-label">Enter your zip code:</label>
                <input type="text" class="form-control" id="zip_code" name="zip_code" required>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
        <br>
        %s
    </div>
    <br><br><br><br>
    <p style="font-size:8px; text-align: center"><i>US Zip Code Directory courtesy of <a href=https://simplemaps.com/data/us-zips>simplemaps.com</a>.</i></p>
</body>
</html>
"""


# results HTML
def create_result_html(cheapest_5_hospitals, cheapest_5_insurance):
    if cheapest_5_hospitals and cheapest_5_insurance:
        result_html = display_cheapest_hospitals(cheapest_5_hospitals)
        result_html += display_cheapest_insurance(cheapest_5_insurance)
    else:
        result_html = "<h2>No hospitals and insurance providers found within your zip code</h2>"
    
    return result_html


# Main CGI logic
def main():
    # constants
    radius_miles = 15   
    
    if test: # tests codes here remove in production
        zip_codes_list, county_fips_list = find_zip_codes_and_county_within_radius('22192', radius_miles)
        
        if len(zip_codes_list) == 0:
            print("Invalid Zip Code!")
        else:
            cheapest_5_hospitals = find_cheapest_5_hospitals(zip_codes_list)
            
            # if cheapest_5_hospitals.empty == False:
            #     #plot
                # fig = plt.figure()
                # cheapest_5_hospitals.sort_values(ascending=False).plot.barh(x='Rndrng_Prvdr_Org_Name', title='Most affordable hospitals', color='blue')
                # plt.xlabel('Average charges in USD')
                # plt.ylabel('Provider')
                # tempfilename = "./tempfiles/" + str(uuid.uuid4()) + ".png"
                # plt.savefig(tempfilename, bbox_inches='tight')

            
    else:
        # Create an instance of FieldStorage
        form = cgi.FieldStorage()

        if "zip_code" in form:
            # Get the zip code from the form
            zip_code = form.getvalue("zip_code")
                      
            # Find zip codes and county fips codes within a 5-mile radius
            zip_codes_list, county_fips_list = find_zip_codes_and_county_within_radius(zip_code, radius_miles)
            
            # get the result cheapest hospitals and insurance for the entered zip code and surrounding areas
            if len(zip_codes_list) > 0 and len(county_fips_list) > 0:
                
                cheapest_5_hospitals = find_cheapest_5_hospitals(zip_codes_list)
                cheapest_5_insurance = find_cheapest_5_insurance(county_fips_list)
                               
                # debug codes remove in production
                if debug:
                    result_html = f"<p>List of zip codes: {zip_codes_list}</p><br>"
                    result_html += f"<p>List of county fips codes: {county_fips_list}</p><br>"
                    if cheapest_5_hospitals.empty == False:
                        result_html += f"<p>Cheapest 5 hospitals: {cheapest_5_hospitals}</p><br>"
                        result_html += '<img src=\"./tempfiles/39c3b0f8-502b-4cf4-b660-a1d5abc0ff8d.png\">'
                
                # display the results        
                #result_html = create_result_html(cheapest_5_hospitals, cheapest_5_insurance)
                
            else:
                result_html = f"<h2>No matches found for zip code: {zip_code}</h2>"
                    
                    
            # Create the final HTML response
            response_html = create_html_template() % result_html
                    
            # Set the Content-Type header to HTML
            print("Content-Type: text/html\n\n")
            print()
            print(response_html)
        else:
            # Show the initial form
            response_html = create_html_template() % ""
                        
            # Set the Content-Type header to HTML
            print("Content-Type: text/html\n\n")
            print()
            print(response_html)

    
if __name__ == "__main__":
    main()
