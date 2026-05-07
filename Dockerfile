# Base image — Python 3.11
FROM python:3.11-slim

# Working directory set karo
WORKDIR /app

# Requirements copy karo aur install karo
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Saara code copy karo
COPY . .

# Data folder banao
RUN mkdir -p data

# Port expose karo
EXPOSE 5000

# App run karo
CMD ["python", "app.py"]