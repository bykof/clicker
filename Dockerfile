FROM python:3.8
RUN pip install pipenv

EXPOSE 80

COPY ./ /app
WORKDIR /app

ENV PYTHONPATH /app

RUN pipenv install

CMD pipenv run migrate && pipenv run uvicorn main:app --host 0.0.0.0 --port 80
