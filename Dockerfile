FROM python:3-onbuild

COPY ./ /
EXPOSE 8000

RUN chmod +x start_celerybeat.sh
RUN chmod +x start_celeryd.sh
RUN chmod +x start_web.sh

RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput