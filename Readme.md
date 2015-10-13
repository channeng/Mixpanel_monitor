# Mixpanel Monitor

Monitor and perform analysis on all events within Mixpanel. 

## Modules
Currently, there is only 1 module in this package.
### **Events_analysis**
For each event in Mixpanel Segmentation, provides the following data:
* Daily Avg (Last 7 days)
* Daily Avg (Prior 7 days)
* Daily Avg (Last 30 days)
* Regress_coeff (30d) - Positive = upward trend, Negative = downward trend
* **Output**: trend_analysis.csv

## Install
To run the module, install all packages given in requirements.txt
* Run the following command: `pip install -r requirements.txt`

Also, set your environment variables:
* Mixpanel API key: `export MP_KEY=<your_mixpanel_api_key>`
* Mixpanel API secret: `export MP_KEY=<your_mixpanel_api_secret>`

## Executing Script
After installing the necessary packages, execute the script with the following command: `python -m mp.events_analysis.trend_30d_analysis`
