# Use a slim version of Python 3.9
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the CSV file to the /app directory
COPY netflix_data.csv ./  

# Copy the rest of the application code to the /app directory
COPY . .

# Expose the default Streamlit port
EXPOSE 8501

# Correct the entry point to run Streamlit and the application file
ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8080", "--server.address=0.0.0.0"]

