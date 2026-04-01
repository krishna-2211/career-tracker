from google import genai
import os

client = genai.Client()

def analyze_data(search_results: dict) -> list:
    combined_text = "\n".join(r["snippet"] for r in search_results.get("results", []))
    role_query = search_results.get("query", "career role")

    prompt = f"""
    You are a career advisor.

    Based on the following data for '{role_query}', extract ONLY a list of key skills.
    Return them as a comma-separated list.

    Data:
    {combined_text}
    """

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        if not response.text:
            raise Exception("Empty response from LLM")

        raw_text = response.text.strip()

        skills = [
            skill.strip()
            for skill in raw_text.replace("\n", ",").split(",")
            if skill.strip()
        ]

        print("✅ LLM RESPONSE:", skills)  # Debug log

        return skills

    except Exception as e:
        print("❌ LLM ERROR:", e)

        # HARD fallback (only if API fails)
        return ["LLM_ERROR"]