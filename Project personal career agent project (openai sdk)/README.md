Agentic AI: Personal Career Representative Chatbot
This project is a lightweight agent-style chatbot designed to act as my personal career assistant. It uses an LLM (GPT-4o-mini via the OpenAI SDK), Gradio for the frontend, and integrates tool-calling for logging contact interest and unanswered questions. The goal is to simulate real-time, professional conversations while representing my background and experience.

Overview:
The chatbot acts as a digital representative of me (Thomas Walciszewski), answering questions related to my career, qualifications, and work history. If the user asks something outside the chatbot’s scope, it logs the unknown question. If a user seems interested in further contact, it records their name, email, and any notes. I receive these events through Pushover notifications in real time.

1) The agent is built using:

	1. The OpenAI SDK (openai>=1.0) with Python

	2. GPT-4o-mini model with function calling for tools

	3. async-style control loop for handling multi-step interactions

	4. Gradio's ChatInterface() for the frontend, supporting local and public access links

2) Key Features:
	1. Agent behavior is driven by a structured system prompt simulating me

	2. Reads and uses text from a PDF (LinkedIn export) and a text-based career summary

	3. Uses function calling to:

		a. Record email/contact details

		b. Log unknown or unhandled questions

	4. Runs in a Gradio interface that launches both locally and via a public shareable URL (using Yield keyword in Python code for the gradio UI progressive streaming experience)

	5. Handles tool calls inside a controlled message-processing loop

	6. Uses .env for managing sensitive data (OpenAI key, Pushover credentials)

	7. Can be extended to support additional tools, knowledge sources, or channels




