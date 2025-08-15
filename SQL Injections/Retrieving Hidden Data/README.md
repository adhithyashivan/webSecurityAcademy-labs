# 🔐 SQL injection vulnerability in WHERE clause allowing retrieval of hidden data

This script is designed to test for basic SQL injection vulnerabilities in labs from PortSwigger's Web Security Academy Lab: [SQL injection vulnerability in WHERE clause allowing retrieval of hidden data](hhttps://portswigger.net/web-security/learning-paths/sql-injection/sql-injection-retrieving-hidden-data/sql-injection/lab-retrieve-hidden-data#). It targets endpoints like `/filter?category=` and checks whether a given payload successfully bypasses input validation.

---

## 🚀 How It Works

The script performs the following steps:

1. **Disables SSL warnings** to avoid certificate issues with lab URLs.
2. **Sets up a proxy** (default: `127.0.0.1:8080`) for interception via tools like Burp Suite.
3. **Accepts two arguments**:
   - `url`: The base URL of the lab.
   - `payload`: The SQL injection payload to test.
4. **Constructs the full request URL** by appending the payload to `/filter?category=`.
5. **Sends the request** and checks the response for a known keyword (e.g., `"paintball"`).
6. **Prints the result** indicating whether the injection was successful.

---

## 🧪 Sample Usage

```bash
python3 retrieveHiddenData.py https://0a1500dd03efd63e802c7b46004200a2.web-security-academy.net "' OR 1=1--"
```

### ✅ Sample Output

```
(+) Targeting: https://0a1500dd03efd63e802c7b46004200a2.web-security-academy.net
(+) Endpoint: /filter?category=
(+) Testing payload: ' OR 1=1--
(+) Full request URL: https://0a1500dd03efd63e802c7b46004200a2.web-security-academy.net/filter?category=' OR 1=1--

[+] SQL injection successful!
```

---

## 📌 Lab-Specific Note

For this particular lab, the script checks whether the response contains the word `"paintball"` to determine success. You can modify this keyword in the code to match other labs or contexts.

---

## 📦 Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

## 📦 Walkthrough of the code
[Code Walkthrough](https://medium.com/@adhithyasivanesh/portswigger-web-security-academy-labs-sqli-lab-1-retrieving-hidden-data-fe40ea356d5d)

