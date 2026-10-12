import os
import requests
import json
import subprocess

from user_input import ask_number, ask_text, ask_choice


def run_sf(command):
    result = subprocess.run(["sf", *command, "--json"], capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return json.loads(result.stdout).get("result")


def get_saved_orgs():
    result = run_sf(["org", "list"]) or {}
    orgs = {}
    for group in ("nonScratchOrgs", "sandboxes", "other"):
        for org in result.get(group, []):
            orgs[org["username"]] = org.get("alias") or org["username"]
    return orgs   # {username: alias}


def get_token(target_org):
    data = run_sf(["org", "display", "--target-org", target_org])
    if data is None or "accessToken" not in data:
        return None
    return data["accessToken"], data["instanceUrl"]


def browser_login():
    alias = ask_text("Short name for this client's org (e.g. acme): ")
    org_type = ask_choice("Production or Sandbox (P/S) [P]: ", ["p", "s"], "p")
    url = "https://test.salesforce.com" if org_type == "s" else "https://login.salesforce.com"

    print("Opening browser to log in to Salesforce...")
    if run_sf(["org", "login", "web", "--alias", alias, "--instance-url", url]) is None:
        raise RuntimeError("Salesforce login failed.")
    return alias


def authenticate():
    orgs = get_saved_orgs()
    usernames = list(orgs)

    print("\nSalesforce orgs:")
    for number, username in enumerate(usernames, start=1):
        print(f"  {number}: {orgs[username]} ({username})")
    new_login_number = len(usernames) + 1
    print(f"  {new_login_number}: Log in to a new org")

    choice = ask_number("Choose an org: ", 1, new_login_number)
    target_org = browser_login() if choice == new_login_number else usernames[choice - 1]

    login = get_token(target_org)
    if login is None:
        # Saved login no longer works (password change, revoked session): log in again.
        print("That saved login has expired.")
        target_org = browser_login()
        login = get_token(target_org)
        if login is None:
            raise RuntimeError("Salesforce login failed.")

    print("Authentication Successful")
    return login


"""
def authenticate():
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
"""