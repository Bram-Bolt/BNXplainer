import sqlite3
import csv
import sys

# Parameters
DB_PATH = "src/db/feedback.db"
TABLE_NAME = "feedback"
output_csv = f"{sys.argv[1]}.csv" if len(sys.argv) > 1 else "db_export.csv" 

def export_table_to_csv():
    # connect to db
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    
    cursor.execute(f"PRAGMA table_info({TABLE_NAME})")
    columns = [col[1] for col in cursor.fetchall()]

    
    cursor.execute(f"SELECT * FROM {TABLE_NAME}")
    rows = cursor.fetchall()
  
   # write to csv
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(columns)  
        writer.writerows(rows)

    conn.close()
    print(f"Exported {TABLE_NAME} to {output_csv}")

if __name__ == "__main__":
    export_table_to_csv()