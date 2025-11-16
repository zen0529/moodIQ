from datetime import datetime
import random
from numerical_calculations import calculations
# from fake_data import data
from obtain_timezone import getTimeZone
from checkins_repository import get_monthly_summaries, obtain_previous_checkins_of_the_current_day, obtain_previous_checkins_of_the_current_week, obtain_previous_checkins_of_the_previous_week, to_manila_datetime
import json

class prompts: 
        
        def __init__(self, user_id, timezone, joined_request):
                self.joined_request = joined_request
                self.user_id = user_id
                self.timezone = timezone
        # def summarize_insights(insights):
                
        # def get_energy_levels(user_id):
        #         """" Get all energy levels for all user checkins """
        #         energy_level_arr = []
        #         for d in data: #fake data only
        #                 if d['user_id'] == user_id:
        #                         # print(d)
        #                         for e in d['entries']:
        #                                 energy_level_arr.append(e['energy_level'])
        #                                 print(energy_level_arr)
        #                         break
        #         return energy_level_arr
        
        # def get_number_of_checkins(user_id):
        #         """" Get number of checkins for a user """
        #         number_of_checkins = 0
        #         for d in data: #fake data only
        #                 if d['user_id'] == user_id:
        #                         # print(d)
        #                         for e in d['entries']:
        #                                 number_of_checkins += 1
        #                                 print(number_of_checkins)
                                
        #         return number_of_checkins
        
        # def get_first_week_user_summary(self, joined_request, user_id):
        #         number_of_checkins = 0
        #         for d in data: #fake data only  
        #                 if d['user_id'] == user_id:
        #                         # print(d)
        #                         for e in d['entries']:
        #                                 number_of_checkins += 1
        #                                 print(number_of_checkins)
        
        
        def new_user_system_template(self):
                system_template_for_new_users = """
                        - Analyze all provided states, considering interplay (e.g., low energy + anxious = restorative focus).
                        - Prioritize safety and well-being; for conflicting states, address negative ones first.
                        - Draw from evidence-based practices (CBT, mindfulness, exercise science, positive psychology).
                        - Provide immediate, practical actions (not long-term therapy or medical advice).
                        - Ensure recommendations are diverse (e.g., physical, mental, social) and positive.

                        SAFETY GUIDELINES:
                        - If concerning patterns detected, include gentle resource suggestions
                        - Never provide medical or clinical diagnoses
                        - Focus on empowerment and self-awareness, not pathology
                        - For crisis indicators, prioritize immediate support resources over analysis

                        STRICT OUTPUT RULES:
                        - Respond ONLY with a valid JSON object
                        """

                return system_template_for_new_users
        
        def new_user_template(self):
                """" User template input for new users """
                user_tempate_for_new_user = f"""
                  "Today's mood check in:
                        - Enery Level (1-10): {self.joined_request.energy_value}
                        {f'- feelings: {self.joined_request.feelings}' if self.joined_request.feelings else ''}
                        {f'- Emotional Intelligence Question: {self.joined_request.emotionalIntelligenceQuestion}' if self.joined_request.emotionalIntelligenceQuestion else ''}
                        {f'- Mirror Question: {self.joined_request.mirrorQuestion}' if self.joined_request.mirrorQuestion else ''}
                """     
                
                return user_tempate_for_new_user
        
        def new_user_with_checkin_system_template():
                system_template_for_new_users = """
                        - Analyze all provided states, considering interplay (e.g., low energy + anxious = restorative focus).
                        - Prioritize safety and well-being; for conflicting states, address negative ones first.
                        - Draw from evidence-based practices (CBT, mindfulness, exercise science, positive psychology).
                        - Provide immediate, practical actions (not long-term therapy or medical advice).
                        - Ensure recommendations are diverse (e.g., physical, mental, social) and positive.

                        SAFETY GUIDELINES:
                        - If concerning patterns detected, include gentle resource suggestions
                        - Never provide medical or clinical diagnoses
                        - Focus on empowerment and self-awareness, not pathology
                        - For crisis indicators, prioritize immediate support resources over analysis

                        STRICT OUTPUT RULES:
                        - Respond ONLY with a valid JSON object
                        """

                return system_template_for_new_users
        
        
        def new_user_template(self):
                """User template input for new users."""
                jr = self.joined_request
                user_template_for_new_user = f"""
                Today's mood check-in:
                        - Energy Level (1-10): {getattr(jr, 'energy_value', 'N/A')}
                        {f'- Feelings: {jr.feelings}' if getattr(jr, 'feelings', None) else ''}
                        {f'- Emotional Intelligence Question: {jr.emotionalIntelligenceQuestion}' if getattr(jr, 'emotionalIntelligenceQuestion', None) else ''}
                        {f'- Mirror Question: {jr.mirrorQuestion}' if getattr(jr, 'mirrorQuestion', None) else ''}
                """
                return user_template_for_new_user.strip()

        
        
        def existing_user_prev_data(self, joined_request, user_id: str, number_of_days_in_this_month:int, day:str, user_timezone:str):
                # obtain energy levels from user data
                # energy_levels = [data['energyLevel'] for data in user_data]
                
                # check current date
                
                energy_level_user_data = self.get_energy_levels(user_id)
                
                # calculate numerical calculations for user data(mean, median, min, max, std_dev)
                calculations_for_user = calculations(energy_level_user_data)
                
                # count number of checkins for user
                number_of_checkins = self.get_number_of_checkins(user_id)
                
                total_number_of_prev_checkins = 14
                
                prev_day_data = f"""
                                - Enery Level (1-10): {joined_request.energy_value}
                                {f'- Energy States: {joined_request.energyStates}' if joined_request.energyStates else ''}
                                {f'- Emotional States: {joined_request.emotionalStates}' if joined_request.emotionalStates else ''}
                                {f'- Mental States: {joined_request.mentalStates}' if joined_request.mentalStates else ''}
                                {f'- Social/Relational States: {joined_request.socialOrRelationalStates}' if joined_request.socialOrRelationalStates else ''}
                                {f'- Achievement/Purpose States: {joined_request.achievementOrPurposeStates}' if joined_request.achievementOrPurposeStates else ''}
                                {f'- Emotional Intelligence Question: {joined_request.emotionalIntelligenceQuestion}' if joined_request.emotionalIntelligenceQuestion else ''}
                                {f'- Mirror Question: {joined_request.mirrorQuestion}' if joined_request.mirrorQuestion else ''}        
                                """
                
                # Check if user has 1 day of data then add a days section in the prompt with daily breakdown
                if len(number_of_checkins) == 1:
                        previous_day_text = f"""
                        Yesterday\'s mood check in:'
                        
                        {prev_day_data}
                        
                        """
                        return previous_day_text
                
                # Check if user has 2 to days of data or less than numer of days in this month
                
                elif len(number_of_checkins) >= 2 and len(number_of_checkins) < total_number_of_prev_checkins:
                        timezone=getTimeZone(user_timezone)
                        current_day = timezone.current_day
                        
                        
                        # libog anhon ang week grrrr
                        
                elif len(number_of_checkins) >= number_of_days_in_this_month:
                        f'- Previous {number_of_days_in_this_month} :'
                        f'- Mean : {calculations_for_user.mean} | Median : {calculations_for_user.median} | Min : {calculations_for_user.min} | Max : {calculations_for_user.max} | Std Dev : {calculations_for_user.std_dev}'
                        
                        
                user_template_for_existing_user_days = f"""
                  "Today's mood check in:
                        - Enery Level (1-10): {joined_request.energy_value}
                        {f'- Energy States: {joined_request.energyStates}' if joined_request.energyStates else ''}
                        {f'- Emotional States: {joined_request.emotionalStates}' if joined_request.emotionalStates else ''}
                        {f'- Mental States: {joined_request.mentalStates}' if joined_request.mentalStates else ''}
                        {f'- Social/Relational States: {joined_request.socialOrRelationalStates}' if joined_request.socialOrRelationalStates else ''}
                        {f'- Achievement/Purpose States: {joined_request.achievementOrPurposeStates}' if joined_request.achievementOrPurposeStates else ''}
                        {f'- Emotional Intelligence Question: {joined_request.emotionalIntelligenceQuestion}' if joined_request.emotionalIntelligenceQuestion else ''}
                        {f'- Mirror Question: {joined_request.mirrorQuestion}' if joined_request.mirrorQuestion else ''}

                         """     
                
                return user_template_for_existing_user_days
        
        def existing_user_input_(self, joined_request, day, month, energy_levels):
                """ User template input """

                _current_day_checkins =  obtain_previous_checkins_of_the_current_day(self.user_id, self.timezone)
                _current_week_checkins =  obtain_previous_checkins_of_the_current_week(self.user_id, self.timezone)
                _previous_week_checkins =  obtain_previous_checkins_of_the_previous_week(self.user_id, self.timezone)
                _previous_months_checkins =  get_monthly_summaries(self.user_id)
                
                # print("checkins for the current week", _current_week_checkins)
                # print("\n\ncheckins for the previous week", _previous_week_checkins)
                # print("\n\ncheckins for the previous month", _previous_months_checkins)
                
                current_day_checkins = f'Current day check-ins:\n'
                current_week_checkins = f'current week check-ins:\n'   
                previous_week_checkins = 'Previous week check-ins:\n'
                previous_months_checkins = 'Previous month(s) check-in:\n'
                
                
                if len(_current_day_checkins) > 0:
                        checkin_len = len(_current_day_checkins)
                        index = checkin_len
                        for checkin in _current_day_checkins:
                                current_day_checkins += (
                                        f" {index}. energy level: {checkin['energy_value']} | feelings: {','.join(json.loads(checkin['feelings'])) if checkin.get('feelings') else ''} |  avoided emotion: {checkin['avoided_emotion']} | mirror question answer: {checkin['mirror_question']} \n")
                                index -= 1
                        print("Im done in current day checkins")
                                
                                                                                                                        
                if len(_current_week_checkins) > 0:
                        for checkin in _current_week_checkins:
                                print('checkin current week: ', checkin)
                                if checkin['energy_value'] is None:
                                        current_week_checkins += (
                                        f" min: {checkin['min']} | max: {checkin['max']} | mean: {checkin['mean']} | std_dev: {checkin['std_dev']} | trend_slope: {checkin['trend_slope']} | summarized_text: {checkin['texts_summary']}\n\n")
                                else:
                                        current_week_checkins += (
                                        f" energy level: {checkin['energy_value']} | feelings: {', '.join(checkin['feelings']) if checkin['feelings'] else ''} | summarized_text: {checkin['texts_summary']}\n")
                        print("Im done in current week checkins")
               
                if len(_previous_week_checkins) > 0:
                        for checkin in _previous_week_checkins:
                                # created_at_local = to_manila_datetime(checkin['created_at'])
                                # previous_week_checkins += (
                                if checkin['energy_value'] is None:
                                        previous_week_checkins += (
                                        f" min: {checkin['min']} | max: {checkin['max']} | mean: {checkin['mean']} | std_dev: {checkin['std_dev']} | trend_slope: {checkin['trend_slope']} | summarized_insights_of_the_day: {checkin['texts_summary']}\n\n")
                                else:
                                        previous_week_checkins += (
                                        f" energy level: {checkin['energy_value']} | feelings: {', '.join(checkin['feelings']) if checkin['feelings'] else ''} | summarized_insights_of_the_day: {checkin['texts_summary']}\n")
                        print("Im done in last week checkins")
                if len(_previous_months_checkins) > 0:
                        for checkin in _previous_months_checkins:
                                if checkin['energy_value'] is None:
                                        previous_months_checkins += (
                                        f"year: {checkin['year']} | month: {checkin['month']} | min: {checkin['min']} | max: {checkin['max']} | mean: {checkin['mean']} | std_dev: {checkin['std_dev']} | trend_slope: {checkin['trend_slope']} | summarized_insights_of_the_month: {checkin['texts_summary']}\n\n")
                                else: 
                                        previous_months_checkins += (
                                        f"year: {checkin['year']} | month: {checkin['month']} | energy level: {checkin['energy_value']} | feelings: {', '.join(checkin['feelings']) if checkin['feelings'] else ''} | summarized_insights_of_the_month: {checkin['texts_summary']}\n\n")
                          
                        print("Im done in last month checkins")
                # Please analyze my current state and provide personalized recommendations for what I can do today based on the following information:
                user_template = f"""
                
                "Today's mood check in:
                - Enery Level (1-10): {joined_request.energy_value}
                {f'- Feelings: {joined_request.feelings}' if joined_request.feelings else ''}
                {f'- Emotional Question Answer: {joined_request.emotionalIntelligenceQuestion}' if joined_request.emotionalIntelligenceQuestion else ''}
                {f'- Mirror Question Answer: {joined_request.mirrorQuestion}' if joined_request.mirrorQuestion else ''}
                
                {current_day_checkins if len(current_day_checkins) > 0 else ''}
                
                {current_week_checkins if len(previous_week_checkins) > 0 else ''}
                
                {previous_week_checkins if len(previous_week_checkins) > 0 else ''}
                
                {previous_months_checkins if len(previous_months_checkins) > 0 else ''}
                """
                
                return user_template

        # add if statement if user has previous week checkins
                # add previous month checkin
                # if user checked in for a week add it
                
                
                
                # Check if user has  of data then add a months section in the prompt with monthly breakdown
                # Check if user has a month only of data then add a month section in the prompt with weekly breakdown
                # Check if user has months of data then add a months section in the prompt with monthly breakdown
                




        def existing_system_template(self):
                system_template = """
                       You are an empathetic and psychologically informed mood analysis assistant.

                        Your task is to analyze a sequence of user reflections to generate a concise, emotionally intelligent insight.

                        The provided input includes (in descending order of priority):

                        Current Check-in — energy level (1–10), selected feelings, Emotional Intelligence answer, and Mirror Question answer.

                        Previous Check-ins from the Same Day — earlier emotional states and reflections (if available). 

                        Summarized Reflections from Previous Days in the Current Week (if available).

                        Summarized Weekly and Monthly Insights (if available).

                        Each input builds a timeline of emotional experience. Your job is to understand this evolving pattern and generate an insight that captures:

                        The current emotional state

                        The continuity or shift compared to earlier check-ins today

                        The connection to larger weekly or monthly emotional themes

                        A reflective takeaway that feels supportive, not prescriptive

                        Analytical Focus

                        Current Emotional Theme: Identify the user’s present state (e.g., tension, calm, fatigue, hope).

                        Intra-day Dynamics: Detect emotional fluctuations or consistencies across multiple check-ins today.

                        Long-term Context: Recognize recurring patterns or progress from previous summaries.

                        Emotional Needs: Infer underlying needs (rest, reassurance, clarity, connection, etc.) subtly within reflection.

                        Safety and Sensitivity:

                        Avoid medical or clinical terms.

                        If distress signals appear (e.g., hopelessness, exhaustion), respond with brief compassion and mention gentle support (e.g., “It might help to reach out to someone you trust.”).

                        Keep tone empowering, never diagnostic.

                        Output Style

                        Tone: Warm, insightful, and psychologically grounded.

                        Voice: Reflective observation, not instruction or judgment.

                        Language: Natural and emotionally intelligent — avoid formulaic phrasing or temporal anchors (“yesterday”, “today”).

                        Length limits: Respect the constraints of each field from the provided schema.
                        """
                return system_template
   





# - Analyze all provided states, considering interplay (e.g., low energy + anxious = restorative focus).
#                         - Prioritize safety and well-being; for conflicting states, address negative ones first.
#                         - Draw from evidence-based practices (CBT, mindfulness, exercise science, positive psychology).
#                         - Provide immediate, practical actions (not long-term therapy or medical advice).
#                         - Ensure recommendations are diverse (e.g., physical, mental, social) and positive.

#                         SAFETY GUIDELINES:
#                         - If concerning patterns detected, include gentle resource suggestions
#                         - Never provide medical or clinical diagnoses
#                         - Focus on empowerment and self-awareness, not pathology
#                         - For crisis indicators, prioritize immediate support resources over analysis

#                         STRICT OUTPUT RULES:
#                         - Respond ONLY with a valid JSON object

# OUTPUT FORMAT RULES:

# **overall_mood:**
# - Maximum 15 words
# - Use format: "Your overall mood today was [classification]."
# - Classifications: Thriving, Positive, Stable, Neutral, Mixed, Challenging, Struggling
# - Choose based on energy level and emotional balance

# **comparison_insight:**
# - Compare to specified timeframe (7 days, 2 weeks, etc.)
# - Include 2-3 specific observations from the data
# - Maximum 2 sentences, 50 words total
# - Start with "Compared to the past [timeframe]..."
# - Highlight what's different or notable about today vs. recent pattern

# **pattern_noticed:**
# - Identify ONE specific, actionable correlation
# - Use format: "[Specific trigger/behavior] tends to correlate with [mood outcome]"
# - Base on actual data provided, not generic advice
# - Maximum 25 words
# - Focus on behavioral patterns, timing, or contextual factors

# **mood_trend:**
# - Describe direction over time with specific timeframe
# - Use trend language: "gradually improving", "declining", "stabilizing", "fluctuating"
# - Include starting and current state
# - Maximum 30 words
# - Be specific about timeframes (e.g., "since last Thursday", "over the past week")

# **suggestions:**
# - Provide 1-2 concrete, immediate actions
# - Base suggestions on identified patterns and current state
# - Use actionable language ("Try...", "Consider...", "Continue...")
# - Maximum 40 words total
# - Prioritize evidence-based interventions matching their current needs

# QUALITY REQUIREMENTS:
# - Use specific details from user data, not generic responses
# - Avoid repetitive phrasing across different insights for the same user
# - Ensure suggestions directly relate to patterns noticed
# - Keep tone supportive but not overly clinical
# - If insufficient data for a field, acknowledge limitations honestly

# EXAMPLE RESPONSE FORMAT:

# {
#   "overall_mood": "Your overall mood today was Mixed with underlying resilience.",
#   "comparison_insight": "Compared to the past 7 days, today shows more emotional complexity but stable energy. Your text responses reveal increased self-awareness.",
#   "pattern_noticed": "Morning check-ins after physical activity correlate with clearer mental states.",
#   "mood_trend": "Energy has been stabilizing over the past week, shifting from fluctuating to more consistent levels.",
#   "suggestions": "Continue your morning routine pattern. Try a brief mindfulness check-in after physical activity to reinforce the clarity you've noticed."
# }

# system_template = """
# - Analyze all provided states, considering interplay (e.g., low energy + anxious = restorative focus).
# - Prioritize safety and well-being; for conflicting states, address negative ones first.
# - Draw from evidence-based practices (CBT, mindfulness, exercise science, positive psychology).
# - Provide immediate, practical actions (not long-term therapy or medical advice).
# - Ensure recommendations are diverse (e.g., physical, mental, social) and positive.

# OUTPUT FORMAT: 
# - Write it in a form of JSON response
# - For overall mood, provide a short summary with a maximum of 15 words (e.g., "Your overall mood today was Neutral.")

# {
#   "overall_mood": "Your overall mood today was Neutral.",       
#   "comparison_insight": "Compared to the past 7 days, today's mood was more stable and slightly more positive. You checked in more consistently and used words like 'balanced,' 'clear-headed,' and 'at ease' in your entries.",
#   "pattern_noticed": "Days with early check-ins and short walks tend to correlate with a calmer mood.",
#   "mood_trend": "Your mood has been gradually improving since last Thursday, shifting from 'low energy' to 'neutral'.",
#   "suggestions": "Keep up the routines that ground you in the morning. Consider adding a brief reflection on what made you feel balanced today to reinforce the habit."
# }

# - Write a short recommendation (2–4 sentences).
# - First sentence: brief summary of the user’s state (in natural, empathetic tone).
# - Following sentences: 2–4 concrete action steps, in imperative mood.
# - Keep under 60 words total.    



# """

# sytem_template = """
        
#         CORE PRINCIPLES:
#         - Analyze all provided states, considering interplay (e.g., low energy + anxious = restorative focus).
#         - Prioritize safety and well-being; for conflicting states, address negative ones first, weighted by energy level or frequency.
#         - Draw from evidence-based practices (CBT, mindfulness, exercise science, positive psychology).
#         - Provide immediate, practical actions (not long-term therapy or medical advice).
#         - Ensure recommendations are diverse (e.g., physical, mental, social actions) and positive.

#         OUTPUT FORMAT:
#             - Respond with ONLY the recommended action as a direct imperative sentence
#             - Start with an action verb (e.g., "Take a 10-minute walk outside")
#             - Do not include explanations, context, or reasoning
#             - Do not reference the user's input states in your response
#             - Maximum of 20 words
#             - Vary recommendation types (e.g., physical, mental, social).
#         """