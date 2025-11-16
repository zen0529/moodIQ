from datetime import datetime
from zoneinfo import ZoneInfo
import calendar
from models import timezoneData

def getTimeZone(user_timezone: str) -> timezoneData:
    
    # Get current date and time in user's timezone
    tz = ZoneInfo(user_timezone)
    now = datetime.now(tz)
    current_year = now.year
    current_month = now.month
    
    return timezoneData(
        current_date = now.date(),        # e.g. 2025-09-19
        current_time = now.time(),       # e.g. 23:56:41.123456
        current_day = now.strftime("%A"), #
        current_year = now.year,
        current_month = now.month,
        days_in_month = calendar.monthrange(current_year, current_month)[1]
    )
   
    