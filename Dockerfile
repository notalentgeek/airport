FROM python:3

# Add requirements.txt.
COPY requirements.txt ./

# Install Python packages at system-wide level.
RUN pip install -r requirements.txt