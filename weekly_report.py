from pathlib import Path
import ollama
from config import MODEL, JOURNAL_DIR


def load_all_entries():
    journal_path = Path(JOURNAL_DIR)
    if not journal_path.exists():
        return ""
    entries = []
    for md_file in sorted(journal_path.glob("*.md")):
        entries.append(f"=== {md_file.stem} ===\n{md_file.read_text()}")
    return "\n\n".join(entries)


def generate_weekly_insight(all_entries):
    prompt = f"""You are a senior engineering mentor.
Below are a developer's daily journal entries from their git commits.

Write a structured Weekly Insight Report with these sections:
1. What you shipped this week (bullet list)
2. Your top 3 patterns (habits noticed — good and bad)
3. Blind spots (2 things you consistently miss)
4. Growth areas (where you improved)
5. Your 5-day learning plan for next week (specific tasks)
6. Motivational closing paragraph

Journal entries:
{all_entries}

Write the full report in markdown now."""

    print(f"\n[weekly] Generating report with {MODEL}...\n")
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]


def main():
    entries = load_all_entries()
    if not entries:
        print("[weekly] No journal entries found yet. Run diary.py first!")
        return

    report = generate_weekly_insight(entries)
    output = Path.home() / "ai-dev-diary" / "weekly_insight.md"
    output.write_text(f"# Weekly Dev Insight Report\n\n{report}\n")

    print("\n" + "=" * 50)
    print(report)
    print("=" * 50)
    print(f"\n[weekly] Report saved to: {output}")


if __name__ == "__main__":
    main()