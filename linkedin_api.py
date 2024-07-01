import requests
import json

# Replace these with your actual values
CLIENT_ID = '864u3xo2xoq5ll'
CLIENT_SECRET = 'ucimFx9yqfszjcnM'
REDIRECT_URI = 'https://www.linkedin.com/developers/tools/oauth/redirect'
AUTHORIZATION_CODE = 'https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=864u3xo2xoq5ll&redirect_uri=https://www.linkedin.com/developers/tools/oauth/redirect&scope=r_liteprofile%20r_emailaddress%20w_member_social%20openid'  # Replace with the captured authorization code
ACCESS_TOKEN ='AQXJ1PKcxtys3jslnqZsc_gDuvdq2JwlWggJEzRnHS_OYuAsBcmeZxykdZ18TSsFgRz0oaqAp9uC4BSDjNU2piXiugOqFxd5qOSLKA7crrm7BStxd_je_39VnctTQYhbk6jCoBSOSlHNfRX06X3OnXPRJTPeIQUqmPaqfR5yd0Mqy5J6Q9NbJfByVWc5hA_g0cy2ELK4mZBDrE9UEhzpVF8JQaA6C36f5DcFHmEl3m_IwGvKD-KmWh-xkTl7tHp5GFbqKI8uX9_fmrrz0YyMFCbuQ8gNlBHSoi-VrH0EMLHsryxVtinKt9JnKpEvvg4C-x2D4k9GW1Z7Tdj92Ct9hPCgMUhCMQ'

# Function to exchange authorization code for access token
def get_access_token(auth_code):
    url = 'https://www.linkedin.com/developers/apps/218669837/auth'
    payload = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    try:
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()  # Raise exception for bad response status
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response status code: {response.status_code}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    return None

# Function to get user profile
def get_user_profile(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    url = 'https://api.linkedin.com/v2/me'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error getting user profile: {response.status_code}")
        print(response.json())
        return None

# Function to get user email address
def get_user_email(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    url = 'https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error getting user email: {response.status_code}")
        print(response.json())
        return None

# Function to post an update
def post_update(token, user_urn, message):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    data = {
        "author": user_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": message
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    response = requests.post('https://api.linkedin.com/v2/ugcPosts', headers=headers, data=json.dumps(data))
    if response.status_code == 201:
        return response.json()
    else:
        print(f"Error posting update: {response.status_code}")
        print(response.json())
        return None

# Example usage
if __name__ == '__main__':
    # Step 1: Get the authorization code by directing the user to:
    # https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI&scope=r_liteprofile%20r_emailaddress%20w_member_social%20openid

    # Step 2: Exchange the authorization code for an access token
    token_response = get_access_token(AUTHORIZATION_CODE)
    if token_response and 'access_token' in token_response:
        ACCESS_TOKEN = token_response['access_token']
        print(f"Access Token: {ACCESS_TOKEN}")

        # Step 3: Use the access token to get the user profile
        profile = get_user_profile(ACCESS_TOKEN)
        if profile:
            print(f"User Profile: {profile}")
            user_urn = f"urn:li:person:{profile['id']}"  # Correctly format the user URN

            # Step 4: Use the access token to get the user's email address
            email = get_user_email(ACCESS_TOKEN)
            if email:
                print(f"User Email: {email}")

            # Step 5: Post an update
            message = "Hello, LinkedIn! This is a test update."
            update_response = post_update(ACCESS_TOKEN, user_urn, message)
            if update_response:
                print(f"Update Response: {update_response}")
    else:
        print("Failed to obtain access token")


