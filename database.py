import sqlite3

conn = sqlite3.connect('jobopenings.sqlite')
cursor = conn.cursor()

# Execute SQL query to create the table with corrected column definition
sql_query_to_create_table = """CREATE TABLE IF NOT EXISTS job_postings (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,  
                                title TEXT NOT NULL,  
                                company TEXT NOT NULL,
                                location TEXT NOT NULL,
                                salary TEXT NOT NULL,
                                job_description TEXT NOT NULL,
                                job_requirement TEXT NOT NULL
                            );"""

cursor.execute(sql_query_to_create_table)

cursor.close()
conn.close()
