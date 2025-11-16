import random

new_user_comparison_insights = [
    "This is your baseline - we'll help you understand patterns as you continue checking in. \nEven this single entry tells us you're someone who values self-awareness."
    "Every journey begins with awareness — this first check-in marks the start of understanding your emotions more clearly each day.",
    "You’ve taken the first brave step toward self-awareness. Keep checking in to uncover your unique emotional patterns over time.",
    "This first entry builds your emotional foundation. With each check-in, you’ll reveal how your moods shift and strengthen naturally.",
    "No comparisons yet — just your starting point. Every future check-in helps uncover what truly shapes your emotions and mindset.",
    "You’ve begun tracking your emotions — that’s powerful. Each reflection ahead will make your patterns clearer and your insights deeper.",
    "Every insight begins here. Keep showing up to reveal the subtle rhythms and emotional strengths that shape your daily experiences.",
    "This first log marks your emotional baseline. Continued check-ins will help you recognize progress, triggers, and moments of growth.",
    "No trends yet — but this first reflection is valuable. Every entry you add brings greater clarity to your emotional story.",
    "This is your foundation for emotional growth. Check in often to see how your moods evolve and your resilience strengthens.",
    "You’ve started your emotional record today. Each check-in after this builds a clearer picture of your balance and self-awareness.",
    "You’ve created your emotional starting point. Consistent reflections ahead will reveal how your energy and mood shift through time.",
    "This first check-in sets your baseline. Keep logging to identify what nurtures your positivity and what drains your emotional focus.",
    "You’ve made the first move toward understanding yourself. Future check-ins will help you uncover patterns behind your emotional changes.",
    "No patterns yet — but this first moment matters. Regular reflections will reveal your emotional landscape with growing precision.",
    "This initial check-in marks the start of your self-discovery. Keep showing up to learn how life shapes your emotional energy.",
    "You’ve taken step one — awareness. Continued reflections will build your emotional map, guiding how you respond to daily experiences.",
    "There’s no past data yet, only a beginning. Every future entry adds depth to your understanding of your emotional wellbeing.",
    "This is your emotional zero point — a baseline for growth. Regular check-ins reveal how your moods align with daily habits.",
    "You’ve started something meaningful. Each check-in after this deepens your understanding of emotions and the patterns that influence them most.",
    "This first reflection begins your emotional timeline. With consistency, you’ll see how your moods, thoughts, and behaviors truly connect."
]


pattern_messages_for_new_users = [
    "Each check-in builds self-awareness — your patterns reveal themselves through steady reflection.",
    "Keep showing up. Patterns form when you give your emotions space to be seen daily.",
    "Every entry deepens your awareness — consistency transforms random feelings into recognizable emotional patterns.",
    "You’re building emotional insight one check-in at a time — keep nurturing your reflection habit.",
    "Patterns aren’t instant — they unfold as you keep recording what feels real each day.",
    "Daily reflections reveal what truly shapes your mood — consistency brings emotional clarity.",
    "You’re not just tracking; you’re learning your emotional language through each consistent check-in.",
    "Steady check-ins help you see what drives your energy and feelings over time.",
    "Your emotions leave gentle clues — consistency helps connect them into meaningful patterns.",
    "Each log is a mirror — over time, you’ll see what shapes your emotional flow.",
    "Every reflection strengthens your emotional awareness — keep building your streak to discover hidden links.",
    "You’re learning how your feelings move. Each day adds another clue to your emotional puzzle.",
    "Keep checking in — you’re closer to seeing how your thoughts and moods intertwine.",
    "Consistency turns chaos into clarity — your daily reflections create patterns of understanding.",
    "Emotional insight comes quietly, through repetition — keep logging to connect feeling with meaning.",
    "Each day you reflect adds color to your emotional landscape — patterns soon take shape.",
    "Your patterns are forming in the background — consistency makes them clearer with every entry.",
    "You’re creating your emotional fingerprint. Regular check-ins make it visible and uniquely yours.",
    "Every check-in refines your self-awareness — stay consistent to uncover your emotional rhythm.",
    "Keep showing up — your feelings are teaching you their patterns one day at a time."
    ]

mood_trend_messages_for_new_users = [
        "Each check-in adds a brushstroke to your mood trend — keep painting your emotional picture.",
        "Your emotional story builds daily — consistency helps your mood trend come into focus.",
        "Every entry adds context — your mood trend strengthens as your reflections grow consistent.",
        "Keep logging — your trend reveals how your emotions shift, recover, and stabilize over time.",
        "Mood awareness blooms from routine — each check-in connects today’s feeling to yesterday’s progress.",
        "You’re writing your emotional timeline. Daily reflections make your mood trend visible and real.",
        "Each reflection builds momentum — your trend emerges when you keep showing up for yourself.",
        "Your trend begins forming now — stay present and track your emotions as they evolve.",
        "Consistency transforms scattered moments into a clear mood trend — keep reflecting daily.",
        "You’re creating your emotional history — each entry shapes your personal mood evolution.",
        "The more consistently you check in, the more meaningful your trend insights become.",
        "Every log strengthens your emotional trend — consistency gives your data its story.",
        "Your trend reflects your resilience — stay consistent to see your emotional balance unfold.",
        "Keep adding reflections — your mood trend will soon reveal how you adapt and grow.",
        "Each check-in gives life to your emotional journey — your trend grows with every log.",
        "Mood awareness is cumulative — every check-in builds the pattern of your emotional growth.",
        "You’re crafting your emotional timeline — your trend thrives on steady, mindful check-ins.",
        "Daily reflections create momentum — keep showing up to understand your emotional evolution.",
        "Consistency turns moments into meaning — your mood trend forms through steady self-awareness.",
        "Every reflection adds clarity — your mood trend is waiting to show you your progress."
    ]



pattern_gap_messages = [
    "It’s been {days} days — your patterns are waiting to be rediscovered, not judged.",
    "After {days} days away, you’re reconnecting with what your emotions have been trying to tell you.",
    "{days} days have passed, but your inner rhythm hasn’t disappeared — it’s just waiting to be noticed again.",
    "Reflection paused for {days} days — that’s okay. Picking it up again still counts as growth.",
    "It’s been {days} days since your last check-in. Your emotional story continues right where you left it.",
    "After {days} days off, your self-awareness didn’t vanish — it just needed a breather.",
    "{days} days may have passed, but you’re already rebuilding your pattern of awareness.",
    "You’ve taken {days} days to breathe — now your reflection can catch up with your life.",
    "{days} days later, your emotional patterns are still here — let’s see what they reveal next.",
    "Even after {days} days, your feelings have been speaking softly. Today you’re listening again.",
    "Your reflections paused for {days} days — today’s check-in reconnects the thread.",
    "It’s been {days} days, but every return adds new depth to your understanding.",
    "{days} days away doesn’t erase your awareness — it just gives you a new angle to view it from.",
    "Your emotional rhythm took a pause for {days} days — this check-in restarts the melody.",
    "After {days} days, you’re noticing again. Awareness never truly disappears.",
    "You’ve been away for {days} days — your patterns have been patiently waiting for your return.",
    "{days} days without logging doesn’t mean lost progress — reflection resumes exactly where you are now.",
    "After {days} days of silence, today’s check-in adds a new note to your emotional pattern.",
    "It’s been {days} days — enough time for new feelings to take shape. Let’s rediscover them.",
    "You’re back after {days} days — awareness always finds its way home."
]

mood_trend_gap_messages = [
     "It’s been {days} days since your last entry — your emotional story picks up again today.",
    "After {days} days away, your mood trend is ready for a new chapter.",
    "{days} days between reflections — now’s a good moment to notice what’s shifted.",
    "Your trend paused for {days} days, but your awareness hasn’t. Let’s reconnect.",
    "{days} days later, today’s mood adds a fresh piece to your evolving picture.",
    "Even after {days} days, your emotional landscape is still unfolding — you’re just rejoining it.",
    "It’s been {days} days — your check-in today restarts the thread of your emotional journey.",
    "Your trend took a break for {days} days — today brings it gently back to life.",
    "After {days} days, your reflection picks up where your last emotion left off.",
    "{days} days apart — now’s your chance to see what’s changed inside and around you.",
    "Your story didn’t stop during those {days} days — it’s just waiting to be noticed again.",
    "{days} days since the last entry — let’s reconnect the dots and see how you’ve shifted.",
    "The last {days} days added quiet space to your journey — today gives it voice again.",
    "Even after {days} days away, your emotions have kept evolving — now we can catch up.",
    "It’s been {days} days, but your trend is still yours — no reset needed, just reflection.",
    "After {days} days, this check-in continues your mood journey, not restarts it.",
    "Those {days} days off may hold hidden patterns — today you’re reconnecting to notice them.",
    "Your awareness is reawakening after {days} days — that’s progress, not pause.",
    "{days} days later, your mood story expands with today’s reflection.",
    "After {days} days away, you’re rejoining your emotional timeline — welcome back."
]


def gap_messages( gap_days: int):
            """Return a random encouraging message based on the gap days."""
            gap_message = ""
            if 4 <= gap_days <= 6:
                gap_message = "short_gap_message"
            elif 7 <= gap_days <= 9:
                gap_message = "medium_gap_message"
            else:
                gap_message = "long_gap_message"
                
                
            gap_messages = {
            "short_gap_message": [
                "Nice to see you again — even short breaks can bring fresh perspective.",
                "You missed a couple of days — totally normal. What matters is you came back.",
                "Good to see you showing up again. These small returns build real self-awareness.",
                "Welcome back — you’re continuing your story, one reflection at a time.",
                "Life happens. Checking in again means you still care about how you feel.",
                "Nice to see you again — even short breaks can bring fresh perspective.",
                "Welcome back! Every reflection helps you stay connected to yourself.",
                "You missed a few days — totally okay. What matters is you showed up today.",
                "Good to see you checking in again. Awareness grows one step at a time.",
                "Short break, strong comeback — that’s how real habits form.",
                "Life happens. You came back, and that’s what matters most.",
                "You took a few days off — now you’re tuning back in. That’s growth.",
                "Glad you’re here again — this check-in keeps your story going.",
                "Even small pauses can reset clarity — great to see you back.",
                "Consistency isn’t perfection; it’s return after pause. You just proved that.",
                "Welcome back — you’re continuing your journey one reflection at a time.",
                "Sometimes you need a little space to feel ready again. You did it.",
                "Back already? That’s commitment. Each small return matters.",
                "You’re keeping the rhythm alive — reflection takes patience.",
                "Short gap, steady heart — you’re still showing up for yourself.",
                "Thanks for returning. Even quick pauses teach something about balance.",
                "You missed a couple of days, but your awareness didn’t fade.",
                "Today’s check-in closes that little gap — you’re still on track.",
                "Short breaks don’t break habits — they make them real.",
                "Glad to see you again — self-awareness doesn’t need perfection, only presence."

            ],
            "medium_gap_message": [
                    "Glad you returned after a few days away — this check-in reconnects you to your inner rhythm.",
                    "A few days off isn’t failure; it’s reset time. Great job rebuilding momentum.",
                    "Welcome back — let’s notice what’s changed since your last reflection.",
                    "You’re showing commitment by returning after a few days. That matters.",
                    "Taking space can be healthy. Today’s check-in closes the gap with awareness.",
                    "Good to see you after a short break — this check-in is your fresh start.",
                    "You’ve been away for a bit — thanks for showing up again today.",
                    "Glad you’re back. A week off can shift perspective — what’s changed since?",
                    "Even after a few days away, your reflection habit is still alive.",
                    "You’re reconnecting with yourself — that’s never wasted effort.",
                    "Welcome back! Rebuilding rhythm matters more than any missed streak.",
                    "This is your reset moment — great to see you recommitting to awareness.",
                    "A few days away is normal — your return is what counts.",
                    "You’re back, and that says a lot about your self-awareness.",
                    "Momentum rebuilds with one step — and this check-in is that step.",
                    "Great to have you back — every return deepens reflection.",
                    "You’re choosing presence again after time away — powerful choice.",
                    "Welcome back — each restart proves how much this matters to you.",
                    "After a week away, you’re re-engaging with your emotional story.",
                    "Short breaks don’t erase growth — they just remind you why it matters.",
                    "Good to see you returning — this check-in keeps your habit alive.",
                    "You took space, now you’re reconnecting — that’s balance, not failure.",
                    "Even when you step back, you come back stronger. That’s reflection in motion.",
                    "Rebuilding awareness is easier than it feels — today’s proof of that.",
                    "Glad you’re back — this is how sustainable habits are built."

                    
                    ],
            "long_gap_message": [
                    "It’s been a while — welcome back. Restarting takes courage, and you just did that.",
                    "Glad to have you here again — today’s entry marks a fresh start in your reflection journey.",
                    "Sometimes life pulls us away — what matters is showing up now. You did.",
                    "Coming back after a break isn’t easy, but it shows you still care about your emotional growth.",
                    "This is your re-entry moment — one honest reflection at a time is enough.",
                    "It’s been a while — welcome back. Restarting takes courage, and you just did that.",
                    "Glad to have you checking in again — reflection always welcomes you home.",
                    "You’ve taken time away — now you’re choosing awareness again. That’s powerful.",
                    "Coming back after a longer break shows real self-respect.",
                    "Sometimes life gets busy — this return is a strong reminder of what matters.",
                    "Great to see you here again — today’s check-in is a true restart.",
                    "It’s never too late to tune back in — you’re doing that beautifully right now.",
                    "This is your re-entry point — reflection doesn’t expire, it renews.",
                    "Glad to have you back — awareness waits patiently, never judges.",
                    "You paused for a while, but this step shows growth, not regression.",
                    "Every comeback is progress — today’s check-in proves that.",
                    "You’re rewriting your rhythm today — small steps count most.",
                    "It takes real intention to return after a break — proud of you for doing it.",
                    "Even long gaps can’t erase self-awareness — it always finds its way back.",
                    "This is a gentle restart, not a reset — you’ve still been learning.",
                    "You’ve been away, but the fact you’re here means you still care.",
                    "Reflection isn’t about streaks — it’s about honesty, and you’re back to it.",
                    "Welcome back — each return plants a stronger root of awareness.",
                    "After time away, checking in again is an act of self-care.",
                    "You’re back after a long gap — that choice speaks volumes about your resilience."

                    ],
            }
            
            return random.choice(gap_messages[gap_message])
            
