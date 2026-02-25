import os
import json
import pandas as pd
from crewai import Crew
from dotenv import load_dotenv
from agents import researcher, validator, reporter
from tasks import create_research_task, create_validate_task, create_report_task

load_dotenv()

def run_crew_for_query(company, designation):
    research_task = create_research_task(company, designation)
    validate_task = create_validate_task(company, designation)
    report_task = create_report_task(company, designation)

    crew = Crew(
        agents=[researcher, validator, reporter],
        tasks=[research_task, validate_task, report_task],
        verbose=True
    )

    result = crew.kickoff().raw
    return json.loads(result) 

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

    with open('results.json', 'w') as f:
        json.dump(results, f, indent=4)
    print("Batch processing complete. Results in results.json")
    return results

if __name__ == "__main__":
    # Example single query
    # example_company = "Facebook"
    # example_designation = "CEO"
    # print(f"Running example: {example_company} {example_designation}")
    # result = run_crew_for_query(example_company, example_designation)
    # print(json.dumps(result, indent=4))
    process_excel_batch()


