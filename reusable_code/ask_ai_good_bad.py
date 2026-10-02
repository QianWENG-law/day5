def ask_ai_good_bad(question: str) -> bool:
    response = cllient.chat.completions.create(
        model="gpt-4o"
        messages={
            {"role": "system", "contect":"Answer strictly with a single"}
            {}
        }
    )