## Project Summary: Stock Picker AI Crew

This project is an AI-powered crew designed to identify promising stock investment opportunities within a specified market sector. It automates the process of scanning financial news, researching trending companies, and recommending a top stock pick based on the collected information and analysis.

**Key Features:**

- **Automated News Analysis:** Scans recent financial news to find trending companies.
- **In-depth Company Research:** Conducts detailed analysis of identified trending companies.
- **Intelligent Stock Selection:** Recommends the best stock for investment based on research findings.
- **Detailed Reporting:** Generates a comprehensive report summarizing the analysis and decision.
- **Customizable Input:** Allows specifying the market sector and relevant topic for the search.

**Agent Workflow Scenario:**

The `stock_picker` crew orchestrates a series of specialized AI agents to achieve its goal. Here's the typical flow of tasks and information between the agents:

1.  **Trending Company Finder Agent:**
    *   **Role:** Financial News Analyst.
    *   **Action:** This agent is the first to act. It takes the provided `sector` (e.g., 'Technology') and `topic` (e.g., 'Technology Stocks') and scours the latest financial news.
    *   **Output:** Identifies and provides a list of 2-3 companies that are currently trending in the news within the specified sector.
    *   **Passes to:** Financial Researcher Agent.

2.  **Financial Researcher Agent:**
    *   **Role:** Senior Financial Researcher.
    *   **Action:** Receives the list of trending companies from the Trending Company Finder. It then conducts a more in-depth online research for each company on the list.
    *   **Output:** Compiles a detailed analysis and report for each trending company, providing comprehensive insights.
    *   **Passes to:** Stock Picker Agent.

3.  **Stock Picker Agent:**
    *   **Role:** Stock Picker from Research.
    *   **Action:** Receives the detailed research reports for the trending companies from the Financial Researcher. It analyzes these reports, synthesizing the information to evaluate the investment potential of each company.
    *   **Output:** Selects the single best company for investment based on its analysis. It then generates a final report that includes its chosen company, the rationale for the selection, and explanations for why other companies were not chosen.
    *   **Saves Output:** The final decision report is saved to `output/decision.md`.

**Inputs:**

The project requires the following inputs, typically set in the `main.py` file:
-   `sector`: The broad market sector to focus the search (e.g., 'Technology').
-   `topic`: A more specific topic related to the sector (e.g., 'Technology Stocks').
-   `current_date`: The current date (used by agents for context).
-   `current_year`: The current year (used by agents for context).

**Output:**

-   A Markdown file (`output/decision.md`) containing the final stock pick decision and the supporting research and analysis.