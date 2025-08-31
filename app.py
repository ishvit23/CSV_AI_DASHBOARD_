# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from helpers.ai_planner import call_planner
from helpers.executor import execute_plan

app = Flask(__name__)
CORS(app)  # allow all origins (for dev); for production restrict origins

UPLOADED_DF = None

@app.route('/upload', methods=['POST'])
def upload_file():
    global UPLOADED_DF
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file provided"}), 400
    try:
        df = pd.read_csv(file, encoding="utf-8", on_bad_lines="skip")
    except UnicodeDecodeError:
        file.seek(0)
        df = pd.read_csv(file, encoding="latin1", on_bad_lines="skip")
    UPLOADED_DF = df
    return jsonify({"message": "File uploaded successfully", "columns": UPLOADED_DF.columns.tolist()})

@app.route("/ask", methods=["POST"])
def ask():
    global UPLOADED_DF
    if UPLOADED_DF is None:
        return jsonify({"error": "No file uploaded"}), 400
    data = request.json or {}
    user_query = data.get("query", "")

    plan = call_planner(user_query, list(UPLOADED_DF.columns), UPLOADED_DF.dtypes.apply(lambda x: str(x)).to_dict())
    text, table, chart = execute_plan(UPLOADED_DF, plan)

    # normalize table to json-friendly structure
    table_json = None
    if isinstance(table, pd.DataFrame):
        table_json = table.reset_index(drop=True).to_dict(orient="records")
    elif isinstance(table, pd.Series):
        table_json = table.to_dict()
    elif table is not None:
        table_json = str(table)

    return jsonify({
        "plan": plan,
        "text": text,
        "table": table_json,
        "chart": chart  # chart is either dict or None
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
