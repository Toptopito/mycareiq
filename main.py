#!"C:/Users/vladc/AppData/Local/Programs/Python/Python311/python.exe"

import cgi
import pandas as pd


#!/usr/bin/env python3


def display_cheapest_hospitals(cheapest_5_hospitals):
    return None


def display_cheapest_insurance(cheapest_5_insurance):
    return None


# find list of zip codes and county fips codes within a radius
def find_zip_codes_and_county_within_radius(zip_code, radius_miles):
    return [],[]


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
