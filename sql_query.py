import sqlite3


# SQL query program adapted from CTD sqlcommand.py
conn = sqlite3.connect("./db/baseball.db")
conn.execute("PRAGMA foreign_keys = 1")

cursor = conn.cursor()

# Show database tables
tables = cursor.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY 'name'").fetchall()

# Print database tables
print("Tables:")
for row in tables:
    print(row[0])

def main():

    # List to store lines of the query
    lines = []

    # Get SQL queries
    while True:
        try:
            # Program line prompt
            prompt = 'sql>' if not lines else '>>>'
            line = input(prompt)

            # Exit clause
            if line.strip().lower() == "exit;":
                break
            
            # Append SQL query lines
            lines.append(line)

            # Look for the end of a command
            if line.strip().endswith(';'):
                command = ' '.join(lines).strip()

            lines = []

            try:
                # Execute and display the results of the command
                cursor.execute(command)
                results = cursor.fetchall()
                for row in results:
                    print(row)

            except sqlite3.Error as e:
                print(e)

            try:
                # Commit any changes
                conn.commit()
            except sqlite3.IntegrityError as e:
                print(e)

        except EOFError:
            break
        except KeyboardInterrupt:
            lines = []

    conn.close()


if __name__ == '__main__':
    main()
