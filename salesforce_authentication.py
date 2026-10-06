import os
import requests
import json
import subprocess

def authenticate():
    #Authenticates with Salesforce using the Salesforce CLI
    #Returns access_token and instance_url
    login_result = subprocess.run(
    ["sf", "org", "login", "web", "--json"],
    capture_output=True,
    text=True,
)
    if login_result.returncode != 0:
        raise RuntimeError("Salesforce login failed.")
    print("Salesforce login succeeded.")
    login_data = json.loads(login_result.stdout)
    access_token = login_data["result"]["accessToken"]
    instance_url = login_data["result"]["instanceUrl"]

    print("Authentication Successful")
    return access_token, instance_url
