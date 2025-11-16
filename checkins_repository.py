from datetime import timedelta, datetime
# from llm_service import summarize_insight
from models import GenerateInsightsRequest
from obtain_timezone import getTimeZone
from setup import SUPABASE
import calendar
from numerical_calculations import calculations
import calendar
from zoneinfo import ZoneInfo

 
def lol(user_id, user_timezone):
    user_type = check_which_user(user_id)
    
    if user_type == "new_user":    
        print("\n\n\nnew user")
        SUPABASE.table("users").insert({"user_id": user_id,"timezone_user": user_timezone}).execute()  
 
def to_manila_datetime(created_at_str: str) -> datetime:
    """Convert UTC timestamp string to Asia/Manila datetime."""
    # Ensure we replace Z with +00:00 for ISO parsing
    created_at_utc = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
    return created_at_utc.astimezone("Asia/Manila")
 
def check_which_user(user_id: str, user_timezone: str, request: GenerateInsightsRequest) -> str:
    """Check if the user is new, new with check-in, or existing."""
    response = SUPABASE.table("mood_checkIns").select("*").eq("user_id", user_id).order("created_at", desc=False).limit(10).execute()
    
    if (len(response.data) == 0):
         new_user_data = {
            "user_id": user_id,
            "feelings": request.feelings,
            "avoided_emotion": request.emotionalIntelligenceQuestion,
            "mirror_question": request.mirrorQuestion,
            "energy_value": request.energy_value
            }
         try:
             SUPABASE.table("mood_checkIns").insert(new_user_data).execute()
             print("new user data inserted successfully.")
         except Exception as e:
             print(f"Failed to insert new user data: {e}")
             return "Failed to insert new user data: {e}"
         
         user_data = {
            "user_id": user_id,
            "timezone_user": user_timezone,
            }
         try:
             SUPABASE.table("users").insert(user_data).execute()
             print("data inserted successfully to user db.")
         except Exception as e:
             print(f"Failed to insert new user data: {e}")
             return "Failed to insert data to user db: {e}"
          
         return "new_user"
    else:
        return "existing_user"

 #for new user
def is_new_user(user_id: str) -> bool:
    """Return True if the user is new (1 previous check-ins)."""
    response = SUPABASE.table("mood_checkIns").select("*").eq("user_id", user_id).order("created_at", desc=False).limit(10).execute()
    
    if (len(response.data) > 0):
        return False
    
    return True  

def is_new_user_with_checkin(user_id: str) -> bool:
    """Return True if the user is new (1 previous check-ins)."""
    response = SUPABASE.table("mood_checkIns").select("*").eq("user_id", user_id).order("created_at", desc=False).limit(10).execute()
    
    if (len(response.data) > 1):
        return False
    
    return True  




def get_days_since_last_checkin(user_id: str, timezone: str) -> int:
    """
    Calculate the number of days between the user's most recent check-in 
    and the current date in the specified timezone.

    Args:
        user_id (str): The ID of the user whose check-in history to query.
        timezone (str): The IANA timezone string (e.g., "Asia/Manila").

    Returns:
        int: The number of full days since the last check-in.
             Returns 0 if the last check-in was today.
    """
    response = (
        SUPABASE.table("mood_checkIns")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )

    # timezone = "Asia/Manila"  # ⚠️ Consider removing hardcoding if you really want to use the function arg
    _get_Timezone = getTimeZone(timezone)

    last_checkin_date = response.data[0]
    created_at_str = last_checkin_date['created_at']

    created_at = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
    created_at_date = created_at.date()
    current_date = _get_Timezone.current_date

    diff_days = (current_date - created_at_date).days
    return diff_days
        
        
        


def has_previous_checkins(user_id: str) -> bool:
    """Return True if the user has at least one previous check-in."""
    response = SUPABASE.table("mood_checkIns").select("*").eq("user_id", user_id).execute()
    has_previous_checkins = len(response.data) > 0
    return has_previous_checkins 

def query(user_id: str):
    response = (
        SUPABASE.table("")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=False)
        .execute()
    )
    
    return response.data
    

def obtain_previous_checkins_of_the_current_day(user_id: str, user_timezone: str):
    """Return the previous check-ins of the current day for the user"""
    
    _get_Timezone = getTimeZone(user_timezone)
    now = _get_Timezone.current_date
    
    # Query all yesterday's data
    start_datetime = f"{now.isoformat()}T00:00:00+00"
    end_datetime = f"{now.isoformat()}T23:59:59+00"
    
    # Fetch all check-ins for the previous day
    response = (
        SUPABASE.table("mood_checkIns")
        .select("*")
        .eq("user_id", user_id)
        .gte("created_at", start_datetime)
        .lte("created_at", end_datetime)
        .execute()
    )
     
    if not response.data:
        print(f"No previous day's check-ins found for user {user_id}.")
        return []
    
    return response.data
    


def obtain_previous_checkins_of_the_current_week(user_id: str, user_timezone: str):
    """Return the previous check-ins of the current week for the user."""
    
    print("pre user timezone: ", user_timezone)
    _user_timezone = getTimeZone(user_timezone) 
    
    print("_user_timezone: ", _user_timezone)
    current_date = _user_timezone.current_date  
    
    print("current date: ", current_date)
    
    start_of_week = current_date - timedelta(days=current_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)      
    
    # Use proper datetime boundaries 
    start_datetime = f"{start_of_week.isoformat()}T00:00:00+00" 
    end_datetime = f"{end_of_week.isoformat()}T23:59:59+00"
    
    print("start datetime: ", start_datetime)
    print("end datetime: ", end_datetime)
    
    # response = (
    #     SUPABASE.table("mood_checkIns")
    #     .select("*")
    #     .eq("user_id", user_id)
    #     .gte("created_at", start_datetime)
    #     .lte("created_at", end_datetime)
    #     .order("created_at", desc=False)
    #     .execute()
    # )
    try:
        print("obtaining current week's check-ins")
        response = (
            SUPABASE.table("daily_summaries")
            .select("*")
            .eq("user_id", user_id)
            .gte("checkin_day", start_of_week.isoformat())
            .lte("checkin_day", end_of_week.isoformat())
            .order("checkin_day", desc=False)
            .execute()
        )
        if not response.data:
            print("No check-ins found for the current week.")
        
        print("current week's check-ins: ", response.data)
        return response.data
        
    except Exception as e:
      print(f"❌ Error fetching current week's check-ins: {e}")
      return f"❌ Error fetching current week's check-ins: {e}"
    

def obtain_previous_checkins_of_the_previous_week(user_id: str, user_timezone: str):
    """Return the previous check-ins of the previous for the user."""
    _user_timezone = getTimeZone(user_timezone) 
    current_date = _user_timezone.current_date
    
    
    
    # obtain current monday of the week
    current_week_monday = current_date - timedelta(days=current_date.weekday())
    
    start_of_week = current_week_monday - timedelta(days=7)
    end_of_week = start_of_week + timedelta(days=6)     
    
    # Use proper datetime boundarie
    start_datetime = f"{start_of_week.isoformat()}T00:00:00+00" 
    end_datetime = f"{end_of_week.isoformat()}T23:59:59+00"    
    
    try:
        print("obtianing previous week summaries")
        response = (
            SUPABASE.table("daily_summaries")
            .select("*")
            .eq("user_id", user_id)
            .gte("checkin_day", start_of_week.isoformat())
            .lte("checkin_day", end_of_week.isoformat())
            .order("checkin_day", desc=False)
            .execute()
        )
        if not response.data:
            print(f"No previous week's check-ins found for user {user_id}.")
    
        print("current week's check-ins: ", response.data)
        return response.data
    except Exception as e:
        print(f"❌ Error fetching previous week's check-ins: {e}")
        return f"❌ Error fetching previous week's check-ins: {e}"
    
   



    
def get_monthly_summaries(user_id: str):
    """Fetch all monthly summaries for the given user."""
    try:
        print("obtianing monthly summaries")
        response = (
            SUPABASE.table("monthly_summaries")
            .select("*")
            .eq("user_id", user_id)
            .order("year", desc=True)
            .order("month", desc=True)
            .execute()
        )

        summaries = response.data
        
        if not summaries:
            print(f"No monthly summaries found for user {user_id}.")

        return summaries
        # if not summaries or len(summaries) == 0:
        #     print(f"No monthly summaries found for user {user_id}.")
        #     return []

        # print(f"✅ Retrieved {len(summaries)} monthly summaries for user {user_id}.")
        # return summaries

    except Exception as e:
        print(f"❌ Error fetching monthly summaries: {e}")

        return f"❌ Error fetching monthly summaries: {e}"




def obtain_previous_checkins_of_previous_months(user_id: str, user_timezone: str):
    """Return check-ins for the current month, organized by weeks (Monday-Sunday)."""
    
    _user_timezone = getTimeZone(user_timezone)
    current_date = _user_timezone.current_date
    
    # check current month -> check current date -> if current date >= 10 days of the month obtain only this month -> else obtain last month
    # Get all check-ins for the entire month
    start_of_month = current_date.replace(day=1)
    last_day = calendar.monthrange(current_date.year, current_date.month)[1]
    end_of_month = current_date.replace(day=last_day)
     
    # Query all month's data
    start_datetime = f"{start_of_month.isoformat()}T00:00:00+00"
    end_datetime = f"{end_of_month.isoformat()}T23:59:59+00"
    
    response = (
        SUPABASE.table("mood_checkIns")
        .select("*")
        .eq("user_id", user_id)
        .gte("created_at", start_datetime)
        .lte("created_at", end_datetime)
        .order("created_at", desc=False)
        .execute()
    )
    
    weekly_checkins = {}
    checkins = {}    
    # checkins["week_1"] = response.data
    
    number_of_checkins = len(response.data)
    # return checkins 
    # return {"start" : start_datetime, 
    #         "end": end_datetime}
    
    if number_of_checkins >= 10:
        # checkins = checkins.append(number_of_checkins)
        pass
    else:
        # Get first day of previous month
        first_of_current = current_date.replace(day=1)
        start_of_month = (first_of_current - timedelta(days=1)).replace(day=1)

        # Get last day of previous month  
        end_of_month = first_of_current - timedelta(days=1)

        # Query all month's data
        start_datetime = f"{start_of_month.isoformat()}T00:00:00+00"
        end_datetime = f"{end_of_month.isoformat()}T23:59:59+00"
                
        response = (
            SUPABASE.table("mood_checkIns")
            .select("*")
            .eq("user_id", user_id)
            .gte("created_at", start_datetime)
            .lte("created_at", end_datetime)
            .order("created_at", desc=False)
            .execute()
        )
        
        checkins = checkins.append(response.data)
        print(checkins)
    return response.data