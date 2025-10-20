import readline
import sqlite3
import sys


# SQL query program adapted from CTD sqlcommand.py
conn = sqlite3.connect("./db/baseball.db")
conn.execute("PRAGMA foreign_keys = 1")

cursor = conn.cursor()

# Show database tables
tables = cursor.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY 'name'").fetchall()

print("Tables:")
for row in tables:
    print(row[0])

def main():

    lines = []

    # Get SQL queries
    while True:
        try:
            prompt = 'sql>' if not lines else '>>>'
            line = input(prompt)

            if line.strip().lower() == "exit;":
                break

            lines.append(line)

            if line.strip().endswith(';'):
                command = ' '.join(lines).strip()

            lines = []

            try:
                cursor.execute(command)

            except sqlite3.Error as e:
                print(e)

        except EOFError:
            break
        except KeyboardInterrupt:
            lines = []

    conn.close()


if __name__ == '__main__':
    main()
