FROM python:3.7
RUN pip install pipenv

ENV FLASK_APP server.py
ENV FLASK_ENV dev
ENV FLASK_RUN_HOST 0.0.0.0

RUN adduser --disabled-login hyperion
USER hyperion

WORKDIR /home/hyperion

COPY Pipfile Pipfile.lock ./
RUN pipenv install

COPY hyperion hyperion
COPY migrations migrations
COPY wsgi.py boot.sh ./

EXPOSE 5000
ENTRYPOINT ["sh", "boot.sh"]
