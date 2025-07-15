from agents import Agent, WebSearchTool, ModelSettings

INSTRUCTIONS = (
    "You are a research assistant. Given a search term, search the web and generate a concise "
    "summary of the findings. The summary should be 2–3 paragraphs long and under 300 words. "
    "Focus on the key takeaways—brevity is important. Full sentences and perfect grammar are not required. "
    "This summary will be used to support a larger report, so prioritize essential information and omit any fluff. "
    "Do not include personal commentary—only the summary itself."
)


search_agent = Agent(
    name="Search agent",
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool(search_context_size="low")],
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required"),
)