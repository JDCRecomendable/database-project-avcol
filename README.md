# Database Project for Avondale College
## About
* Sample database for logistical management of an online shop
* Provide a focused, web-based software for use in logistics

## Pre-Requisites
* Python 3
* MySQL Server 8.0.16 or higher OR MariaDB 10.2 or higher
* MySQL Connector/Python 8.0 or higher
* Flask web application framework 1.1.1
* WTForms module 2.2.1
* PyFPDF 1.7.2

## Setup
1. Install MySQL 8.0.16 and above OR MariaDB 10.2 and above.
2. Start the database server. On macOS, this can be done in System
Preferences. On GNU/Linux:
```
systemctl start mysql
# or
systemctl start mariadb
```
3. Create a schema to be used. Example:
```
mysql> CREATE SCHEMA online_shop;
```
4. Create a user for accessing the database. Example:
```
mysql> CREATE USER 'online_shop_admin'@'localhost'
    -> IDENTIFIED BY '<password>';
```
5. Grant the user privileges to the schema to be used:
```
mysql> GRANT ALL PRIVILEGES
    -> ON online_shop.*
    -> TO 'online_shop_admin'@'localhost'
    -> WITH GRANT OPTION;
```
6. Install the following Python modules for the backend:
```
pip3 install Flask==1.1.1
pip3 install WTForms==2.2.1
pip3 install mysql-connector-python
pip3 install fpdf==1.7.2
```
7. To generate the config file (`config.cfg`), execute `main.py`:
```
cd /path/to/database_package_directory/
python3 main.py
```

## Running
1. Open `config.cfg` and set up the necessary parameters as per
specifications of the database engine. Also need to set the IP
address for the web-interface:
```
[SYSTEM]
is_initialised = 0

[DATABASE]
schema = online_shop
username = online_shop_admin
password = <password>
host = 127.0.0.1

[WEB_INTERFACE]
host = 0.0.0.0
port = 5000

[LOGGER]
max_number_of_lines = 50000
```
2. Run the database engine. On macOS, this can be done in System
Preferences. On GNU/Linux:
```
systemctl start mysql
# or
systemctl start mariadb
```
3. Execute `main.py`.
4. Point any browser to the web-interface.
