from flask import Flask, render_template, jsonify, request, redirect
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
    sql_query_to_clear_table = """DELETE FROM userdata"""
    cursor.execute(sql_query_to_clear_table)
    cursor.execute("DROP TABLE IF EXISTS userdata")
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


@app.route("/api/applicants")
def list_applicants():
    conn = db_connection()
    cursor = conn.execute("SELECT id, name, email, skills, job_id FROM userdata")
    applicants = [
        dict(
            id=row[0],
            name=row[1],
            email=row[2],
            skills=row[3],
            job_id=row[4]
        ) for row in cursor.fetchall()
    ]
    return jsonify(applicants)


@app.route("/apply", methods=['POST'])
def apply_job():
    name = request.form['name']
    email = request.form['email']
    skills = request.form['skills']
    job_id = request.form['job_id']

    conn = db_connection()
    cursor = conn.execute(
        "SELECT id FROM userdata WHERE email=? AND job_id=?", (email, job_id))
    result = cursor.fetchone()

    if result is not None:
        # Display a popup indicating that the user has already applied for this job
        return render_template('jobapplied.html')

    conn.execute(
      "INSERT INTO userdata (name, email, skills, job_id) VALUES (?, ?, ?, ?)",
      (name, email, skills, job_id))
    conn.commit()

    # Redirect to the job details page, passing the job_id as a parameter
    return redirect(f"/job/{job_id}")



@app.route("/job/<job_id>")
def job_details(job_id):
    conn = db_connection()
    cursor = conn.execute("SELECT * FROM job_postings WHERE id=?", (job_id,))
    job = cursor.fetchone()
    cursor = conn.execute("SELECT COUNT(*) FROM userdata WHERE job_id=?", (job_id,))
    user_count = cursor.fetchone()[0]  # Retrieve count directly from the database
    # print(applicants)  # Print the applicants to check the data
    return render_template('jobdetails.html', job=job, user_count=user_count)




if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
