FROM python:3.11-slim

# Installer les outils necessaires
RUN apt-get update && apt-get install -y \
    bash \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*


# Definir le repertoire de travail
WORKDIR /app

# Copier et installer les dependances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Rendre les scripts executables
RUN chmod +x scripts/*.sh || true

# Commande par defaut
CMD ["bash"]