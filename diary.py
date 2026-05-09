import subprocess, os
from datetime import date
from pathlib import Path
import ollama
from config import REPO_PATH, MODEL, JOURNAL_DIR


def get_latest_commit_info():
    try:
        msg = subprocess.check_output(
            ["git", "log", "-1", "--pretty=%B"],
            cwd=REPO_PATH, text=True
        ).strip()

        files = subprocess.check_output(
            ["git", "diff", "HEAD~1", "HEAD", "--name-only"],
            cwd=REPO_PATH, text=True
        ).strip()

        diff = subprocess.check_output(
            ["git", "diff", "HEAD~1", "HEAD"],
            cwd=REPO_PATH, text=True
        )[:3000]

        return msg, files, diff

    except Exception:
        diff = subprocess.check_output(
            ["git", "show", "--stat", "HEAD"],
            cwd=REPO_PATH, text=True
        )[:3000]
        return "First commit", "Various files", diff


def write_journal_entry(commit_msg, files_changed, diff):
    prompt = f"""You are a thoughtful developer journal assistant.

A developer just made a commit.

Write a clean, insightful developer reflection in markdown format.

Keep it under 120 words.

Use this exact structure:

## Today's Progress
Explain what was built or changed.

## Patterns Noticed
Mention one coding habit or workflow pattern observed.

## Technical Debt or Risks
Mention one possible refactor need, risk, or bug.

## Tomorrow's Focus
Give one short improvement suggestion or encouragement.

## Focus Score
Give a score out of 10.

Commit message:
{commit_msg}

Files changed:
{files_changed}

Code diff:
{diff}

Write only the markdown journal entry.
"""
    print(f"\n[diary] Thinking with {MODEL}...\n")
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]


def save_entry(text):
    Path(JOURNAL_DIR).mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    filepath = Path(JOURNAL_DIR) / f"{today}.md"
    mode = "a" if filepath.exists() else "w"
    with open(filepath, mode) as f:
        if mode == "a":
            f.write("\n\n---\n\n")
        f.write(f"# {today}\n\n{text}\n")
    return filepath


def main():
    print("[diary] Reading your latest commit from:", REPO_PATH)
    msg, files, diff = get_latest_commit_info()
    print(f"[diary] Commit message: '{msg}'")
    entry = write_journal_entry(msg, files, diff)
    print("\n========== YOUR JOURNAL ENTRY ==========")
    print(entry)
    print("==========================================\n")
    saved = save_entry(entry)
    print(f"[diary] Saved to: {saved}")


if __name__ == "__main__":
    main()