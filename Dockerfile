FROM python:3

# Add requirements.txt.
COPY requirements.txt ./

# Update repository.
RUN apt-get -qq update

# Insall `cron`.
RUN apt-get -qq install cron

# Install Python packages at system-wide level.
RUN pip install -r requirements.txt