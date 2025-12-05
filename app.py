import ollama
import requests
from flask import Flask, jsonify

app = Flask(__name__)

DATA_ENDPOINT = "https://fonteyn.cloud/api/dashboard"
CHAT_MODEL = "phi3"
SYSTEM_PROMPT = """You are a senior business analyst AI assistant.
Your task is to analyze a JSON object containing a company's sales and logistics
data and provide a concise report of key insights for an internal sprint review. 
The report should be easy to understand for a non-technical audience.

Please provide a report that covers the following points:

1.  **Overall Performance:** Briefly summarize the company's performance based on the key metrics (total offers, total orders, conversion rate, revenue, etc.).
2.  **Sales Team Performance:** Analyze the performance of the top and bottom salesmen. Are there any significant discrepancies? What could be the reasons for the performance differences?
3.  **Geographical Performance:** Analyze the performance of the top and bottom countries. Are there any surprises? Are there any untapped markets?
4.  **Sales Trends:** Analyze the `salesData` to identify any trends, patterns, or anomalies in revenue over time.
5.  **Actionable Recommendations:** Based on your analysis, provide at least three actionable recommendations for the business to consider. These could be related to improving sales, optimizing logistics, or exploring new opportunities.

Your report should be structured, insightful, and focus on the 'why' behind the numbers, not just the 'what'.

Use the following JSON data:
<PLACEHOLDER_FOR_JSON_DATA>
"""

@app.route('/')
def home():
    return jsonify({"message": "BAS AI API is running."})

@app.route('/chat')
def chat():
    try:
        user_input = requests.get(DATA_ENDPOINT).json()
    except Exception as e:
        return jsonify({"error": f"Failed to fetch data: {str(e)}"}), 500
    

    sys_prompt = SYSTEM_PROMPT.replace("<PLACEHOLDER_FOR_JSON_DATA>", str(user_input))

    # Generate Response via Ollama
    # We use stream=False here for a simpler HTTP response, 
    try:
        response = ollama.chat(
            model=CHAT_MODEL,
            messages=[
                {'role': 'system', 'content': sys_prompt},
                {'role': 'user', 'content': "Please analyze the data and generate the report as instructed."}
            ]
        )
        ai_message = response['message']['content']
        
        return jsonify({
            "response": ai_message
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)