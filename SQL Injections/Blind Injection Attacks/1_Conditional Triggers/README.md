# 🔐 Blind SQL injection with conditional responses

This script is designed to test for basic SQL injection vulnerabilities in labs from PortSwigger's Web Security Academy Lab: [Blind SQL injection with conditional responses](https://portswigger.net/web-security/learning-paths/sql-injection/sql-injection-exploiting-blind-sql-injection-by-triggering-conditional-responses/sql-injection/blind/lab-conditional-responses#). It targets endpoints like `/filter?category=` and checks whether a given payload successfully bypasses input validation.

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
python3 blindSqlConditionalTriggers.py https://0a8900dd03da2aa5801e12f300fd00e3.web-security-academy.net 
```

### ✅ Sample Output

```
(+) Targeting: https://0a8900dd03da2aa5801e12f300fd00e3.web-security-academy.net

(+) Fetching initial TrackingId cookie...
(✓) Found TrackingId: 2bSclk2MUxX1dlFk

(+) Determining administrator password length...

    ➤ Testing length: 20
(✓) Administrator password is 20 characters long.

(+) Extracting administrator password...

(✓) Successfully extracted administrator password.

(+) Administrator Password: 1gv32tsd08x7gvpz4yio
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

## Sample HTML response which was scrapped (Output with welcome back line)

```HTML
HTTP/2 200 OK
Content-Type: text/html; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 11496

<!DOCTYPE html>
<html>
    <head>
        <link href=/resources/labheader/css/academyLabHeader.css rel=stylesheet>
        <link href=/resources/css/labsEcommerce.css rel=stylesheet>
        <title>Blind SQL injection with conditional responses</title>
    </head>
    <body>
        <script src="/resources/labheader/js/labHeader.js"></script>
        <div id="academyLabHeader">
            <section class='academyLabBanner'>
                <div class=container>
                    <div class=logo></div>
                        <div class=title-container>
                            <h2>Blind SQL injection with conditional responses</h2>
                            <a class=link-back href='https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses'>
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
                <div class="container">
                    <header class="navigation-header">
                        <section class="top-links">
                            <a href=/>Home</a><p>|</p>
                            <div>Welcome back!</div><p>|</p>
                            <a href="/my-account">My account</a><p>|</p>
                        </section>
                    </header>
                    <header class="notification-header">
                    </header>
                    <section class="ecoms-pageheader">
                        <img src="/resources/images/shop.svg">
                    </section>
                    <section class="search-filters">
                        <label>Refine your search:</label>
                        <a class="filter-category selected" href="/">All</a>
                        <a class="filter-category" href="/filter?category=Accessories">Accessories</a>
                        <a class="filter-category" href="/filter?category=Clothing%2c+shoes+and+accessories">Clothing, shoes and accessories</a>
                        <a class="filter-category" href="/filter?category=Corporate+gifts">Corporate gifts</a>
                        <a class="filter-category" href="/filter?category=Gifts">Gifts</a>
                        <a class="filter-category" href="/filter?category=Toys+%26+Games">Toys & Games</a>
                    </section>
                    <section class="container-list-tiles">
                        <div>
                            <img src="/image/productcatalog/products/45.jpg">
                            <h3>ZZZZZZ Bed - Your New Home Office</h3>
                            <img src="/resources/images/rating2.png">
                            $92.03
                            <a class="button" href="/product?productId=4">View details</a>
                        </div>
                        <div>
                            <img src="/image/productcatalog/products/5.jpg">
                            <h3>Cheshire Cat Grin</h3>
                            <img src="/resources/images/rating5.png">
                            $39.06
                            <a class="button" href="/product?productId=9">View details</a>
                        </div>
                        <div>
                            <img src="/image/productcatalog/products/38.jpg">
                            <h3>Six Pack Beer Belt</h3>
                            <img src="/resources/images/rating1.png">
                            $8.26
                            <a class="button" href="/product?productId=14">View details</a>
                        </div>
                        <div>
                            <img src="/image/productcatalog/products/30.jpg">
                            <h3>Giant Pillow Thing</h3>
                            <img src="/resources/images/rating3.png">
                            $7.48
                            <a class="button" href="/product?productId=19">View details</a>
                        </div>
                        <div>
                            <img src="/image/productcatalog/products/60.jpg">
                            <h3>Dancing In The Dark</h3>
                            <img src="/resources/images/rating3.png">
                            $33.45
                            <a class="button" href="/product?productId=1">View details</a>
                        </div>
                        <div>
                            <img src="/image/productcatalog/products/43.jpg">
                            <h3>First Impression Costumes</h3>
                            <img src="/resources/images/rating3.png">
                            $83.18
                            <a class="button" href="/product?productId=6">View details</a>
                        </div>
                        <div>
                            <img src="/image/productcatalog/products/24.jpg">
                            <h3>The Alternative Christmas Tree</h3>
                            <img src="/resources/images/rating5.png">
                            $59.53
                            <a class="button" href="/product?productId=11">View details</a>
                        </div>
                        <div>
                            <img src="/image/productcatalog/products/27.jpg">
                            <h3>The Trolley-ON</h3>
                            <img src="/resources/images/rating4.png">
                            $41.34
                            <a class="button" href="/product?productId=16">View details</a>
                        </div>
                        <div>
                            <img src="/image/productcatalog/products/37.jpg">
                            <h3>The Giant Enter Key</h3>
                            <img src="/resources/images/rating5.png">
                            $8.68
                            <a class="button" href="/product?productId=5">View details</a>
                        </div>
                        <div>
                            <img src="/image/productcatalog/products/58.jpg">
                            <h3>There is No &apos;I&apos; in Team</h3>
                            <img src="/resources/images/rating1.png">
                            $10.50
                            <a class="button" href="/product?productId=10">View details</a>
                        </div>
                        <div>
                            <img src="/image/productcatalog/products/8.jpg">
                            <h3>Folding Gadgets</h3>
                            <img src="/resources/images/rating3.png">
                            $54.42
                            <a class="button" href="/product?productId=15">View details</a>
                        </div>
                        <div>
                            <img src="/image/productcatalog/products/6.jpg">
                            <h3>Com-Tool</h3>
                            <img src="/resources/images/rating1.png">
                            $41.24
                            <a class="button" href="/product?productId=20">View details</a>
                        </div>
                        <div>
                            <img src="/image/productcatalog/products/53.jpg">
                            <h3>High-End Gift Wrapping</h3>
                            <img src="/resources/images/rating2.png">
                            $27.59
                            <a class="button" href="/product?productId=3">View details</a>
                        </div>
                        <div>
                            <img src="/image/productcatalog/products/31.jpg">
                            <h3>Couple&apos;s Umbrella</h3>
                            <img src="/resources/images/rating5.png">
                            $77.82
                            <a class="button" href="/product?productId=8">View details</a>
                        </div>
                        <div>
                            <img src="/image/productcatalog/products/7.jpg">
                            <h3>Conversation Controlling Lemon</h3>
                            <img src="/resources/images/rating1.png">
                            $43.86
                            <a class="button" href="/product?productId=13">View details</a>
                        </div>
                        <div>
                            <img src="/image/productcatalog/products/21.jpg">
                            <h3>Snow Delivered To Your Door</h3>
                            <img src="/resources/images/rating1.png">
                            $59.13
                            <a class="button" href="/product?productId=18">View details</a>
                        </div>
                        <div>
                            <img src="/image/productcatalog/products/63.jpg">
                            <h3>Laser Tag</h3>
                            <img src="/resources/images/rating2.png">
                            $80.09
                            <a class="button" href="/product?productId=2">View details</a>
                        </div>
                        <div>
                            <img src="/image/productcatalog/products/13.jpg">
                            <h3>Inflatable Dartboard</h3>
                            <img src="/resources/images/rating3.png">
                            $71.40
                            <a class="button" href="/product?productId=7">View details</a>
                        </div>
                        <div>
                            <img src="/image/productcatalog/products/55.jpg">
                            <h3>WTF? - The adult party game</h3>
                            <img src="/resources/images/rating4.png">
                            $7.83
                            <a class="button" href="/product?productId=12">View details</a>
                        </div>
                        <div>
                            <img src="/image/productcatalog/products/64.jpg">
                            <h3>Hexbug Battleground Tarantula Double Pack</h3>
                            <img src="/resources/images/rating2.png">
                            $36.41
                            <a class="button" href="/product?productId=17">View details</a>
                        </div>
                    </section>
                </div>
            </section>
            <div class="footer-wrapper">
            </div>
        </div>
    </body>
</html>

```