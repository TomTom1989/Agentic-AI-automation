import os
from typing import Dict

import sendgrid
from sendgrid.helpers.mail import Email, Mail, Content, To
from agents import Agent, function_tool

@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """ Send an email with the given subject and HTML body """
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("tom@test.com") 
    to_email = To("tom@test.com") 
    content = Content("text/html", html_body)
    mail = Mail(from_email, to_email, subject, content).get()
    response = sg.client.mail.send.post(request_body=mail)
    print("Email response", response.status_code)
    return {"status": "success"}

INSTRUCTIONS = """You will receive a detailed report and are expected to send it as a well-formatted HTML email. Use your tool to convert the report into clean, visually appealing HTML, and send it in a single email with a suitable subject line."""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
)
