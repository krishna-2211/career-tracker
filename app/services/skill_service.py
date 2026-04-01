def analyze_data(search_results: dict) -> list:
    context = "\n".join(r["snippet"] for r in search_results.get("results", []))
    query = search_results.get("query", "career role")

    prompt = f"List key skills for {query} from this text:\n{context}"

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        text = response.text.strip()
        return [s.strip() for s in text.replace("\n", ",").split(",") if s.strip()]

    except Exception as e:
        print("Error:", e)
        return ["LLM_ERROR"]


def extract_skills(search_results: dict) -> list:
    return analyze_data(search_results)