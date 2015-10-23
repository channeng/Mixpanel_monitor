from trend_30d_analysis import Mixpanel_Events_monitor
import os

api_key = os.environ["MP_DESKTOP_KEY"]
api_secret = os.environ["MP_DESKTOP_SECRET"]
monitor = Mixpanel_Events_monitor(api_key,api_secret)
for i in  monitor.get_all_events():
  print i
  