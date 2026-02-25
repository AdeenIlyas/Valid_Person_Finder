from flask import Flask, render_template, request, jsonify
import json
from crew_runner import run_crew_for_query, process_excel_batch
import os

os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    company = data.get('company')
    designation = data.get('designation')

    if not company or not designation:
        return jsonify({"error": "Company and designation are required"}), 400

    try:
        result = run_crew_for_query(company, designation)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/batch', methods=['POST'])
def batch():
    try:
        results = process_excel_batch('Test data.xlsx')
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)