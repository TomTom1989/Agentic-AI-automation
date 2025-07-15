## Goal
Automate writing and sending a cold sales email using a team of AI agents with added validation and guardrails.

## Flow Overview

1. **Setup**  
   - Loads SendGrid API key from a `.env` file.  
   - Prepares SSL certificates (to avoid email-sending errors).

2. **Email-Sending Functions**  
   Two tools are defined:  
   - send_email: sends plain text emails.  
   - send_html_email: sends emails in HTML format.

3. **Sales Agents**  
   Three different agent "personalities" (professional, humorous, concise).  
   Each generates a version of a cold sales email.

4. **Tools**  
   Each agent is converted into a tool so the sales manager can call them dynamically.

5. **Support Agents**  
   - subject_writer: generates a catchy subject line.  
   - html_converter: turns the plain email into HTML format.

6. **Email Manager Agent**  
   Takes the chosen email, generates a subject, converts it to HTML, and sends it using send_html_email.

7. **Sales Manager Agent**  
   Controls the full process:  
   - Tries all 3 email-writing tools.  
   - Picks the best email.  
   - Hands off the final message to the Email Manager, who finishes the job.

8. **Guardrails and Validation**  
   Before running the agent, an input guardrail (guardrail_against_name) checks for personal names in the message.  
   If a name is detected, execution is blocked.  
   This logic is supported by structured validation using a Pydantic model to ensure consistent output.

9. **Main Function**  
   Starts the whole system with a sample message:  
   “Send out a cold sales email addressed to Dear CEO from Tom”.  
   Traces execution for debugging and visibility on OpenAI trace viewer.

10. **Agentic Design Patterns Used**  
   - Agent as tool  
   - Tool orchestration  
   - Agent handoff  
   - Input guardrail  
   - Structured output (Pydantic)  
   - Trace-based debugging
