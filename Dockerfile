# Menggunakan image Python sebagai basis
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Salin requirements.txt dan instal dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Salin aplikasi ke dalam container
COPY . /app

# Copy .env ke dalam container
COPY .env /app/.env

# Jalankan aplikasi
CMD ["python", "server.py"]
