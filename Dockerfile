FROM python:3.8
WORKDIR /app
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv
RUN pipenv lock --requirements > requirements.txt

FROM python:3.8-slim
RUN mkdir -p /workspace/app && useradd -rm -d /workspace/app -s /bin/bash -u 1000 app
COPY --from=0 /app/requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn
WORKDIR /worspace/app
USER app
COPY ./wichtelit/ ./
EXPOSE 8080
CMD ["gunicorn", "-w", "10", "-b", ":8080", "wichtelit.wsgi:application"]  
