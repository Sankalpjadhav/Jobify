from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)


def db_connection():
  conn = None
  try:
    # Connect to the database
    conn = sqlite3.connect('jobopenings.sqlite')
    return conn
  except sqlite3.Error as e:
    print(e)
    return None


@app.route("/clear")
def clear_db():
  conn = db_connection()
  if conn is not None:
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS job_postings")
    sql_query_to_clear_table = """DELETE FROM job_postings"""
    cursor.execute(sql_query_to_clear_table)
    conn.commit()
    return "Database cleared"
  else:
    return "Error: unable to connect to database"


@app.route("/")
def hello_world():
  conn = db_connection()
  cursor = conn.execute("SELECT * FROM job_postings")
  JOBS = [
      dict(id=row[0],
           title=row[1],
           company=row[2],
           location=row[3],
           salary=row[4],
           job_description=row[5],
           job_requirement=row[6]) for row in cursor.fetchall()
  ]
  return render_template('home.html', jobs=JOBS, company_name='Jobify')


@app.route("/addjobs", methods=['GET', 'POST'])
def add_jobs():
  if request.method == 'POST':
    title = request.form['title']
    company = request.form['company']
    location = request.form['location']
    salary = request.form['salary']
    description = request.form['description']
    requirement = request.form['requirement']
    conn = db_connection()
    conn.execute(
        "INSERT INTO job_postings (title, company, location, salary, job_description, job_requirement) VALUES (?, ?, ?, ?, ?, ?)",
        (title, company, location, salary, description, requirement))
    conn.commit()
    # Update the JOBS variable
    cursor = conn.execute("SELECT * FROM job_postings")
    JOBS = [
        dict(id=row[0],
             title=row[1],
             company=row[2],
             location=row[3],
             salary=row[4],
             job_description=row[5],
             job_requirement=row[6]) for row in cursor.fetchall()
    ]
    return render_template('home.html', jobs=JOBS, company_name='Jobify')
  return render_template('addjobs.html')


@app.route("/api/jobs")
def list_jobs():
  conn = db_connection()
  cursor = conn.execute("SELECT * FROM job_postings")
  jobs = [
      dict(id=row[0],
           title=row[1],
           company=row[2],
           location=row[3],
           salary=row[4],
           job_description=row[5],
           job_requirement=row[6]) for row in cursor.fetchall()
  ]
  return jsonify(jobs)


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
