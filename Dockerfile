FROM debian:latest

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    build-essential \
    python3-dev \
    python3-setuptools \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-rus \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Копирование исходного кода
COPY . /app
WORKDIR /app


RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir -Ur requirements.txt

RUN chmod -R 777 /app

# Команда для запуска приложения
CMD ["python3", "./main.py"]
