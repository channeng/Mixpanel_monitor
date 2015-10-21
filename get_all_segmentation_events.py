from trend_30d_analysis import Mixpanel_Events_monitor
import os

api_key = os.environ["MP_PRO_KEY"]
api_secret = os.environ["MP_PRO_SECRET"]
monitor = Mixpanel_Events_monitor(api_key,api_secret)
print monitor.get_all_events()
  