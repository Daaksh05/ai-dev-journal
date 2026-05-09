# AI Dev Journal 📓

An automated developer journaling system that turns your Git commits into thoughtful, AI-generated journal entries and weekly insight reports.

## Features
- **Daily Journaling**: Automatically analyzes your latest commit and generates a first-person journal entry.
- **Weekly Insights**: Compiles daily entries into a structured report with patterns, blind spots, and a learning plan.
- **Local AI**: Uses [Ollama](https://ollama.ai/) with the `qwen3:8b` model for private, local processing.

## Setup

1. **Install dependencies**:
   ```bash
   pip install ollama
   ```

2. **Configure**:
   Update `config.py` with your repository path and desired Ollama model.

3. **Usage**:
   - Run `python diary.py` after a commit to generate a daily entry.
   - Run `python weekly_report.py` to generate your weekly insight report.

## Technology Stack
- Python
- Git
- Ollama (LLM: qwen3:8b)
