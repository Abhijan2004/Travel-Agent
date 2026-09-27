from agent import agent


print("✈️ AI Travel Planner")
print("--------------------")

destination = input("Where do you want to travel? ")
days = input("How many days? ")
budget = input("What is your budget? ")
interests = input("What are you interested in? ")


prompt = f"""
You are an AI Travel Planner.

Create a personalized travel itinerary using the user's
information and the available tools.

USER INFORMATION
----------------
Destination: {destination}
Number of days: {days}
Budget: ₹{budget}
Interests: {interests}

IMPORTANT INSTRUCTIONS
---------------------

1. Use the available tools when useful.
2. Use the weather tool to get weather information.
3. Use the places tool to discover attractions.
4. Use web search when current or specific information
   is needed.
5. Keep the total estimated spending within the user's budget.
6. Adapt the itinerary to the user's interests.
7. Do not invent tool results.

FORMAT YOUR FINAL ANSWER EXACTLY LIKE THIS:

✈️ AI TRAVEL PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 Destination: [destination]
📅 Duration: [number of days] days
💰 Budget: ₹[budget]
🎯 Interests: [interests]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌤️ WEATHER
[Give a short weather summary based on the weather tool.]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 BUDGET BREAKDOWN

• Accommodation: ₹...
• Food: ₹...
• Transportation: ₹...
• Activities: ₹...
• Emergency/Buffer: ₹...

Total Estimated Cost: ₹...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 DAY 1 — [location]

🏯 Places to Visit
• Place 1
• Place 2

🎯 Activities
• Activity 1
• Activity 2

🍜 Food
• Food recommendation

💰 Estimated Daily Cost: ₹...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 DAY 2 — [location]

🏯 Places to Visit
• ...

🎯 Activities
• ...

🍜 Food
• ...

💰 Estimated Daily Cost: ₹...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Continue this format for every day of the trip.

At the end, provide:

💡 TRAVEL TIPS
• Tip 1
• Tip 2
• Tip 3

⚠️ IMPORTANT NOTES
Mention any important limitations, uncertain prices,
weather considerations, transportation considerations,
or information that should be verified before booking.

Keep the answer useful and readable.
Do not include unnecessary explanations about how you
used the tools.
"""


result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
)


final_answer = result["messages"][-1].content

# Gemini may return the response as a list of content blocks
if isinstance(final_answer, list):
    final_answer = final_answer[0]["text"]


print("\n--- ✈️ AI Travel Plan ---")
print(final_answer)