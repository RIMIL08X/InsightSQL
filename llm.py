import re
import ollama
from db import get_schema
from prompts import SQL_PROMPT, EXPLANATION_PROMPT

# Hybrid Model Approach
SQL_MODEL = "deepseek-coder:6.7b"
EXP_MODEL = "mistral:7b-instruct-q4_K_M"

def clean_sql(sql: str) -> str:
    """Robust SQL extraction for DeepSeek."""
    if not sql or "CANNOT_ANSWER" in sql.upper():
        return "CANNOT_ANSWER"

    # Remove markdown blocks if the model ignored the 'No Markdown' rule
    sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"```", "", sql)

    # Fix 'ojoin' and other smushed keywords
    sql = re.sub(r"(\w)join", r"\1 JOIN", sql, flags=re.IGNORECASE)

    # Extract the actual query - search for SELECT until the end or semicolon
    match = re.search(r"(SELECT[\s\S]+)", sql, re.IGNORECASE)
    if match:
        query = match.group(1).strip()
        # Basic cleanup: remove trailing text if the model added it
        if ";" in query:
            query = query.split(";")[0] + ";"
        return query

    return sql.strip()

def nl_to_sql(question: str, db_url: str):
    schema = get_schema(db_url)
    prompt = SQL_PROMPT.format(schema=schema, question=question)

    response = ollama.chat(model=SQL_MODEL, messages=[{"role": "user", "content": prompt}])
    raw_sql = response["message"]["content"]

    print("\n--- RAW SQL OUTPUT ---\n", raw_sql) # Debugging is key
    return clean_sql(raw_sql)

def explain(question: str, result_list):
    """Uses Mistral for the human-like explanation."""
    prompt = EXPLANATION_PROMPT.format(question=question, result=str(result_list))

    response = ollama.chat(model=EXP_MODEL, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"].strip()
