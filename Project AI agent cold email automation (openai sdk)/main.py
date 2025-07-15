import os
import asyncio
import certifi
import sendgrid
from dotenv import load_dotenv
from typing import Dict
from sendgrid.helpers.mail import Mail, Email, To, Content
from agents import Agent, Runner, trace, function_tool, input_guardrail, GuardrailFunctionOutput
from openai.types.responses import ResponseTextDeltaEvent
from pydantic import BaseModel

# Set SSL cert path to avoid potential SSL errors
os.environ['SSL_CERT_FILE'] = certifi.where()

# Load environment variables from .env
load_dotenv(override=True)

# Define tools
@function_tool
def send_email(body: str) -> Dict[str, str]:
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("tom@test.com")
    to_email = To("tom@test.com")
    content = Content("text/plain", body)
    mail = Mail(from_email, to_email, "Sales email", content).get()
    response = sg.client.mail.send.post(request_body=mail)
    return {"status": "success"}

@function_tool
def send_html_email(subject: str, html_body: str) -> Dict[str, str]:
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("tom@test.com")
    to_email = To("tom@test.com")
    content = Content("text/html", html_body)
    mail = Mail(from_email, to_email, subject, content).get()
    response = sg.client.mail.send.post(request_body=mail)
    return {"status": "success"}

# Structured output for name checking
class NameCheckOutput(BaseModel):
    is_name_in_message: bool
    name: str

# Guardrail agent to check for personal names
guardrail_agent = Agent(
    name="Name check",
    instructions="Check if the user is including someone's personal name in what they want you to do.",
    output_type=NameCheckOutput,
    model="gpt-4o-mini"
)

@input_guardrail
async def guardrail_against_name(ctx, agent, message):
    result = await Runner.run(guardrail_agent, message, context=ctx.context)
    is_name_in_message = result.final_output.is_name_in_message
    return GuardrailFunctionOutput(output_info={"found_name": result.final_output}, tripwire_triggered=is_name_in_message)

# Sales agent instructions
instructions1 = "As a professional sales representative at ComplAI, your job is to craft cold outreach emails that are formal, polished, and clearly communicate the value of our AI-driven SOC2 compliance platform."
instructions2 = "As an outgoing and witty sales rep at ComplAI, your cold outreach emails should be charming and funny while still getting across how our AI tool helps companies with SOC2 compliance and audit readiness."
instructions3 = "As a no-nonsense sales agent at ComplAI, your cold emails are brief, direct, and efficient—quickly showing how our AI platform simplifies SOC2 compliance."

# Agents
sales_agent1 = Agent(name="Professional Sales Agent", instructions=instructions1, model="gpt-4o-mini")
sales_agent2 = Agent(name="Engaging Sales Agent", instructions=instructions2, model="gpt-4o-mini")
sales_agent3 = Agent(name="Busy Sales Agent", instructions=instructions3, model="gpt-4o-mini")

# Convert to tools
tool1 = sales_agent1.as_tool(tool_name="sales_agent1", tool_description="Write a cold sales email")
tool2 = sales_agent2.as_tool(tool_name="sales_agent2", tool_description="Write a cold sales email")
tool3 = sales_agent3.as_tool(tool_name="sales_agent3", tool_description="Write a cold sales email")

# Subject and HTML agents
subject_writer = Agent(name="Email subject writer", instructions="You can write a subject...", model="gpt-4o-mini")
subject_tool = subject_writer.as_tool(tool_name="subject_writer", tool_description="Write a subject for a cold sales email")

html_converter = Agent(name="HTML email body converter", instructions="You can convert a text email...", model="gpt-4o-mini")
html_tool = html_converter.as_tool(tool_name="html_converter", tool_description="Convert a text email body to an HTML email body")

# Email Manager agent
emailer_agent = Agent(
    name="Email Manager",
    instructions="You receive the body of an email to be sent...",
    tools=[subject_tool, html_tool, send_html_email],
    model="gpt-4o-mini",
    handoff_description="Convert an email to HTML and send it"
)

# Final sales manager with input guardrail
sales_manager_instructions = "You are a sales manager working for ComplAI. You use the tools given to you to generate cold sales emails. You never generate sales emails yourself; you always use the tools. You try all 3 sales agent tools at least once before choosing the best one. You can use the tools multiple times if you're not satisfied with the results from the first try. You select the single best email using your own judgement of which email will be most effective. After picking the email, you hand off to the Email Manager agent to format and send the email."

sales_manager = Agent(
    name="Sales Manager",
    instructions=sales_manager_instructions,
    tools=[tool1, tool2, tool3],
    handoffs=[emailer_agent],
    model="gpt-4o-mini",
    input_guardrails=[guardrail_against_name]
)

# Main execution logic
async def main():
    message = "Send out a cold sales email addressed to Dear CEO from Tom"
    with trace("Protected Automated SDR"):
        result = await Runner.run(sales_manager, message)
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
