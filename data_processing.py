# contains functions for data processing for the My Care IQ project
import pandas as pd # to use dataframes for data processing
from pyzipcode import ZipCodeDatabase # to generate zip codes within a radius


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
        df_hospitals_average_cost = df_hospitals_average_cost.sort_values()
        cheapest_5_hospitals = df_hospitals_average_cost.head(5)
        
        return cheapest_5_hospitals
        
    return pd.DataFrame() # empty dataframe

def find_cheapest_5_insurance(county_fips_list):
    # constant
    insurance_data_path = "./files/Individual_Market_Medical.csv"
    columns_list = ['Issuer Name', \
                    'Premium Child Age 0-14', 'Premium Child Age 18', \
                    'Premium Adult Individual Age 21', 'Premium Adult Individual Age 27', 'Premium Adult Individual Age 30 ', \
                    'Premium Adult Individual Age 40 ', 'Premium Adult Individual Age 50 ', 'Premium Adult Individual Age 60 ', \
                    'Premium Couple 21  ', 'Premium Couple 30 ', 'Premium Couple 40 ', 'Premium Couple 50 ', 'Premium Couple 60 ', \
                    'Couple+1 child, Age 21', 'Couple+1 child, Age 30 ', 'Couple+1 child, Age 40 ', 'Couple+1 child, Age 50 ', \
                    'Couple+3 or more Children, Age 21', 'Couple+3 or more Children, Age 30', 'Couple+3 or more Children, Age 40', \
                    'Couple+3 or more Children, Age 50', \
                    'Individual+1 child, Age 21', 'Individual+1 child, Age 30', 'Individual+1 child, Age 40', 'Individual+1 child, Age 50', \
                    'Individual+2 children, Age 21', 'Individual+2 children, Age 30', 'Individual+2 children, Age 40', \
                    'Individual+2 children, Age 50', \
                    'Individual+3 or more children, Age 21', 'Individual+3 or more children, Age 30', 'Individual+3 or more children, Age 40', \
                    'Individual+3 or more children, Age 50']
    
    # list insurance products in county fips list
    df_insurances = pd.read_csv(insurance_data_path)
    df_insurances['FIPS County Code'] = df_insurances['FIPS County Code'].astype(str)
    df_insurances_around = df_insurances[df_insurances['FIPS County Code'].isin(county_fips_list)]
    
    if df_insurances_around.empty:
        return pd.DataFrame() # empty dataframe
    else:
        # retain only needed columns for averaging calculation and drop NaN values
        df_insurances_around = df_insurances_around[df_insurances_around.columns.intersection(columns_list)]
        df_insurances_around = df_insurances_around.dropna()
        
        # change columns to numeric
        for column in columns_list:
            if column == 'Issuer Name':
                continue
            
            df_insurances_around[column] = df_insurances_around[column].str.replace('$', '') # remove $ sign
            df_insurances_around[column] = df_insurances_around[column].str.replace(',', '') # remove comma
            df_insurances_around[column] = pd.to_numeric(df_insurances_around[column])
        
        # average premiums column
        df_insurances_around['Average Premium'] = df_insurances_around.mean(axis=1, numeric_only=True)
        
        # get average premiums by insurance provider / issuer
        df_insurances_average_premiums = df_insurances_around.groupby(['Issuer Name'])['Average Premium'].mean()
        
        # sort then get top 5 cheapest insurances
        df_insurances_average_premiums = df_insurances_average_premiums.sort_values()
        cheapest_5_insurance = df_insurances_average_premiums.head(5)
        
        return cheapest_5_insurance
           
    
    return pd.DataFrame() # empty dataframe