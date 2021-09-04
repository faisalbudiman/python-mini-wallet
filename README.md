# ewallet
This web api is using framework Flask from python and database using MySQL

## What Inside this project
This project result are based on [Mini Wallet Exersice](https://documenter.getpostman.com/view/8411283/SVfMSqA3?version=latest). The endpoint, header/body request, and responses are same as that instruction.

## Installation instructions
1. Make sure you have python > 3.7 Installed on your machine. [Download Python](https://www.python.org/downloads/).
2. Clone this repo using command on your terminal `git clone https://github.com/faisalbudiman/python-mini-wallet.git` 
3. Copy `.env.example` to `.env`, and fill the value of the variable, (fill JWT_SECRET_KEY and DATABASE_URI_DEV value. example: Since I use mysql database for this project, so fill the DATABASE_URI_DEV value with `mysql+pymysql://<username>:<password>@localhost/ewallet_dev`. Also dont forget to create database with the name ewallet_dev.
4. Run command on your terminal `pip install pipenv` if you dont have install pipenv yet.
5. Run command `pipenv shell` to activate the virtual environment.
6. Run command `pip install -r requirements.txt` to install modules.
7. Set variable FLASK_ENV to development. Run command on terminal `export FLASK_ENV=development`, if you are using Windows use command `set FLASK_ENV=development`
8. Set variable CONFIG_SETTING to config.Devconfig . Run command on terminal `export CONFIG_SETTING=config.DevConfig`, if you are using Windows use command `set CONFIG_SETTING=config.DevConfig`
9. Run migration for database using command `make migrate_dev`.
10. To run application, use command `flask run`.
