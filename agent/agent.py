import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import re

# Load environment variables from .env file
load_dotenv()

# Set up the language model (OpenRouter with GPT-3.5-turbo)
llm = ChatOpenAI(
    temperature=0.7,
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    model_name="openai/gpt-3.5-turbo",
    base_url="https://openrouter.ai/api/v1"
)

# Define the prompt structure that guides the assistant
PROMPT_TEMPLATE = """
You are a daily reflection and planning assistant. Your goal is to:
1. Reflect on the user's journal and dream input
2. Interpret the user's emotional and mental state
3. Understand their intention and 3 priorities
4. Generate a practical, energy-aligned strategy for their day

INPUT:
Morning Journal: {journal}
Intention: {intention}
Dream: {dream}
Top 3 Priorities: {priorities}

OUTPUT:
1. Inner Reflection Summary
2. Dream Interpretation Summary
3. Energy/Mindset Insight
4. Suggested Day Strategy (time-aligned tasks)
"""

def process_inputs(journal, dream, intention, priorities):
    # Format the prompt with user input
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    messages = prompt.format_messages(
        journal=journal,
        dream=dream,
        intention=intention,
        priorities=priorities
    )

    # Send the prompt to the model and get the result
    result = llm.invoke(messages)
    content = result.content

    # Split the response into different sections using numbered headings
    sections = re.split(r'\n?\s*\d\.\s+', content)
    labels = ["", "Inner Reflection", "Dream Interpretation", "Mindset Insight", "Suggested Day Strategy"]

    # Map each section to its label
    output = {}
    for i in range(1, min(len(sections), len(labels))):
        output[labels[i]] = sections[i].strip()

    # Combine the first three sections into a reflection summary
    reflection = "\n\n".join([
        f"### {label}\n{output[label]}"
        for label in ["Inner Reflection", "Dream Interpretation", "Mindset Insight"]
        if label in output
    ])

    # Get the strategy section separately
    strategy = output.get("Suggested Day Strategy", "⚠️ Strategy section not found.")

    return reflection, strategy
