FROM python:3.11-slim

WORKDIR /app

COPY examples/reference_sut/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY examples/reference_sut/app.py /app/app.py

ENV PORT=8000
EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
