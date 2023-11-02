import sqlite3

conn = sqlite3.connect('jobopenings.sqlite')
cursor = conn.cursor()

# Create the job_postings table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_postings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        location TEXT NOT NULL,
        salary TEXT NOT NULL,
        job_description TEXT NOT NULL,
        job_requirement TEXT NOT NULL
    );
""")

# Create the userdata table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS userdata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        skills TEXT NOT NULL,
        job_id INTEGER NOT NULL,
        UNIQUE (id, email),
        FOREIGN KEY (job_id) REFERENCES job_postings (id)
    );
""")

cursor.close()
conn.close()
