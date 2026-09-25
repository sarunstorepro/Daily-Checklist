#!/usr/bin/env python3
"""
Housekeeping script for the daily task diary's data repo.

Moves tasks that were completed more than ARCHIVE_AFTER_DAYS days ago out of
data/tasks.json and into a monthly archive file under data/archive/, so the
"live" file the web app loads on every page view stays small forever.

This does NOT do anything with pending tasks - pending tasks are meant to
stay in tasks.json until you complete or delete them, which is what makes
them "roll over" to the next day automatically (there's nothing to move;
they just remain in the one Pending list until you deal with them).
"""
import json
import os
from datetime import date, datetime, timedelta

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "tasks.json")
ARCHIVE_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "archive")
ARCHIVE_AFTER_DAYS = 30


def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        return json.loads(content) if content else default


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main():
    today = date.today()
    cutoff = today - timedelta(days=ARCHIVE_AFTER_DAYS)

    store = load_json(DATA_FILE, {"tasks": []})
    tasks = store.get("tasks", [])

    keep = []
    to_archive = {}  # "YYYY-MM" -> [tasks]
    moved = 0

    for t in tasks:
        completed_on = t.get("completedOn")
        if t.get("status") == "completed" and completed_on:
            try:
                completed_date = datetime.strptime(completed_on, "%Y-%m-%d").date()
            except ValueError:
                keep.append(t)
                continue
            if completed_date < cutoff:
                month_key = completed_on[:7]  # "YYYY-MM"
                to_archive.setdefault(month_key, []).append(t)
                moved += 1
                continue
        keep.append(t)

    if moved == 0:
        print("Nothing to archive today.")
        return

    for month_key, archived_tasks in to_archive.items():
        archive_path = os.path.join(ARCHIVE_DIR, f"{month_key}.json")
        existing = load_json(archive_path, {"tasks": []})
        existing_ids = {t["id"] for t in existing.get("tasks", [])}
        for t in archived_tasks:
            if t["id"] not in existing_ids:
                existing.setdefault("tasks", []).append(t)
        save_json(archive_path, existing)
        print(f"Archived {len(archived_tasks)} task(s) into data/archive/{month_key}.json")

    store["tasks"] = keep
    save_json(DATA_FILE, store)
    print(f"Moved {moved} completed task(s) out of the live file.")


if __name__ == "__main__":
    main()
