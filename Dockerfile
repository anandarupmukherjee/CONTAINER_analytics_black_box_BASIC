FROM python:3
MAINTAINER ANAND MUKHERJEE @ IfM


ADD ./results/ /app/results

COPY requirements.txt .
COPY app.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "/app.py"]
