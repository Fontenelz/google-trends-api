# Imagem base oficial do Python
FROM python:3.10-slim

# Define diretório de trabalho dentro do container
WORKDIR /app

# Instala dependências de sistema necessárias
RUN apt-get update && apt-get install -y \
  chromium \
  chromium-driver \
  curl \
  gcc \
  libxml2-dev \
  libxslt-dev \
  build-essential \
  && rm -rf /var/lib/apt/lists/*

# Define variável de ambiente para o Chromium usado pelo pyppeteer
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

# Copia requirements.txt e instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Expõe a porta 3000
EXPOSE 3000

# Comando de inicialização usando gunicorn na porta 3000
CMD ["gunicorn", "-w", "4", "-k", "gthread", "--threads", "2", "-b", "0.0.0.0:3000", "app:app"]
