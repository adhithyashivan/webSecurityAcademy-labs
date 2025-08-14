# 🔐 SQL Injection Tester – Web Security Academy Lab

This script is designed to test for basic SQL injection vulnerabilities in labs from PortSwigger's Web Security Academy Lab: [SQL injection vulnerability using UNION to identify count of columns returned by query](https://portswigger.net/web-security/learning-paths/sql-injection/sql-injection-determining-the-number-of-columns-required/sql-injection/union-attacks/lab-determine-number-of-columns#). It targets endpoints like `/filter?category=` and checks whether a given payload successfully bypasses input validation.

---

## 🚀 How It Works

The script performs the following steps:

1. **Disables SSL warnings** to avoid certificate issues with lab URLs.
2. **Sets up a proxy** (default: `127.0.0.1:8080`) for interception via tools like Burp Suite.
3. **Accepts two arguments**:
   - `url`: The base URL of the lab.
   - `payload`: The SQL injection payload to test.
4. **Constructs the full request URL** by appending the payload to `/filter?category=`.
5. **Sends the request** and checks the response for a known keyword (e.g., `"Congratulations, you solved the lab!"`).
6. **Prints the result** indicating whether the injection was successful.

---

## 🧪 Sample Usage

```bash
python3 unionColumnCount.py https://0a82001304b6eb4f81be4d4b003300ed.web-security-academy.net "' UNION SELECT NULL, NULL, NULL--"
```

### ✅ Sample Output

```
(+) Targeting: https://0a82001304b6eb4f81be4d4b003300ed.web-security-academy.net
(+) Endpoint: /filter?category=
(+) Testing payload: ' UNION SELECT NULL, NULL, NULL--
(+) Encoded payload: %27+UNION+SELECT+NULL%2C+NULL%2C+NULL--
(+) Full request URL: https://0a82001304b6eb4f81be4d4b003300ed.web-security-academy.net/filter?category=%27+UNION+SELECT+NULL%2C+NULL%2C+NULL--


[+] SQL injection successful!
```

---

## 📌 Lab-Specific Note

For this particular lab, the script checks whether the response contains the word `"Congratulations, you solved the lab!"` to determine success. You can modify this keyword in the code to match other labs or contexts.

---

## 📦 Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

## 📦 Walkthrough of the code
[Code Walkthrough](https://medium.com/@adhithyasivanesh/portswigger-web-security-academy-labs-sqli-lab-1-retrieving-hidden-data-fe40ea356d5d)

