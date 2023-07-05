#!"C:/Users/vladc/AppData/Local/Programs/Python/Python311/python.exe"

import cgi
import pandas as pd
from pyzipcode import ZipCodeDatabase
# import csv
# from geopy.distance import geodesic

# remember to remove test and debug codes in productions
test = False

#!/usr/bin/env python3


def display_cheapest_hospitals(cheapest_5_hospitals):
    return None


def display_cheapest_insurance(cheapest_5_insurance):
    return None


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
        return [],[]

    # # Open the CSV file containing zip codes and location data
    # with open(zipdb_file_path, newline='') as csvfile:
    #     reader = csv.DictReader(csvfile)

    #     # Search for the nearest 5 zip codes in the CSV file
    #     nearest_zipcodes = [zip_code]
    #     for row in reader:
    #         dist = geodesic((zip_obj.latitude, zip_obj.longitude), (float(row['lat']), float(row['lng']))).miles
    #         if dist <= radius_miles and row['zip'] != zip_code:
    #             nearest_zipcodes.append(row['zip'])

    # Search for zip codes that are near (within a radius in miles) the given zip code
    nearest_zipcodes = [z.zip for z in zcdb.get_zipcodes_around_radius(zip_code, radius_miles)]
   
    # find relevant county FIPS codes for nearest zip codes
    df_zipdb = pd.read_csv(zipdb_file_path)
    df_zipdb['zip'] = df_zipdb['zip'].astype(str)
    df_zipdb_nearest = df_zipdb[df_zipdb['zip'].isin(nearest_zipcodes)]
    
    nearest_county_fips = df_zipdb_nearest['county_fips'].values.tolist()

    # remove duplicate county FIPS then change back to list
    nearest_county_fips = set(nearest_county_fips)
    nearest_county_fips = list(nearest_county_fips)
    
    return nearest_zipcodes, nearest_county_fips


def find_cheapest_5_hospitals(zip_codes_list):
    return []


def find_cheapest_5_insurance(county_fips_list):
    return []


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
    radius_miles = 5   
    
    if test: # tests codes here remove in production
        zip_codes_list, county_fips_list = find_zip_codes_and_county_within_radius('22192', radius_miles)
        
        if len(zip_codes_list) == 0:
            print("Invalid Zip Code!")
        else:
            print(zip_codes_list, county_fips_list)
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
                
                # display the results        
                result_html = create_result_html(cheapest_5_hospitals, cheapest_5_insurance)
                
                # debug codes remove in production
                result_html = f"<h2>List of zip codes: {zip_codes_list}</h2><br>"
                result_html += f"<h2>List of county fips codes: {county_fips_list}</h2>"
                           
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
