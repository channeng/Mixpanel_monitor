# Run script by going to root and run command: cd ~/Mixpanel_monitor && python -m mp.events_analysis.trend_30d_analysis
from ..mixpanel_wrapper import Mixpanel
from ..dropbox_wrapper import Dropbox
import datetime
from sys import stdout
import os
import pandas as pd
from pandas.stats.api import ols
# import statsmodels.formula.api as sm 
import dateutil.parser

class Mixpanel_Events_monitor(object):
  def __init__(self,api_key,api_secret):
    self.api = Mixpanel(api_key,api_secret)

  def get_all_events(self):
    all_events = self.api.request(['events','names'], {
      'type' : "unique"
    })
    return all_events

  def get_trend_data(self):
    all_events = self.get_all_events()
    from_date = datetime.date.today()-datetime.timedelta(30)
    to_date = datetime.date.today()-datetime.timedelta(1)
    count_all_events = len(all_events)
    trend_data = {}
#     i = 0
    for event in all_events:
      event_data = self.api.request(['segmentation'], {
          'event' : event,
          'from_date' : str(from_date),
          'to_date' : str(to_date),
          'unit': 'day',
          'type' : "unique",
        })
      trend_data[event] = event_data['data']['values'][event]
      # Print counter
#       i += 1
#       stdout.write("\r%d / %s events retrieved" %(i,count_all_events))
#       stdout.flush()
#     stdout.write("\n")
    return trend_data

  # CONVERT DATA TO CSV
  def trend_data_to_csv(self):
    trend_data = self.get_trend_data()
    import csv
    # Create header line
    header_line = ["Date"] + trend_data.keys()
    # Create unique keys.
    rows = list(set([date for event in trend_data.values() for date in event.keys()]))
    # Create rows
    table = [header_line]+[[unique_date]+[trend_data[event].get(unique_date, '-') for event in header_line[1:]] for unique_date in rows]
    with open('trend_data.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for row in table:
            writer.writerow(row)
  
  # GET DATAFRAMES          
  def csv_to_pandas(self):
    # csv file must be located in root
    trend_dataframe = pd.read_csv("trend_data.csv",index_col=0)
    trend_dataframe.index = pd.to_datetime(trend_dataframe.index)
    trend_dataframe.index.name = 'Date'
    return trend_dataframe
  
  def data_to_pandas(self):
    trend_dataframe = pd.DataFrame.from_dict(self.get_trend_data())
    trend_dataframe.index = pd.to_datetime(trend_dataframe.index)
    trend_dataframe.index.name = 'Date'
    return trend_dataframe
  
  def trend_analysis_df(self,trend_dataframe):
    # Define date variables
    date_today = datetime.date.today()
    date_7d_ago = date_today - datetime.timedelta(7)
    date_8d_ago = date_today - datetime.timedelta(8)
    date_14d_ago = date_today - datetime.timedelta(14)
    # Setting up view for regression
    trend_df_last_7d = trend_dataframe.ix[str(date_7d_ago):str(date_today)]
    trend_df_prior_7d = trend_dataframe.ix[str(date_14d_ago):str(date_8d_ago)]
    # Get timeseries means
    trend_series_last7d_mean = pd.Series(trend_df_last_7d.mean(), name='Daily Avg (Last week)')
    trend_series_prior7d_mean = pd.Series(trend_df_prior_7d.mean(), name='Daily Avg (Prior week)')
    trend_series_last30d_mean = pd.Series(trend_dataframe.mean(), name='Daily Avg (Last 30 days)')
    # Get Regression Coeffs
    trend_series_30d_regress_coeff = pd.Series(name='Regress_coeff (30d)')
    for i in trend_dataframe:
      # Conduct Regression for each event
      t_series = pd.Series(trend_dataframe[i],index=trend_dataframe.index).sort_index()
      s_series = pd.Series(t_series.values)
      s_reset_as_df = s_series.reset_index()
      s_coeff = ols(x=s_reset_as_df["index"] ,y=s_reset_as_df[0]).beta['x'] # Gets the regression coeff
      trend_series_30d_regress_coeff = trend_series_30d_regress_coeff.set_value(i,s_coeff)
    # Create Trend Analysis Dataframe
    trend_analysis_df = pd.concat([trend_series_last7d_mean,trend_series_prior7d_mean,trend_series_last30d_mean,trend_series_30d_regress_coeff],axis=1)
    trend_analysis_df.index.name = "Events"
    return trend_analysis_df
    
  def trend_analysis_csv(self,trend_dataframe):
    # Output to CSV
    trend_analysis_df = self.trend_analysis_df(trend_dataframe)
    file_name = "Trend_analysis_"+str(datetime.date.today())+".csv"
    trend_analysis_df.to_csv(file_name)

if __name__ == '__main__':
  # 1) INITIALIZE MIXPANEL_EVENTS_MONITOR INSTANCE 
  api_key = os.environ["MP_PRO_KEY"]
  api_secret = os.environ["MP_PRO_SECRET"]
  monitor = Mixpanel_Events_monitor(api_key,api_secret)
  
  # 2) CREATE TREND_DATAFRAME FOR ANALYSIS WITH PANDAS - 2 options to do so
  
  # OPTION (A)
#   # PART 1: Download TREND_DATA to root as csv file
#   monitor.trend_data_to_csv()
#   # PART 2: Create trend dataframe from csv file in root
#   trend_dataframe = monitor.csv_to_pandas()

#   # OPTION (B)
#   # Create trend dataframe straight from Mixpanel API
  trend_dataframe = monitor.data_to_pandas()
  
  # 3) GENERATE TREND_ANALYSIS AS CSV
  monitor.trend_analysis_csv(trend_dataframe)
  
  # 4) Automated file upload to dropbox
  dropbox_token = os.environ["DROPBOX_TOKEN"]
  file_name = "Trend_analysis_"+str(datetime.date.today())+".csv"
  upload_path_in_dropbox = os.environ["UPLOAD_PATH"]+"MP_Events_Report/"
    # Initialize dropbox instance, upload to dropbox, and delete original
  DB = Dropbox(dropbox_token,file_name,upload_path_in_dropbox)
  DB.upload_to_dropbox()
  DB.delete_original()

#   # OTHER FUNCTIONS
#   # Print all events
#   all_events = monitor.get_all_events()
#   for event in all_events:
#     print event
  
#   # Print trend data
#   trend_data = monitor.get_trend_data()
#   print trend_data