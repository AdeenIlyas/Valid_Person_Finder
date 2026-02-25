import os
import json
import pandas as pd
import time
from crewai import Crew
from dotenv import load_dotenv
from agents import researcher, validator, reporter
from tasks import create_research_task, create_validate_task, create_report_task

load_dotenv()

def run_crew_for_query(company, designation):
    research_task = create_research_task(company, designation)
    validate_task = create_validate_task(company, designation)
    report_task = create_report_task(company, designation)

    # Wire context: validator sees researcher output; reporter sees both
    validate_task.context = [research_task]
    report_task.context = [research_task, validate_task]

    crew = Crew(
        agents=[researcher, validator, reporter],
        tasks=[research_task, validate_task, report_task],
        verbose=True
    )

    raw = crew.kickoff().raw

    # Strip markdown code fences if the LLM wraps the JSON
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Try to extract the first JSON object from the output
        import re
        match = re.search(r'\{.*?\}', raw, re.DOTALL)
        if match:
            return json.loads(match.group())
        return {"firstName": "", "lastName": "", "source": f"Parse error: {raw[:200]}"}

def process_excel_batch(file_path='Test data.xlsx'):
    df = pd.read_excel(file_path)
    results = []
    for index, row in df.iterrows():
        designation = row['Title']
        company = row['Company Name']
        if pd.isna(company) or pd.isna(designation):
            results.append({"Title": designation, "Company Name": company, "First Name": "", "Last Name": "", "Source": "Skipped - Missing Data"})
            continue
        print(f"Processing: {company} - {designation}")
        try:
            result = run_crew_for_query(company, designation)
            processed_result = {
                "Title": designation,
                "Company Name": company,
                "First Name": result.get("firstName", ""),
                "Last Name": result.get("lastName", ""),
                "Source": result.get("source", "")
            }
            results.append(processed_result)
        except Exception as e:
            results.append({"Title": designation, "Company Name": company, "First Name": "", "Last Name": "", "Source": f"Error: {e}"})

        time.sleep(10) # Add a 2-second delay to avoid rate limiting

    with open('results.json', 'w') as f:
        json.dump(results, f, indent=4)
    print("Batch processing complete. Results in results.json")
    return results

if __name__ == "__main__":
    process_excel_batch()


