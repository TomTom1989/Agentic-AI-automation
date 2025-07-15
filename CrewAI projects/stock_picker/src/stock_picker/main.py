#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime

from stock_picker.crew import StockPicker

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the research crew.
    """
    inputs = {
        'sector': 'Technology',
        'topic': 'Technology Stocks',
        "current_date": str(datetime.now()),
        'current_year': str(datetime.now().year)
    }

    # Create and run the crew
    result = StockPicker().crew().kickoff(inputs=inputs)

    # Print the result
    print("\n\n=== FINAL DECISION ===\n\n")
    print(result.raw)

    # Create output directory if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Define output file path
    output_file = os.path.join(output_dir, "decision.md")

    # Save the result to a markdown file
    with open(output_file, "w") as f:
        f.write(result.raw)

    print(f"\nReport has been saved to {output_file}")


if __name__ == "__main__":
    run()
