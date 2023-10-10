# SSR_Automation
Python script that automates the task of individually running Medi-Cal Single Subscriber Response Eligibility checks, and saves the results to a file.

# Packages to install
    Requests
    BeautifulSoup
    Openpyxl
    Dotenv
- pip install requests bs4 openpyxl dotenv

# Login with Medi-Cal Credentials
  Create a **.env** file and replace *"your_username_here"* & *"your_password_here"* with your Medi-Cal Transaction Services username & password

    LOGIN_USERNAME=your_username_here
    LOGIN_PASSWORD=your_password_here

# Load Entry List
  In **subscriber_list.xlsx** add entries to be run in each row in the following format:

    Subscriber ID 1    DOB 1 (MM/DD/YYYY)    Issue Date 1 (MM/DD/YYYY)    Service Date 1 (MM/DD/YYYY)
    Subscriber ID 2    DOB 2 (MM/DD/YYYY)    Issue Date 2 (MM/DD/YYYY)    Service Date 2 (MM/DD/YYYY)
    ...

# Run script
  Open a terminal and run the script with **py script.py**.
  
  Results will be saved in **Results.xlsx**.
