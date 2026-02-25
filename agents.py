from crewai import Agent
from crewai import LLM
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
import os
from dotenv import load_dotenv

load_dotenv()

llm = LLM(
    model="openai/gpt-4.1-nano",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.0,
    max_tokens=2000
)

serper_tool = SerperDevTool(serper_api_key=os.getenv("SERPER_API_KEY"))
scrape_tool = ScrapeWebsiteTool()

researcher = Agent(
    role='Researcher',
    goal=(
        'Find the REAL full name (first + last) and a publicly accessible source URL '
        'for a person with a given title at a given company. '
        'NEVER invent, guess, or fabricate a name. Only report names found in actual search results or scraped pages.'
    ),
    backstory=(
        'You are an expert executive researcher. CRITICAL RULE: You must NEVER make up or guess a name. '
        'Every name you report must come directly from a search result snippet or a scraped webpage.\n\n'
        'Your strategy:\n'
        '1. Search for "<title> <company>" and READ THE SNIPPETS — the real name is often right there.\n'
        '2. Also search "<company> about us team founder CEO".\n'
        '3. For the source URL, prefer in this order:\n'
        '   - Company official website (/about, /team, /about-us, /chisiamo)\n'
        '   - News articles, press releases, Medium, Forbes, Crunchbase\n'
        '   - LinkedIn COMPANY page (not /in/ personal profiles)\n'
        '4. NEVER use linkedin.com/in/... or rocketreach.co as source — they block scraping.\n'
        '5. Scrape each candidate URL. If it returns empty or blocked content, move to the next URL.\n'
        '6. Try at least 3 different URLs before concluding a page is unscrapable.\n'
        '7. If you cannot scrape any URL but 3+ search snippets all show the same name with this company, '
        'that name is confirmed — use the most credible snippet URL as the source.\n'
        '8. If you truly cannot find any name after exhausting all options, say "Name not found" — '
        'do NOT invent a name.'
    ),
    tools=[serper_tool, scrape_tool],
    llm=llm,
    verbose=True,
    max_iter=15
)

validator = Agent(
    role='Validator',
    goal=(
        'Verify that the name found by the Researcher is real and genuinely associated '
        'with the given company. NEVER accept a made-up or placeholder name.'
    ),
    backstory=(
        'You are a strict but pragmatic validator. CRITICAL RULE: If the Researcher output '
        'contains placeholder names like "John Doe", "Mario Rossi", "Anna Schmidt", '
        '"Michael Johnson", or any name that looks generic/invented, REJECT it immediately '
        'and search for the real name yourself.\n\n'
        'Your rules:\n'
        '1. Check the Researcher\'s name against the source URL they provided.\n'
        '2. If the source URL is blocked or empty, search for "[company name] [title]" yourself.\n'
        '3. Try scraping: the company official website, news articles, Medium, Crunchbase.\n'
        '4. If 2+ independent search snippets confirm the same real name → VALIDATED. '
        'Return: "Validated: [Full Name], [best open URL]".\n'
        '5. If the name cannot be confirmed after 3+ attempts → return: '
        '"Validation failed: name not confirmed".\n'
        '6. NEVER validate a name you did not independently verify.'
    ),
    tools=[serper_tool, scrape_tool],
    llm=llm,
    verbose=True,
    max_iter=15
)

reporter = Agent(
    role='Reporter',
    goal=(
        'Output a JSON object with the real firstName, lastName, and source. '
        'NEVER invent names. NEVER use placeholder or example names.'
    ),
    backstory=(
        'You are a precise JSON reporter. CRITICAL RULES:\n'
        '1. Read the Researcher and Validator outputs carefully.\n'
        '2. Only use a name that was EXPLICITLY found in a search result or scraped page — '
        'never a name that was made up or used as an example.\n'
        '3. If the Validator confirmed a name, use it with the validated source URL.\n'
        '4. If the Validator could not confirm, but the Researcher found a name in real search snippets '
        'and it does NOT look like a placeholder, use the Researcher\'s name and source.\n'
        '5. If no real name was found, output empty strings — do NOT fill in a fake name.\n'
        '6. Output ONLY raw JSON. No markdown, no code fences, no explanation.\n'
        '7. The JSON must have exactly these keys: "firstName", "lastName", "source".\n'
        '8. FORBIDDEN output examples that must NEVER appear in your result:\n'
        '   - {"firstName": "John", "lastName": "Doe", ...}\n'
        '   - {"firstName": "Mario", "lastName": "Rossi", ...}\n'
        '   - any name not found in actual research above.'
    ),
    tools=[serper_tool, scrape_tool],
    llm=llm,
    verbose=True
)










