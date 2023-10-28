from flask import Flask, render_template, jsonify

app = Flask(__name__)

JOBS = [{
    'id': 1,
    'title': 'Cloud Engineer',
    'location': 'Bengaluru, India',
    'salary': 'Rs. 15,00,000'
}, {
    'id': 2,
    'title': 'Software Development Engineer',
    'location': 'Hyderabad, India',
    'salary': 'Rs. 13,00,000'
}, {
    'id': 3,
    'title': 'Data Engineer',
    'location': 'Bengaluru, India'
}, {
    'id': 4,
    'title': 'Data Analyst',
    'location': 'Delhi, India',
    'salary': 'Rs. 10,00,000'
}, {
    'id': 5,
    'title': 'Frontend Engineer',
    'location': 'Remote',
    'salary': 'Rs. 12,00,000'
}]


@app.route("/")
def hello_world():
  return render_template('home.html', jobs=JOBS, company_name='Jobify')

@app.route("/api/jobs")
def list_jobs():
  return jsonify(JOBS)

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
