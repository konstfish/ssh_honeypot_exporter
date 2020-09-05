FROM python:3.5

COPY . /opt
WORKDIR /opt

EXPOSE 5000

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "-u", "main.py" ]
