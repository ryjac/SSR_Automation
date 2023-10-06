import requests
# import subprocess
from bs4 import BeautifulSoup

# Define headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Start a session
session = requests.Session()
session.headers.update(headers)

def login_to_medi_cal():
    # Medi-Cal Credentials
    username = "enter_username"
    password = "enter_password"

    # URL
    login_url = 'https://secure.medi-cal.ca.gov/mcwebpub/login.aspx'

    # Fetch the login page first
    response = session.get(login_url)

    # Use BeautifulSoup to parse the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the necessary hidden form fields
    viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
    viewstategenerator = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']
    eventvalidation = soup.find('input', {'name': '__EVENTVALIDATION'})['value']

    # Create the payload using the extracted values and your actual credentials
    form_data = {
        '__VIEWSTATE': viewstate,
        '__VIEWSTATEGENERATOR': viewstategenerator,
        '__EVENTVALIDATION': eventvalidation,
        'ctl00$MainContent$txtUserID': username,
        'ctl00$MainContent$txtPassword': password,
        'ctl00$MainContent$btnSubmit': 'Login'
    }

    # POST the payload
    login_response = session.post(login_url, data=form_data)

    # Display status code
    print("Status Code:", login_response.status_code)

    # Check the response to see if the login was successful
    # Update this check based on the expected behavior of a successful login
    if 'Single Subscriber' in login_response.text:
        print('Login successful!')
        
        next_page_url = 'https://secure.medi-cal.ca.gov/eligibility/Eligibility.aspx'
        response_next_page = session.get(next_page_url)
        
        if 'Subscriber ID' in response_next_page.text:
            print('Navigated to SSR Form')
            submit_ssr()
        
        # print(response_next_page.text)
    else:
        print('Login failed!')
        
def get_next_entry(file):
    """
    Get the next set of details from the file.
    Returns a dictionary with the details or None if the end of the file is reached.
    """
    recip_id = file.readline().strip()
    if not recip_id:  # End of file reached
        return None

    recip_dob = file.readline().strip()
    recip_doi = file.readline().strip()
    recip_dos = file.readline().strip()
    
    # Skip the blank line
    file.readline()

    return {
        "recip_id": recip_id,
        "recip_dob": recip_dob,
        "recip_doi": recip_doi,
        "recip_dos": recip_dos
    }        

def submit_ssr():
    # Read ssr to be ran from a file
    with open('ssr.txt', 'r') as file:
        while True:
            entry = get_next_entry(file)
            if entry is None:
                break  # End of file reached, exit loop
    
            # Use BeautifulSoup to parse the page
            eligibility_page_url = 'https://secure.medi-cal.ca.gov/eligibility/Eligibility.aspx'
            response_eligibility = session.get(eligibility_page_url)
            soup_eligibility = BeautifulSoup(response_eligibility.content, 'html.parser')

            # Extract hidden fields
            viewstate = soup_eligibility.find('input', {'name': '__VIEWSTATE'})['value']
            viewstategenerator = soup_eligibility.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']
            eventvalidation = soup_eligibility.find('input', {'name': '__EVENTVALIDATION'})['value']

            # Create the payload using the extracted values and values from the entry
            eligibility_data = {
                '__VIEWSTATE': viewstate,
                '__VIEWSTATEGENERATOR': viewstategenerator,
                '__EVENTVALIDATION': eventvalidation,
                'ctl00$MainContent$RecipID': entry["recip_id"],
                'ctl00$MainContent$RecipDOB': entry["recip_dob"],
                'ctl00$MainContent$RecipDOI': entry["recip_doi"],
                'ctl00$MainContent$RecipDOS': entry["recip_dos"],
                '__ASYNCPOST': 'true',
                'ctl00$MainContent$Submit': 'Submit'
            }

            eligibility_response = session.post(eligibility_page_url, data=eligibility_data)

            # Display status code
            print("Status Code:", eligibility_response.status_code)
    
            # if 'Single Subscriber Response' in eligibility_response.text:
            print('Submit successful!')
    
            results_page_url = 'https://secure.medi-cal.ca.gov/Eligibility/EligResp.aspx'
            results_next_page = session.get(results_page_url)
    
            if 'Single Subscriber Response' in results_next_page.text:
                print('Obtained SSR Results:')

                # Parse results
                soup = BeautifulSoup(results_next_page.text, 'html.parser')
                
                # Extracting the data with error handling

                eligibility_message_elem = soup.find('span', {'id': 'MainContent_lblMessages'})
                eligibility_message = eligibility_message_elem.text if eligibility_message_elem else "Not Found"

                subscriber_name_elem = soup.find('div', {'id': 'MainContent_trname'})
                subscriber_name = subscriber_name_elem.text.replace("Subscriber Name: ", "").strip() if subscriber_name_elem else "Not Found"

                subscriber_id_elem = soup.find('div', {'id': 'MainContent_trssntrue'})
                subscriber_id = subscriber_id_elem.text.replace("Subscriber ID: ", "").strip() if subscriber_id_elem else "Not Found"

                birth_date_b_tag = soup.find('b', string="Subscriber Birth Date: ")
                if birth_date_b_tag:
                    birth_date = birth_date_b_tag.next_sibling.strip()
                else:
                    birth_date = "Not Found"
                    
                issue_date_b_tag = soup.find('b', string="Issue Date: ")
                if issue_date_b_tag:
                    issue_date = issue_date_b_tag.next_sibling.strip()
                else:
                    issue_date = "Not found"
                    
                primary_aid_code_b_tag = soup.find('b', string="Primary Aid Code: ")
                if primary_aid_code_b_tag:
                    primary_aid_code = primary_aid_code_b_tag.next_sibling.strip()
                else:
                    primary_aid_code = "Not found"

                responsible_county_b_tag = soup.find('b', string="Responsible County: ")
                if responsible_county_b_tag:
                    responsible_county = responsible_county_b_tag.next_sibling.strip()
                else:
                    responsible_county = "Not found"
                    
                service_date_b_tag = soup.find('b', string="Service Date: ")
                if service_date_b_tag:
                    service_date = service_date_b_tag.next_sibling.strip()
                else:
                    service_date = "Not found"

                trace_number_elem = soup.find('span', {'id': 'MainContent_lblEVCNo'})
                trace_number = trace_number_elem.text if trace_number_elem else "Not Found"

                
                # Print to console
                print("Eligibility Message:", eligibility_message)
                print("Subscriber Name:", subscriber_name)
                print("Subscriber ID:", subscriber_id)
                print("Birth Date:", birth_date)
                print("Issue Date:", issue_date)
                print("Primary Aid Code:", primary_aid_code)
                print("Responsible County:", responsible_county)
                print("Service Date:", service_date)
                print("Trace Number:", trace_number)

                # Save to results.txt
                with open('results.txt', 'a') as f:
                    f.write("Eligibility Message: " + eligibility_message + "\n")
                    f.write("Subscriber Name: " + subscriber_name + "\n")
                    f.write("Subscriber ID: " + subscriber_id + "\n")
                    f.write("Birth Date: " + birth_date + "\n")
                    f.write("Issue Date: " + issue_date + "\n")
                    f.write("Primary Aid Code: " + primary_aid_code + "\n")
                    f.write("Responsible County: " + responsible_county + "\n")
                    f.write("Service Date: " + service_date + "\n")
                    f.write("Trace Number: " + trace_number + "\n\n")
                    
                print("Results saved in 'Results.txt'")
        
login_to_medi_cal()