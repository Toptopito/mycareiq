# mycareiq
Source code and other files for the My Care IQ platform

Test Environment Creation: 
1. Follow instructions here to configure XAMPP: https://blog.terresquall.com/2021/10/running-python-in-xampp/
2. Clone the repository in the "XAMPP htdocs folder" in your development computer
3. In the "XAMPP htdocs folder", go to the 'mycareiq" folder and create a folder named "files"
4. In the "files" folder, copy the following datasets: Individual_Market_Medical.csv, Medicare_Inpatient_Hospital_by_Provider_and_Service_2021.csv, and uszips.csv (files are too big to be uploaded in the repository)
5. Install the following libraries using pip install: cgi, pandas, pyzipcode, csv, geopy
6. In main.py change the first line to the location of python.exe in your computer
7. To run the XAMPP app as an administrator
8. Go to this URL in your browser: http://localhost/mycareiq/main.py
