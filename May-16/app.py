import autogen
import google.generativeai as genai
import os

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Get the absolute path to the web directory
current_dir = os.path.dirname(os.path.abspath(__file__))
web_dir = os.path.join(current_dir, 'web')

config_list = [
    {
        'model': 'gemini-1.5-flash',
        'api_key': os.getenv("GOOGLE_API_KEY"),
        'base_url': 'https://generativelanguage.googleapis.com/v1beta/models',
        'api_type': 'google'
    }
]

llm_config = {
    "config_list": config_list,
    "temperature": 0,
    "seed": 42
}

assistant = autogen.AssistantAgent(
    name="CTO",
    llm_config=llm_config,
    system_message="Chief technical officer of a tech company"
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": web_dir, "use_docker": False},
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)

task = """
Write python code to output numbers 1 to 100
"""

user_proxy.initiate_chat(
    assistant,
    message=task
)

