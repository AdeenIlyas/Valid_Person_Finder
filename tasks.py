from crewai import Task
from agents import researcher, validator, reporter

def create_research_task(company, designation):
    return Task(
        description=(
            f'Find the REAL full name and a publicly accessible source URL for the person '
            f'with the title "{designation}" at "{company}".\n\n'
            f'STRICT RULES:\n'
            f'- NEVER invent, guess, or fabricate a name. Only report a name you actually saw in a snippet or scraped page.\n'
            f'- If you cannot find the name, say "Name not found" — do not fill in a placeholder.\n\n'
            f'STRATEGY:\n'
            f'Step 1: Search for "{designation} {company}" — read every snippet carefully for a real person\'s name.\n'
            f'Step 2: Search for "{company} about us" or "{company} team" to find the official website.\n'
            f'Step 3: Scrape the company official website first (/about, /team, /about-us). '
            f'If empty/blocked, try a news article or press release mentioning the person. '
            f'If still blocked, try Medium, Crunchbase, or any open blog.\n'
            f'Step 4: SKIP linkedin.com/in/... and rocketreach.co — they always block scraping.\n'
            f'Step 5: Try at least 3 different URLs. If none load but 3+ snippets show the same name, '
            f'that name is real — use the snippet\'s URL as source.\n'
            f'Step 6: Return the name you found and the URL where it was confirmed.'
        ),
        expected_output=(
            'The REAL full name of the person and the URL where it was confirmed, both found through actual research. '
            'If not found, state "Name not found". Do NOT use placeholder names.'
        ),
        agent=researcher
    )

def create_validate_task(company, designation):
    return Task(
        description=(
            f'Validate the name found by the Researcher for the "{designation}" at "{company}".\n\n'
            f'STRICT RULES:\n'
            f'- NEVER validate a name you did not independently verify.\n'
            f'- If the Researcher said "Name not found", search for the name yourself before giving up.\n'
            f'- Reject any name that looks like a placeholder (e.g. generic Western names with no evidence).\n\n'
            f'STEPS:\n'
            f'1. Read the Researcher\'s output for the name and source URL.\n'
            f'2. Scrape the source URL. If it confirms the name → VALIDATED.\n'
            f'3. If the URL is blocked/empty: search for "{company} {designation}" yourself, '
            f'then try scraping the company website, a news article, or Crunchbase.\n'
            f'4. If 2+ search snippets independently confirm the same name with this company → VALIDATED.\n'
            f'5. Return exactly: "Validated: [Full Name], [source URL]" '
            f'OR "Validation failed: name not confirmed".'
        ),
        expected_output=(
            '"Validated: [Real Full Name], [working source URL]" '
            'OR "Validation failed: name not confirmed". No placeholders, no invented names.'
        ),
        agent=validator,
        context=[]
    )

def create_report_task(company, designation):
    return Task(
        description=(
            f'Create a JSON report for the "{designation}" at "{company}".\n\n'
            f'STRICT RULES:\n'
            f'- Read ALL outputs from the Researcher and Validator above.\n'
            f'- ONLY use a name that was explicitly found in real research — never a guessed or example name.\n'
            f'- If the Validator confirmed a name, use it with the validated source URL.\n'
            f'- If Validator failed but Researcher found a real name (visible in snippets/scraped page), use that.\n'
            f'- If no real name was found anywhere, output empty strings for all fields.\n'
            f'- Split the full name into firstName and lastName.\n\n'
            f'OUTPUT FORMAT: Raw JSON only — no markdown, no code fences, no extra text.\n'
            f'{{"firstName": "<real first name or empty>", "lastName": "<real last name or empty>", "source": "<real URL or empty>"}}'
        ),
        expected_output=(
            'A raw JSON object with keys "firstName", "lastName", "source" containing only real researched data. '
            'Empty strings if nothing was found. No markdown, no invented names.'
        ),
        agent=reporter,
        context=[]
    )