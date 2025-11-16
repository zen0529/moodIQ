from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time


class moodInsightOutputParser(BaseModel):
    overall_mood: str = Field(
        description=(
            "A short, natural-language summary (max 20 words) describing the user's overall emotional state. "
            "It should sound reflective or observational — not formulaic. "
            "Example: 'Energy feels low, but there’s a quiet sense of perseverance.'"
        )
    )

    comparison_insight: str = Field(
        description=(
            "Compare the current state to previous data (yesterday, week, or month if available). "
            "Highlight emotional or energetic changes. If no prior data, mention it naturally. "
            "Max 2 sentences, 50 words. "
            "Example: 'Compared to earlier check-ins, emotions feel more balanced though motivation still fluctuates.'"
        )
    )
    
    pattern_noticed: str = Field(
        description=(
            "Identify one clear correlation between a feeling, thought, or behavior and a mood outcome. "
            "Format: '[Trigger/behavior] tends to correlate with [mood outcome].' "
            "Keep it specific and grounded. Max 25 words."
        )
    )

    mood_trend: str = Field(
        description=(
            "Describe the emotional trajectory over time (e.g., improving, stabilizing, declining, fluctuating). "
            "Include timeframe if possible. Max 30 words. "
            "Example: 'Mood appears to be gradually improving over the week, with more emotional steadiness emerging.'"
        )
    )

    suggestions: str = Field(
        description=(
            "Provide 1–2 actionable, psychologically safe suggestions (max 40 words). "
            "Tone should be gentle and supportive — never medical. "
            "Example: 'Try spending a few quiet minutes journaling about what felt manageable today.'"
        )
    )

 


# class suggestionOutputParser(BaseModel):
#     suggestions: str = Field(
#         description="1-2 concrete actions, max 40 words. Actionable and based on the input."
#     )

# class moodInsightOutputParserForNewUsers(BaseModel):
#     suggestions: str = Field(
#         description="1-2 concrete actions, max 40 words. Actionable insights based on the input."
#     )

class EnergyStats(BaseModel):
    mean: float
    median: float
    min: int
    max: int
    std_dev: float
    trend_slope: float
    
class GenerateInsightsRequest(BaseModel):
    energy_value: int
    feelings: Optional[list[str]] = None 
    emotionalIntelligenceQuestion: Optional[str] = None
    mirrorQuestion: Optional[str] = None
    

class JoinedInsightRequest(BaseModel): 
    energy_value: int
    feelings: Optional[str] = None 
    emotionalIntelligenceQuestion: Optional[str] = None
    mirrorQuestion: Optional[str] = None
    summarizedAnswers: Optional[str] = None


class timezoneData(BaseModel):
    current_date: date
    current_time: time
    current_day: str
    current_year: int
    current_month: int
    days_in_month: int