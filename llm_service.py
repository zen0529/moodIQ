from langchain_core.prompts import ChatPromptTemplate
from gap_days import *
from obtain_timezone import getTimeZone
from models import *
from fastapi import HTTPException
from prompt_templates import *
from checkins_repository import check_which_user, get_days_since_last_checkin, is_new_user, is_new_user_with_checkin
from setup import *
from langchain_core.output_parsers import JsonOutputParser
# from models import MoodAnalysis       
from new_users_overall_mood import overall_mood




def Join_States(request: GenerateInsightsRequest) -> JoinedInsightRequest:
    
    """ This function takes a GenerateInsightsRequest object and joins the feelings into comma-separated strings. """
    
    # Create a dictionary to hold the joined states
    states_map = {
        "feelings": request.feelings,
    }
    
    # Join the states into comma-separated strings
    joined = {
        name: ", ".join(states) if len(states) > 1 else (states[0] if states else "")
        for name, states in states_map.items()
    }
    
    print(f'joined = {joined}') # for logging purposes
    return JoinedInsightRequest(
        energy_value=request.energy_value,
        mirrorQuestion=request.mirrorQuestion,
        emotionalIntelligenceQuestion=request.emotionalIntelligenceQuestion,
        
        # add summarized answers later
        
        
        **joined
    ) 


async def LLM_Query(request: GenerateInsightsRequest, user_id: str, user_timezone: str):
    """Generate insights using LLM with fallback support."""
    
    # Setup
    timezone = getTimeZone(user_timezone)
    user_type = check_which_user(user_id, user_timezone, request)
    print(f"user type: {user_type}")
    
    # Build prompt
    joined_request = Join_States(request)
    prompt = prompts(joined_request=joined_request, user_id=user_id, timezone=user_timezone)
    
    system_template, user_template = _get_templates(
        prompt, user_type, joined_request, timezone
    )
    
    print("\n\nsystem template", system_template)
    print("\n\nuser template", user_template)
    
    # Get LLM response
    insights = await _call_llm_with_fallback(system_template, user_template)
    
    # Apply business logic
    return _apply_user_specific_logic(insights, request, user_type, user_id, user_timezone)


def _get_templates(prompt, user_type, joined_request, timezone):
    """Get system and user templates based on user type."""
    if user_type == "existing_user":
        print("\n\nuser is existing")
        return (
            prompt.existing_system_template(),
            prompt.existing_user_input_(
                joined_request, 
                timezone.current_day, 
                timezone.current_month, 
                timezone.days_in_month
            )
        )
    else:
        print("\n\nuser is new")
        return (
            prompt.new_user_system_template(),
            prompt.new_user_template()
        )


async def _call_llm_with_fallback(system_template: str, user_template: str) -> dict:
    """Call LLM with fallback to secondary model."""
    parser = JsonOutputParser(pydantic_object=moodInsightOutputParser)
    
    template = ChatPromptTemplate([
        ('system', system_template + "\n\n {format_instructions}"),
        ('user', user_template)
    ])
    
    messages = template.format_messages(
        format_instructions=parser.get_format_instructions()
    )
    
    # Try primary, then fallback
    for llm in [PRIMARY_LLM, FALLBACK_LLM_1, FALLBACK_LLM_2, FALLBACK_LLM_3, FALLBACK_LLM_4]:
        try:
            response = await llm.ainvoke(messages)
            print("\n\nresponse content", response.content)
            print("\n\nresponse content type", type(response.content))
            
            insights = parser.parse(response.content)
            return _normalize_insights(insights)
            
        except Exception as e:
            print(f"LLM call failed: {e}")
            if llm == FALLBACK_LLM_4:  # Last attempt failed
                print(f"Messages: {messages}")
                raise HTTPException(
                    status_code=503,
                    detail="Language model services are currently unavailable"
                )


def _normalize_insights(insights) -> dict:
    """Convert insights to dict if needed."""
    if hasattr(insights, "dict"):
        try:
            return insights.dict()
        except Exception:
            return json.loads(json.dumps(insights))
    elif not isinstance(insights, dict):
        return dict(insights)
    return insights


def _apply_user_specific_logic(
    insights: dict, 
    request: GenerateInsightsRequest, 
    user_type: str, 
    user_id: str, 
    user_timezone: str
) -> dict:
    """Apply business logic based on user type and activity gaps."""
    
    # Always override overall_mood from energy_value
    insights['overall_mood'] = overall_mood(request.energy_value)
    print("energy value:", request.energy_value)
    print("insights overall mood:", insights['overall_mood'])
    
    if user_type == "new_user":
        insights['comparison_insight'] = random.choice(new_user_comparison_insights)
        insights['pattern_noticed'] = random.choice(pattern_messages_for_new_users)
        insights['mood_trend'] = random.choice(mood_trend_messages_for_new_users)
        print("New User insights:", insights)
        return insights
    
    # Existing user logic
    gap_days = get_days_since_last_checkin(user_id, user_timezone)
    print("gap days:", gap_days)
    
    if gap_days >= 4:
        gap_message = gap_messages(gap_days)
        insights['comparison_insight'] = gap_message
        insights['pattern_noticed'] = random.choice(pattern_gap_messages).format(days=gap_days)
        insights['mood_trend'] = random.choice(mood_trend_gap_messages).format(days=gap_days)
    
    print("insights:", insights)
    return insights


# async def LLM_Query(request: GenerateInsightsRequest, user_id: str,  user_timezone: str):
#     """ 
#         This function takes a GenerateInsightsRequest object and sends it to the LLM model to generate response. 
#         If the primary model fails, it falls back to the secondary model. 
#     """
    
#     # Get current date and time in user's timezone
#     timezone = getTimeZone(user_timezone)
#     # date_now = f"{timezone.current_month} {timezone.current_time} {timezone.current_day}"
    
#     system_template = ''
#     user_template = ''
    
#     # Determine user type
#     user_type = check_which_user(user_id)   
    
#     print(f"user type: {user_type}")
#     # if user_type == "new_user":    
#     #     print("\n\n\nnew user")
#     #     SUPABASE.table("users").insert({"timezone_user": user_timezone}).execute()  
    
    
#     # response = await PRIMARY_LLM.ainvoke("generate")
#     # Create a prompt based on the user type 
#     # instantiate the prompt class
#     joined_request = Join_States(request)
    
#     prompt = prompts(joined_request=joined_request, user_id=user_id, timezone=user_timezone) 
    
#     parser = JsonOutputParser(pydantic_object=moodInsightOutputParser)
    
#     if user_type == "existing_user":
#         # system_template = prompt.existing_user_system_template()
#         # user_template =  prompt.existing_user_template(Join_States(request))
#         print("\n\nuser is existing")
#         system_template = prompt.existing_system_template()
#         user_template =  prompt.existing_user_input_(joined_request, timezone.current_day, timezone.current_month, timezone.days_in_month)
#     else:   
#         print("\n\nuser is new")
#         system_template = prompt.new_user_system_template()
#         user_template =  prompt.new_user_template()
    
#     print("\n\nsystem template", system_template)
#     print("\n\nuser template",user_template)
    
#     # create the parser for output formatting
#     # print(f"parser: {parser}")
#     # Create a ChatPromptTemplate object with system and user messages in a list of tuples
#     template = ChatPromptTemplate([
#         ('system', system_template + "\n\n {format_instructions}"),
#         ('user', user_template)
#     ])  

#     # Convert the template into a list of formatted messages that the LLM can understand
#     messages = template.format_messages(
#         format_instructions=parser.get_format_instructions()
#     )

#     # print(f"mesages: {messages}")

#     try:
#         # Send the formatted messages to the LLM asynchronously and await the response
#         response = await PRIMARY_LLM.ainvoke(messages)
        
#         print("\n\nresponse content", response.content)
#         print("\n\nresponse content type", type(response.content))
        
#         # generated insights 
#         insights = parser.parse(response.content)
        
#         if hasattr(insights, "dict"):
#                 try:
#                     insights = insights.dict()
#                 except Exception:
#                     insights = json.loads(json.dumps(insights))
#         elif not isinstance(insights, dict):
#             insights = dict(insights)
        
#         print("insights: ", type(insights))

#         print("insights overall mood: ", insights['overall_mood'])
        
#         print("energy value:", request.energy_value)
#         if user_type == "new_user":
#             insights['overall_mood'] = overall_mood(request.energy_value)
#             insights['comparison_insight'] = random.choice(new_user_comparison_insights) 
#             insights['pattern_noticed'] = random.choice(pattern_messages_for_new_users) 
#             insights['mood_trend'] = random.choice(mood_trend_messages_for_new_users)
#             print("New User insights: ", insights)  
#             return insights
            
#         else:
#             gap_days = get_days_since_last_checkin(user_id, user_timezone)
#             gap_message = gap_messages(gap_days)
#             insights['overall_mood'] = overall_mood(request.energy_value)
            
#             print("gap days: naur ", gap_days)
#             print("insights overall mood:",  insights['overall_mood'])
#             if gap_days >= 4:
#                 insights['overall_mood'] = overall_mood(request.energy_value)
#                 insights['comparison_insight'] = gap_message
#                 insights['pattern_noticed'] = random.choice(pattern_gap_messages).format(days=gap_days)
#                 insights['mood_trend'] = random.choice(mood_trend_gap_messages).format(days=gap_days) 
#             print(" insights: ", insights)
#             return insights
        
        
        
#         # return insights
        

#     except Exception as e:
#         print(f"Primary model failed: {e}")
        
#         # Fallback to secondary model
#         try:
#             response = await FALLBACK_LLM.ainvoke(messages)
            
#             print("\n\nresponse content", response.content)
#             print("\n\nresponse content type", type(response.content))
            
#             # generated insights 
#             insights = parser.parse(response.content)
            
#             if hasattr(insights, "dict"):
#                 try:
#                     insights = insights.dict()
#                 except Exception:
#                     insights = json.loads(json.dumps(insights))
#             elif not isinstance(insights, dict):
#                 insights = dict(insights)
            
#             print("insights: ", type(insights))

#             print("insights overall mood: ", insights['overall_mood'])
            
#             print("energy value:", request.energy_value)
#             print("energy value type:", type(request.energy_value))
            
#             if user_type == "new_user":
#                 insights['overall_mood'] = overall_mood(request.energy_value)
#                 insights['comparison_insight'] = random.choice(new_user_comparison_insights) 
#                 insights['pattern_noticed'] = random.choice(pattern_messages_for_new_users) 
#                 insights['mood_trend'] = random.choice(mood_trend_messages_for_new_users)
#                 print("New User insights: ", insights)  
#                 return insights
                
#             else:
#                 gap_days = get_days_since_last_checkin(user_id, user_timezone)
#                 gap_message = gap_messages(gap_days)
#                 print("request energy value", request.energy_value)
#                 insights['overall_mood'] = overall_mood(request.energy_value)
                
#                 print("gap days: naur ", gap_days)
#                 print("insights overall mood: fallback",  insights['overall_mood'])
#                 if gap_days >= 4:
#                     insights['overall_mood'] = overall_mood(request.energy_value)
#                     insights['comparison_insight'] = gap_message
#                     insights['pattern_noticed'] = random.choice(pattern_gap_messages).format(days=gap_days)
#                     insights['mood_trend'] = random.choice(mood_trend_gap_messages).format(days=gap_days) 
#                 print("insights fallback: ", insights)
#                 return insights
            
            
#         except Exception as fallback_e:
#             print(f"Messages: {messages}")
#             error_msg = f"Both models failed: {fallback_e}" 
#             print(error_msg) # For server-side logging
#             raise HTTPException(
#                 status_code=503,  # Service Unavailable
#                 detail="Language model services are currently unavailable"
#             )
            

def new__user_query(request: GenerateInsightsRequest):
    pass

async def summarize_insight_daily(input_text: str):
    
    system_template = """
    You are an empathetic mood analysis assistant helping the user understand their emotional progress over time.

    You are given the user’s most recent check-in answers. Each check-in consists of two responses:

    Emotional Intelligence Question: "What emotions are you avoiding right now? How is this avoidance limiting your potential?"
    Mirror Question: "What would you tell someone else facing this exact situation?"

    Your task is to summarize the emotional pattern, mindset, and underlying need reflected in the user’s responses.

    The summary should sound like an internal reflection — warm, psychologically insightful, and emotionally aware.

    Do not refer to time (e.g., avoid “yesterday,” “today,” or “recently”).

    Focus on:

    The emotional lesson or pattern shown in the responses

    The user’s emerging mindset or growth direction

    A short, supportive takeaway that captures their inner state

    Output only one paragraph, limited to 50 words.

    Respond with the insight only — no prefaces, labels, or meta-text.

    Here is the user's input:
    {input_text}
    """


    # Properly define the prompt structure
    prompt = system_template.format(input_text=input_text)

    # Format the message
    # messages = prompt.format_messages(input_text=input_text)

    # Call the model
    try:
        response = await SUMMARIZATION_LLM.ainvoke(prompt)
        return response.content
    
    except Exception as e:
        print(f"en error occured: {e}")

async def summarize_insight_monthly(input_text: str):
    system_template = """
    You are an empathetic mood analysis assistant helping the user understand their emotional growth over time.

    You are given a collection of daily reflective insights — each one summarizes the user’s emotional state and mindset from individual check-ins.

    Your task is to synthesize these daily insights into one cohesive reflection that captures the user’s overall emotional evolution, recurring patterns, and emerging lessons.

    Focus on:

    The emotional themes or patterns appearing throughout the insights

    Signs of healing, progress, or recurring inner struggles

    The deeper emotional needs or beliefs guiding the user’s journey

    A reflective and compassionate tone that conveys understanding and continuity

    Avoid references to time (e.g., “throughout the month,” “lately,” “in recent days”).

    The summary should sound timeless, gentle, and psychologically insightful — as if capturing the essence of the user’s inner journey in one paragraph.

    Limit to 80 words.

    Respond with the reflection only — no prefaces or labels.


    Here is the user's last months daily checkins:
    {input_text}
    """


    # Properly define the prompt structure
    prompt = system_template.format(input_text=input_text)

    # Call the model
    try:
        response = await SUMMARIZATION_LLM.ainvoke(prompt)
        return response.content
    
    except Exception as e:
        print(f"en error occured: {e}")

