from crewai import Task
from agents import researcher, validator, reporter

def create_research_task(company, designation):
    return Task(
        description=f'Find the full name and a source URL for a person with the title "{designation}" at "{company}". You must find the first name, last name, and a valid source URL.',
        expected_output='A string containing the first name, last name, and source URL, separated by commas. Example: "John Doe, https://www.example.com"',
        agent=researcher
    )

def create_validate_task(company, designation):
    return Task(
        description=f'Validate the information for the person with the title "{designation}" at "{company}". Confirm the name and the source URL. The source URL must be a valid, publicly accessible webpage.',
        expected_output='A string containing the validated first name, last name, and source URL, separated by commas. If validation fails, return "Validation failed".',
        agent=validator
    )

def create_report_task(company, designation):
    return Task(
        description=f'Create a JSON report for the person with the title "{designation}" at "{company}". The report must contain "firstName", "lastName", and "source".',
        expected_output='A JSON object with the keys "firstName", "lastName", and "source". Example: \'{"firstName": "John", "lastName": "Doe", "source": "https://www.example.com"}\'',
        agent=reporter
    )