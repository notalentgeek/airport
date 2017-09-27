FROM python:3-onbuild

COPY start.sh /start.sh
EXPOSE 8000
RUN python3 manage.py collectstatic --noinput

CMD ["/start.sh"]