
import psycopg2

# Connect to PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="LMS",
    user="postgres",
    password="SHA2456101717",
    port="5432"
)

# Create cursor
cur = conn.cursor()

# Fetch all student records
cur.execute("SELECT * FROM students")

# Get all records
rows = cur.fetchall()

# Display records
print("STUDENT DETAILS")
print("-----------------------------")

for row in rows:
    print("ID:", row[0])
    print("Name:", row[1])
    print("Age:", row[2])
    print("City:", row[3])
    print("State:", row[4])
    print("ZIP:", row[5])
    print("-----------------------------")

# Close connection
cur.close()
conn.close()
