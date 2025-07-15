# Financial Researcher AI Crew

An AI-powered research crew that analyzes and generates comprehensive reports on financial topics using CrewAI framework.

## 🚀 Features

- **AI-Powered Research**: Utilizes advanced language models to conduct thorough financial research
- **Automated Report Generation**: Creates detailed markdown reports with structured analysis
- **Customizable Inputs**: Configurable research topics and parameters
- **Output Management**: Automatically saves reports to an organized output directory

## 🛠️ Technical Stack

- **Framework**: [CrewAI](https://github.com/joaomdmoura/crewAI) - For orchestrating role-playing AI agents
- **Language Model**: OpenAI GPT-4o-mini - For intelligent analysis and report generation
- **Environment Management**: Python virtual environment with dependency management
- **Configuration**: YAML-based agent and task configurations

=============WORKFLOW============================================================
## 🔄 Agent Workflow

1. **Research Agent**:
   - Role: Senior Financial Researcher
   - Receives the research topic
   - Gathers comprehensive data about the company
   - Compiles initial research findings
   - Passes findings to the Analyst Agent

2. **Analyst Agent**:
   - Role: Market Analyst and Report Writer
   - Receives research findings
   - Performs in-depth analysis
   - Creates comprehensive report
   - Structures information in markdown format
   - Saves final report to `output/report.md`
===================================================================================================

## 🚀 Getting Started

### Prerequisites

- Python 3.12 or higher
- OpenAI API key

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd financial_researcher
   ```

2. Create and activate virtual environment:
   ```bash
   crewai create crew financial_researcher
   cd financial_researcher
   crewai install
   ```

3. Set up environment variables:
   - Create a `.env` file in the project root
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

### Running the Project

Execute the research crew:
```bash
python -m financial_researcher.main
```

The generated report will be saved to `output/report.md`.

## 🔧 Configuration

### Customizing Research Topics

Modify the `inputs` dictionary in `main.py`:
```python
inputs = {
    'topic': 'Your Research Topic',
    'current_year': str(datetime.now().year)
}
```

### Agent Configuration

Edit `config/agents.yaml` to customize:
- Agent roles
- Capabilities
- Behavior parameters

### Task Configuration

Edit `config/tasks.yaml` to modify:
- Research objectives
- Task sequences
- Output requirements

## 📝 Output

The project generates comprehensive markdown reports including:
- Executive summary
- Detailed analysis
- Key findings
- Recommendations

Reports are automatically saved to the `output` directory.

## 🔐 Security

- API keys are stored in `.env` file (not tracked in git)
- Virtual environment isolates project dependencies
- Secure handling of sensitive financial data
