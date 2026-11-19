# import os

# path = r"C:\Users\syedh\OneDrive\Documents\python\landingfolder"

# files = os.listdir(path)

# print("Files and folders inside the directory:\n")

# for file in files:
#     print(file)



# import os
# from datetime import datetime, date

# path = r"C:\Users\syedh\OneDrive\Documents\python\landingfolder"

# today = date.today()

# print("Today's Date:", today)
# print("\nToday's files:\n")

# files = os.listdir(path)

# for file in files:
#     full_path = os.path.join(path, file)

#     if os.path.isfile(full_path):

#         file_date = datetime.fromtimestamp(
#             os.path.getmtime(full_path)
#         ).date()

#         if file_date == today:
#             print(file)




# import os
# from datetime import datetime

# path = r"C:\Users\syedh\OneDrive\Documents\python\landingfolder"

# today = datetime.now().strftime("%Y%m%d")

# print("Today's Date:", today)
# print("\nToday's files:\n")

# for file in os.listdir(path):
#     if today in file:
#         print(file)





# import pandas as pd
# from sqlalchemy import create_engine

# host = "localhost"
# port = 5432
# database = "myapplication"  
# username = "postgres"
# password = "SHA2456101717"  

# # Create connection URL
# connection_url = (
#     f"postgresql+psycopg2://{username}:{password}"
#     f"@{host}:{port}/{database}"
# )

# # Connect to database
# engine = create_engine(connection_url)

# try:
#     # Test database connection
#     with engine.connect() as connection:
#         print("Database connected successfully!")

#     # Fetch records using Pandas
#     df = pd.read_sql("SELECT * FROM students", engine)

#     print("\nStudent Records:")
#     print(df.to_string(index=False))

# except Exception as e:
#     print("Connection failed:", e)

# finally:
#     engine.dispose()






# import json
# import pandas as pd
# from datetime import datetime
# from sqlalchemy import create_engine
# from sqlalchemy.dialects.postgresql import insert

# # Folder path
# path = r"C:\Users\syedh\OneDrive\Documents\python\landingfolder"
# json_file = path + r"\students.json"

# # Database connection
# engine = create_engine(
#     "postgresql+psycopg2://postgres:your_password@localhost:5432/postgres"
# )

# try:
#     # Read JSON data
#     with open(json_file, "r") as file:
#         data = json.load(file)

#     # Convert JSON to DataFrame
#     df = pd.DataFrame(data)

#     print("JSON Records:")
#     print(df)

#     # Add timestamps
#     today = datetime.now()
#     df["inserted_on"] = today
#     df["updated_on"] = today

#     # Connect to PostgreSQL
#     with engine.begin() as conn:

#         for record in df.to_dict(orient="records"):

#             query = insert(
#                 __import__("sqlalchemy").Table(
#                     "students",
#                     __import__("sqlalchemy").MetaData(),
#                     autoload_with=conn
#                 )
#             ).values(**record)

#             query = query.on_conflict_do_update(
#                 index_elements=["idno"],
#                 set_={
#                     "name": query.excluded.name,
#                     "age": query.excluded.age,
#                     "course": query.excluded.course,
#                     "fees": query.excluded.fees,
#                     "joindate": query.excluded.joindate,
#                     "updated_on": today
#                 }
#             )

#             conn.execute(query)

#     print("\nRecords inserted/updated successfully!")

# except Exception as e:
#     print("Error:", e)

# finally:
#     engine.dispose()






import os
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.dialects.postgresql import insert

# Folder path
folder = r"C:\Users\syedh\Documents\python\landingfolder"

csv_file = os.path.join(folder, "students.csv")
json_file = os.path.join(folder, "students_20261119json")

# PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg2://postgres:SHA2456101717@localhost:5432/postgres"
)

try:
    # Read CSV file
    csv_df = pd.read_csv(csv_file)

    # Read JSON file
    json_df = pd.read_json(json_file)

    # Combine CSV and JSON data
    df = pd.concat([csv_df, json_df], ignore_index=True)

    print("Data loaded from CSV and JSON:")
    print(df)

    # Connect to PostgreSQL
    with engine.begin() as conn:

        metadata = MetaData()
        students_table = Table(
            "students",
            metadata,
            autoload_with=conn
        )

        current_time = datetime.now()

        # Insert or update students
        for record in df.to_dict(orient="records"):

            record["inserted_on"] = current_time
            record["updated_on"] = current_time

            query = insert(students_table).values(**record)

            query = query.on_conflict_do_update(
                index_elements=["idno"],
                set_={
                    "name": query.excluded.name,
                    "age": query.excluded.age,
                    "course": query.excluded.course,
                    "fees": query.excluded.fees,
                    "joindate": query.excluded.joindate,
                    "updated_on": current_time
                }
            )

            conn.execute(query)

    print("\nData successfully synchronized!")

    result = pd.read_sql(
        "SELECT * FROM students ORDER BY idno",
        engine
    )

    print("\nFinal Student Records:")
    print(result.to_string(index=False))

except Exception as e:
    print("Error:", e)

finally:
    engine.dispose()

