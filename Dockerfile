FROM python:3.12

WORKDIR /app

COPY requirment.txt .

RUN pip install --no-cache-dir -r requirment.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
