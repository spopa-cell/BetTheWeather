FROM python:3.12-alpine

# Empêche la création de fichiers .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dossier de travail dans le container
WORKDIR /app

# Installer les dépendances système (souvent utiles avec requests)
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev

# Copier les dépendances Python
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du projet
COPY . .

# Commande de lancement
CMD ["python", "app.py"]
