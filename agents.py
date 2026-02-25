from crewai import Agent
from crewai import LLM
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
import os
from dotenv import load_dotenv

load_dotenv()

llm = LLM(
    model = "openai/gpt-4.1-nano",
    # model="gemini/gemini-2.5-flash",
    api_key=os.getenv("OPENAI_API_KEY"), 
    temperature=0.2,
    max_tokens=1600
)

serper_tool = SerperDevTool(serper_api_key=os.getenv("SERPER_API_KEY"))
scrape_tool = ScrapeWebsiteTool()

researcher = Agent(
    role='Researcher',
    goal='Find the full name and a source URL for a person with a given title and company. You must find the first name, last name, and a valid source URL.',
    backstory='You are an expert in finding executive names and their source. You are a master at crafting search queries to locate this information. You must provide the first name, last name, and a source URL. Do not give up until you find all three pieces of information.',
    tools=[serper_tool, scrape_tool],
    llm=llm,
    verbose=True
)

validator = Agent(
    role='Validator',
    goal='Verify the accuracy of the name and source URL provided by the researcher. You must confirm that the person is associated with the company.',
    backstory='You are a meticulous validator. You cross-reference the information provided by the researcher with other sources to ensure its accuracy. You must confirm that the person is associated with the company and that the source URL is valid. You will be given a name and a source, and you must validate them.',
    tools=[serper_tool, scrape_tool],
    llm=llm,
    verbose=True
)

reporter = Agent(
    role='Reporter',
    goal='Create a JSON report with the validated information. The JSON object must contain "firstName", "lastName", and "source".',
    backstory='You are a JSON expert. You take the validated information and format it into a clean JSON object. The JSON object must have the keys "firstName", "lastName", and "source". Do not include any other information or keys. If you cannot find the information, you must return a JSON object with empty strings for the values.',
    llm=llm,
    verbose=True
)










