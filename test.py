import os

os.environ["POSTGRES_PASSWORD"] = "SHA2456101717"

import pyodbc

conn = pyodbc.connect(
    "DRIVER={PostgreSQL Unicode(x64)};"
    "SERVER=localhost;"
    "PORT=5432;"
    "DATABASE=Leapstart;"
    "UID=postgres;"
    f"PWD={os.environ['POSTGRES_PASSWORD']};"
)

cursor = conn.cursor()

cursor.execute("SELECT * FROM candidates")

rows = cursor.fetchall()

# Get column names
columns = [column[0] for column in cursor.description]

# Display column names
print(columns)

# Display records
for row in rows:
    print(row)

cursor.close()
conn.close()