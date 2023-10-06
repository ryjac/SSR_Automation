# SSR_Automation
Python script that automates the task of individually running Medi-Cal Single Subscriber Response Eligibility checks, and saves the results to a file.

# Login with Medi-Cal Credentials
  In **login_to_medi_cal()** replace *"enter_username"* and *"enter_password"* with your Medi-Cal Transaction Services username & password
  ##
    def login_to_medi_cal():
      # Medi-Cal Credentials
      username = "enter_username"
      password = "enter_password"

# Load Entry List
  In **ssr.txt** add entries separated by a new line.
  ##
    Subscriber ID 1
    DOB 1 (MM/DD/YYYY)
    Issue Date 1 (MM/DD/YYYY)
    Service Date 1 (MM/DD/YYYY)

    Subscriber ID 2
    DOB 2 (MM/DD/YYYY)
    Issue Date 2 (MM/DD/YYYY)
    Service Date 2 (MM/DD/YYYY)

    ...

# Run script
  Open a terminal and run the script with **py script.py**.
  
  Results will be saved in **results.txt**.
