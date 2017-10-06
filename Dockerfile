FROM python:3

# Add requirements.txt.
COPY requirements.txt ./

# Insall `cron`.
RUN apt-get install cron

# Install Python packages at system-wide level.
RUN pip install -r requirements.txt