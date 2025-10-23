from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd
import sqlite3
from tabulate import tabulate
from config.logger import get_logger

log = get_logger("view_db")

conn = sqlite3.connect("database/database.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM findings ORDER BY created_at DESC LIMIT 10;")
rows = cursor.fetchall()

# Convert to pandas csv
df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
df.to_csv("database/findings.csv", index=False)


conn.close()