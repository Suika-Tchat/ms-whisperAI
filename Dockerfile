FROM python:3.11

# Installation de ffmpeg
RUN apt-get update \
    && apt-get install -y ffmpeg \
    && rm -rf /var/lib/apt/lists/*

    
WORKDIR /app
# Première étape: Copier uniquement requirements.txt
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Deuxième étape: Copier le reste du code
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
