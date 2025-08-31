import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
You are a helpful AI data planner. 
Given a natural language query, available columns, and their datatypes, 
you will produce a **JSON plan** with one of the supported intents.

INTENTS:
1. "summary" → high-level overview of the data
2. "aggregate" → groupby + aggregation
3. "filter" → subset rows by conditions
4. "topk" → return top-k rows by some metric
5. "comparison" → compare metrics across categories

STRUCTURE:
{
  "intent": "aggregate" | "filter" | "summary" | "topk" | "comparison",
  "columns": [list of relevant columns],
  "metrics": { "col": "agg_func" },        # for aggregate/comparison
  "filters": [ {"column": col, "op": ">", "value": 100} ],  # optional
  "topk": { "k": 5, "by": "column", "order": "desc" },      # for topk intent
  "visualization": {
    "type": "bar" | "line" | "pie",
    "x": "column_for_x_axis",
    "y": "column_for_y_axis"
  }  # optional, only if user asks for a chart
}

NOTES:
- Always ensure valid JSON (no trailing commas, no comments).
- Use only available columns.
- Default to "summary" if query is vague.
- For "aggregate" or "comparison":
    * Always include at least one metric in "metrics".
    * Use valid Pandas functions only: sum, mean, count, min, max, median, std.
    * If multiple metrics, name them separately (e.g., {"Sales":"sum","Profit":"mean"}).
- Always output metrics with correct aggregation keys (e.g., "mean" instead of "avg").
- Ensure visualization "y" matches the aggregated column name (e.g., "Sales_sum").
- For "topk", wrap parameters inside the "topk" object.
- Only include "visualization" if explicitly useful (user requests chart).
"""



# ====== FUNCTION ======
def call_planner(user_query: str, columns: list, dtypes: dict) -> dict:
    """
    Convert user query into a JSON execution plan using Gemini.
    """
    try:
        # Add schema context
        col_context = f"Available columns: {columns}. Dtypes: {dtypes}."
        full_prompt = SYSTEM_PROMPT + "\n\nSchema: " + col_context + "\n\nQuestion: " + user_query

        # Call Gemini
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(full_prompt)

        raw_output = response.text.strip()

        # Extract only JSON part if extra text slips in
        match = re.search(r"\{.*\}", raw_output, re.DOTALL)  # Match the JSON object
        if match:
            raw_output = match.group(0)

        # Parse JSON
        try:
            plan = json.loads(raw_output)
        except json.JSONDecodeError:
            plan = {
                "intent": "error",
                "message": "Invalid JSON from model",
                "raw": raw_output
            }

        return plan

    except Exception as e:
        return {"intent": "error", "message": str(e)}
