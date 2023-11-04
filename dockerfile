# Use an official Python runtime as a paranet image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy only the retirements.txt file and run pip install
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# First run the database setup script
COPY database.py /app/
RUN python database.py

# Copy the rest of the project contents into the container at /app
COPY . /app/

# Expose the port that will be used by our Flask application to run
EXPOSE 5000

# Command to start the Flask application
CMD ["python","app.py"]
