# 🔐 Blind SQL injection with conditional errors

This script is designed to test for basic SQL injection vulnerabilities in labs from PortSwigger's Web Security Academy Lab: [Blind SQL injection with conditional errors](https://portswigger.net/web-security/learning-paths/sql-injection/sql-injection-error-based-sql-injection/sql-injection/blind/lab-conditional-errors#). It targets endpoints like `/filter?category=` and checks whether a given payload successfully bypasses input validation.

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
python3 blindSqlErrorConditionalTriggers.py https://0a21005d04913d328096dfa500310055.web-security-academy.net 
```

### ✅ Sample Output

```
(+) Targeting: https://0a21005d04913d328096dfa500310055.web-security-academy.net

(+) Fetching initial TrackingId cookie...
(✓) Found TrackingId: npCqAHYA0tN7LYtS

(+) Determining administrator password length...

    ➤ Testing length: 20
(✓) Administrator password is 20 characters long.

(+) Extracting administrator password...

(✓) Successfully extracted administrator password.

(+) Administrator Password: f9ppxf9khmwr9ve611gv
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
