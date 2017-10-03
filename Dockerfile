FROM python:3-onbuild

RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput
RUN automation/rm.sh