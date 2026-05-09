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
A developer just made a commit. Write a SHORT personal journal entry
(150 words) in first person as if the developer wrote it.

Include:
1. What they built or changed (1-2 sentences)
2. One habit or pattern you notice from the diff
3. **Technical Debt or Risks**: One thing that might need refactoring or a potential bug introduced.
4. One tip or encouragement for tomorrow
5. A focus score out of 10

Commit message: {commit_msg}
Files changed: {files_changed}
Code diff:
{diff}

Write the journal entry now. No preamble."""

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