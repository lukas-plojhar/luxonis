FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN playwright install --with-deps chromium

COPY . .

ENTRYPOINT [ "python" ]

CMD ["app.py"]