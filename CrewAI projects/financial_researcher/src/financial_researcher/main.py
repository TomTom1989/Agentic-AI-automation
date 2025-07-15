#!/usr/bin/env python
import sys
import warnings
import os

from datetime import datetime

from financial_researcher.crew import FinancialResearcher

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'company': 'OpenAI',  # The company to research
        'topic': 'AI LLMs',
        'current_year': str(datetime.now().year)
    }
    
    try:
        result = FinancialResearcher().crew().kickoff(inputs=inputs)
        print("\n\n=== FINAL REPORT ===\n\n")
        print(result.raw)
        
        # Create output directory if it doesn't exist
        os.makedirs('output', exist_ok=True)
        
        # Save the report to output/report.md
        with open('output/report.md', 'w', encoding='utf-8') as f:
            f.write(result.raw)
            
        print("\n\nReport has been saved to output/report.md")
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'company': 'OpenAI',  # The company to research
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        FinancialResearcher().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        FinancialResearcher().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'company': 'OpenAI',  # The company to research
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    
    try:
        FinancialResearcher().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    run()
