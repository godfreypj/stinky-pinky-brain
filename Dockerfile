FROM python:3.9-slim

WORKDIR /home/user/stinky-pinky-brain

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT 8080
EXPOSE 8080

RUN pip install gunicorn

CMD ["gunicorn", "-b", ":8080", "main:app"]
