FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure backend can import shared code under /workspace/src
ENV PYTHONPATH="/app:/workspace"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--factory", "--host", "0.0.0.0", "--port", "8000"]

