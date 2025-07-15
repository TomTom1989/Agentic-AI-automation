from pydantic import BaseModel, Field
from agents import Agent

INSTRUCTIONS = (
    "You are a senior researcher responsible for producing a comprehensive report based on a research query. "
    "You will receive the original query along with preliminary findings gathered by a research assistant.\n"
    "Begin by outlining the structure and logical flow of the report. After finalizing the outline, write the full report.\n"
    "The final deliverable should be written in markdown format and should be thorough and well-developed. "
    "Target a length of 5–10 pages, with a minimum of 1000 words. "
    "Return your answer as JSON in the following format: "
    '{"short_summary": "...", "markdown_report": "...", "follow_up_questions": ["...", "...", "..."]}'
)



class ReportData(BaseModel):
    short_summary: str = Field(description="A short 2-3 sentence summary of the findings.")

    markdown_report: str = Field(description="The final report")

    follow_up_questions: list[str] = Field(description="Suggested topics to research further")


writer_agent = Agent(
    name="WriterAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ReportData,
)