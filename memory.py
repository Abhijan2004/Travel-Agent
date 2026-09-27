import json
import os
from langchain_core.tools import tool

MEMORY_FILE = "memory.json"

DEFAULT_MEMORY = {
    "travel_style": "",
    "interests": [],
    "food_preferences": "",
    "budget_preference": "",
    "dislikes": []
}


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return DEFAULT_MEMORY.copy()

    with open(MEMORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_memory(
    travel_style=None,
    interests=None,
    food_preferences=None,
    budget_preference=None,
    dislikes=None
):
    memory = load_memory()

    if travel_style:
        memory["travel_style"] = travel_style

    if interests:
        memory["interests"] = interests

    if food_preferences:
        memory["food_preferences"] = food_preferences

    if budget_preference:
        memory["budget_preference"] = budget_preference

    if dislikes:
        memory["dislikes"] = dislikes

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=4)


def get_memory():
    return load_memory()


if __name__ == "__main__":
    save_memory(
        travel_style="solo",
        interests=["cars", "history"],
        food_preferences="local food",
        dislikes=["crowded places"]
    )

    print(get_memory())
    
@tool
def save_user_preference(
    travel_style: str = "",
    interests: str = "",
    food_preferences: str = "",
    budget_preference: str = "",
    dislikes: str = ""
) -> str:
    """
    Save the user's travel preferences for future trips.
    Call this when the user provides a new personal travel preference.
    """

    memory = load_memory()

    if travel_style:
        memory["travel_style"] = travel_style

    if interests:
        memory["interests"] = [
            item.strip()
            for item in interests.split(",")
            if item.strip()
        ]

    if food_preferences:
        memory["food_preferences"] = food_preferences

    if budget_preference:
        memory["budget_preference"] = budget_preference

    if dislikes:
        memory["dislikes"] = [
            item.strip()
            for item in dislikes.split(",")
            if item.strip()
        ]

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=4)

    return "User preference saved successfully."