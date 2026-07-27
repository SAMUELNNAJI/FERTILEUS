"""
Transfer all data from SQLite to Neon PostgreSQL.
Run with: python transfer_to_neon.py
"""
import os
import sys
import django
import json
import subprocess
from pathlib import Path

BASE = Path(__file__).resolve().parent

# ── Step 1: Dump from SQLite ──────────────────────────────────────────────────
print("=" * 60)
print("STEP 1: Dumping data from SQLite...")
print("=" * 60)

# Temporarily override DATABASE_URL to use SQLite
env_sqlite = os.environ.copy()
env_sqlite["DATABASE_URL"] = f"sqlite:///{BASE / 'db.sqlite3'}"

result = subprocess.run(
    [sys.executable, "manage.py", "dumpdata",
     "--natural-foreign", "--natural-primary",
     "--exclude=contenttypes",
     "--exclude=auth.permission",
     "--exclude=admin.logentry",
     "--indent=2",
     "--output=sqlite_dump.json"],
    env=env_sqlite,
    cwd=str(BASE),
    capture_output=True,
    text=True,
)

if result.returncode != 0:
    print("ERROR dumping SQLite:")
    print(result.stderr)
    sys.exit(1)

print(result.stdout or "Dump complete.")
if result.stderr:
    print("Warnings:", result.stderr[:500])

# Check what was dumped
dump_path = BASE / "sqlite_dump.json"
with open(dump_path, "r", encoding="utf-8") as f:
    data = json.load(f)

models_count = {}
for obj in data:
    m = obj["model"]
    models_count[m] = models_count.get(m, 0) + 1

print(f"\nDumped {len(data)} total objects:")
for model, count in sorted(models_count.items()):
    print(f"  {model}: {count}")

# ── Step 2: Load into Neon ────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 2: Loading data into Neon PostgreSQL...")
print("=" * 60)

result2 = subprocess.run(
    [sys.executable, "manage.py", "loaddata", "sqlite_dump.json"],
    cwd=str(BASE),
    capture_output=True,
    text=True,
)

print(result2.stdout)
if result2.stderr:
    print("Warnings/Errors:", result2.stderr[:1000])

if result2.returncode != 0:
    print("\nERROR loading data into Neon.")
    sys.exit(1)

print("\nTransfer complete!")
print("You can delete sqlite_dump.json once you have verified the data.")
