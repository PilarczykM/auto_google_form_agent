import yaml
from crewai import Agent, Crew, Task

from config.project_paths import PROMPTS_DIRECTORY


def _load_prompts(language: str) -> dict:
    lang_code = language.lower()[:2]  # 'en'
    path = PROMPTS_DIRECTORY / f"{lang_code}.yaml"

    if not path.exists():
        msg = f"No prompt file found for language: {language}"
        raise ValueError(msg)

    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def create_form_crew(question: str, traits: list[str], language: str) -> Crew:
    prompts = _load_prompts(language)
    inputs = {
        "question": question,
        "traits": ", ".join(traits),
        "language": language
    }

    form_agent = Agent(
        role=prompts["form_agent"]["role"],
        goal=prompts["form_agent"]["goal"].format(**inputs),
        backstory=prompts["form_agent"]["backstory"].format(**inputs),
        allow_delegation=False,
        verbose=True,
    )

    answer_task = Task(
        description=prompts["form_response_task"]["description"].format(**inputs),
        expected_output=prompts["form_response_task"]["expected_output"],
        agent=form_agent,
    )

    return Crew(
        agents=[form_agent],
        tasks=[answer_task],
        verbose=True
    )