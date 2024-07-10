import requests
from bs4 import BeautifulSoup

# Replace these with the cookies captured from HTTP Toolkit
cookies = {
    'li_at': 'AQEFARABAAAAABBwXxkAAAGQlsLtZgAAAZC6z3nmVgAAs3VybjpsaTplbnRlcnByaXNlQXV0aFRva2VuOmVKeGpaQUFDOXNkaU0wRTA1OC9VeDJCNjM2NUtSaEJEVFBTZ0twakJkNmJ5UFFNTEFNVXNDVGc9XnVybjpsaTplbnRlcnByaXNlUHJvZmlsZToodXJuOmxpOmVudGVycHJpc2VBY2NvdW50OjEzMjMyMjk2OSwxNjczMzk0OTEpXnVybjpsaTptZW1iZXI6Nzc2MTQwMzAxxnlrEJm3oxzAS9pkj3-K06Lhwu9xaDutL3kZGegiGku3nD9KQBXhyK8krVtGo-bvdDelYfxZSFU3EqF_PKspNQmzsrvSzbGD-44D6sv-DdRAyoWr3DwCeFwokA1pVpdSE6JtTjoPM_NfKqtNKqlm99xVgC9utucjKlG0ICqGuyaBflJnZFxJmPVYGJfrQ_1LLUd0TQ'
}

# Replace these with the headers captured from HTTP Toolkit
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    # Add other headers as necessary
}

# Session setup
session = requests.Session()
session.headers.update(headers)
for name, value in cookies.items():
    session.cookies.set(name, value)

# Verify login by requesting the LinkedIn feed
response = session.get("https://www.linkedin.com/feed/")
print("Login Verification Status Code:", response.status_code)

# Check and print all cookies to find CSRF token
print("Session Cookies:")
for cookie in session.cookies:
    print(cookie)

# Attempt to get CSRF token from known cookie names
csrf_token = session.cookies.get("JSESSIONID")
if csrf_token:
    csrf_token = csrf_token.strip('"')
else:
    # Check if CSRF token is embedded in the HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_meta_tag = soup.find('meta', {'name': 'csrf-token'})
    if csrf_meta_tag:
        csrf_token = csrf_meta_tag['content']
    else:
        csrf_token = session.cookies.get("ajax:3449190675516434369")

if csrf_token:
    print("CSRF Token Found:", csrf_token)
    session.headers.update({
        "x-restli-protocol-version": "2.0.0",
        "Content-Type": "application/json"
    })

# Step 1: Post Job Details
job_post_data = {
    "jobTitle": "Software Engineer",
    "company": "Persist Ventures",
    "workplaceType": "Remote",
    "employeeLocation": "Mumbai, Maharashtra, India",
    "jobType": "Full-time",
}

job_post_url = "https://linkedin.sc.omtrdc.net/b/ss/lnkdprod/10/JS-2.20.0/s7325585209947"
response = session.post(job_post_url, json=job_post_data)

if response.status_code == 200 or response.status_code == 201:
    print("Job posted successfully!")
else:
    print(f"Failed to post job: {response.status_code}")
    print(response.text)

# Step 2: Move to the Next Page and Post Job Description
description_data = {
    "description": "The ideal candidate will be responsible for developing high-quality applications...",
    "responsibilities": "Develop quality software and web applications...",
    "qualifications": "Bachelor's degree or equivalent experience...",
}

description_url = "https://linkedin.sc.omtrdc.net/b/ss/lnkdprod/10/JS-2.20.0/s72017443906772"
response = session.post(description_url, json=description_data)

if response.status_code == 200 or response.status_code == 201:
    print("Job description posted successfully!")
else:
    print(f"Failed to post job description: {response.status_code}")
    print(response.text)

# Step 3: Move to the Qualification Settings Page and Submit
#Provide the Organization email id for verification code
qualification_data = {
    "qualificationSettings": {
        "filterOutRejections": True,
        "rejectionMessage": "Thank you for your interest in the Software Engineer position at Publicis Sapient France in Gurugram, Haryana, India. Unfortunately, Publicis Sapient France did not select your application to move forward in the hiring process. Regards, Publicis Sapient France"
    },
}

qualification_url = "https://www.linkedin.com/voyager/api/jobQualificationEndpoint"
response = session.post(qualification_url, json=qualification_data)

if response.status_code == 200 or response.status_code == 201:
    print("Qualification settings posted successfully!")
else:
    print(f"Failed to post qualification settings: {response.status_code}")
    print(response.text)
