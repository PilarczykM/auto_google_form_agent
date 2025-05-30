from crewai import Agent, Crew, Task

from utils.yaml_utils import load_prompts


def create_form_crew(language: str, llm=None) -> Crew:
    """Create a Crew instance configured to generate a form-based response based on a question and traits.

    This function initializes an agent with a specific role, goal, and backstory derived from
    language-specific prompts. It also defines a task for the agent to perform, and returns a
    Crew instance composed of the agent and task.

    Parameters
    ----------
    language : str
        The language code to determine which prompt templates to use.
    llm: Any
        The llm to use.

    Returns
    -------
    Crew
        An instance of the `Crew` class containing the configured agent and task.

    """
    prompts = load_prompts(language)

    form_agent = Agent(
        role=prompts["form_agent"]["role"],
        goal=prompts["form_agent"]["goal"],
        backstory=prompts["form_agent"]["backstory"],
        allow_delegation=False,
        verbose=True,
        llm=llm,
    )

    answer_task = Task(
        description=prompts["form_response_task"]["description"],
        expected_output=prompts["form_response_task"]["expected_output"],
        agent=form_agent,
    )

    return Crew(agents=[form_agent], tasks=[answer_task], verbose=True)


def create_bio_generator_crew(language: str, llm=None) -> Crew:
    """Create a Crew instance that generates a fictional IT professional's biography.

    This function sets up a CrewAI agent and task designed to generate a short, structured biography
    of an IT professional. The biography includes traits such as age, gender, specialization,
    years of experience, key technologies, and communication style. The agent's behavior and prompts
    are dynamically loaded based on the specified language.

    Parameters
    ----------
    language : str
        Language code (e.g., "en", "pl") determining the prompt language and output language of the biography.
    llm: Any
        The llm to use.

    Returns
    -------
    Crew
        A Crew instance with one agent (`bio_generator_agent`) and one task (`bio_generation_task`)
        responsible for generating a single, personality-rich IT biography.

    """
    prompts = load_prompts(language)

    bio_generator_agent = Agent(
        role=prompts["bio_generator_agent"]["role"],
        goal=prompts["bio_generator_agent"]["goal"],
        backstory=prompts["bio_generator_agent"]["backstory"],
        allow_delegation=False,
        verbose=True,
        llm=llm,
    )

    bio_generation_task = Task(
        description=prompts["generate_bio_task"]["description"],
        expected_output=prompts["generate_bio_task"]["expected_output"],
        agent=bio_generator_agent,
    )

    return Crew(agents=[bio_generator_agent], tasks=[bio_generation_task], verbose=True)
