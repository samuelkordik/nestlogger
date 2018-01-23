# nestlogger
Simple script to automate logging Nest thermostat temperatures.

### Installation
Install the Python Nest Library:

    [sudo] pip install python-nest

Download this script into the directory of your choosing.

Change 'sample-config.py' to 'config.py' and update it with your Nest Developer Account Credentials and WeatherUnderground API Key (See below for obtaining these API keys).

Nest Developer Account
=======================

*This is copied from the python-nest README:*

You will need a Nest developer account, and a Product on the Nest developer portal to use this module:

1. Visit `Nest Developers <https://developers.nest.com/>`_, and sign in. Create an account if you don't have one already.

2. Fill in the account details:

  - The "Company Information" can be anything.

3. Submit changes.

4. Click "`Products <https://developers.nest.com/products>`_" at top of page.

5. Click "`Create New Product <https://developers.nest.com/products/new>`_"

6. Fill in details:

  - Product name must be unique.

  - The description, users, urls can all be anything you want.

7. For permissions, check every box and if it's an option select the read/write option.

  - The description requires a specific format to be accepted.

8. Click "Create Product".

9. Once the new product page opens the "Product ID" and "Product Secret" are located on the right side. These will be used as client_id and client_secret below.

WeatherUnderground API Key
==========================

You will need a WeatherUnderground API Key (free for developer usage), which you can get here [http://www.wunderground.com/weather/api/](http://www.wunderground.com/weather/api/).

### Usage

Initially, run the script from terminal and enter your Nest Developer PIN. Once the access token is cached, you can automate this script.

Schedule this to run automatically on a Mac OS X using `launchctl`; the launch daemon plist file is included. Update it with your path and update the shell script as needed.

See the [original Reddit post](https://www.reddit.com/r/Nest/comments/56gdnu/auto_logging_inside_and_outside_temperatures_into/) for details on integrating this with IFTTT into Google Sheets. With the modifications in this script (courtesy of [u/bucketybuckbuck](https://www.reddit.com/user/bucketybuckbuck)), this data will expand into multiple rows as it is added to the sheet.

You can create a new sheet for each day by pasting the formula below into A1 of each and putting the date in column I2 (i.e. 15/11/2017 just put 15):

```=ArrayFormula(query(ImportRange("<google sheets ID from URL>","All!A1:Z1000"),"select Col1,Col3,Col4,Col5,Col6,Col7 where Col1 contains """&I2&""" "))```

This can create a chart like this:
![chart_preview](https://user-images.githubusercontent.com/3252725/32892824-17150974-ca9d-11e7-9816-541c0299b777.png)


### About
Script originally sourced from this Reddit post [Auto logging inside and outside temperatures into a spreadsheet with graphs](https://www.reddit.com/r/Nest/comments/56gdnu/auto_logging_inside_and_outside_temperatures_into/); unfortunately, Nest updated their API and the Python Nest library also has changed, so the original script did not work. This script updates for these changes.

Modifications to improve how things are logged to Google sheets and the charting instructions from [u/bucketybuckbuck](https://www.reddit.com/user/bucketybuckbuck).

Requires the Python-Nest library from here: [https://github.com/jkoelker/python-nest/blob/master/nest/nest.py](https://github.com/jkoelker/python-nest/blob/master/nest/nest.py).

