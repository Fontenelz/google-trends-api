# Use Python slim para não ficar pesado
FROM python:3.10-slim

# Evita prompts de instalação
ENV DEBIAN_FRONTEND=noninteractive

# Instala dependências do Chromium e do Playwright/Pyppeteer
RUN apt-get update && apt-get install -y \
  wget curl gnupg ca-certificates \
  fonts-liberation libnss3 libxss1 libasound2 libatk1.0-0 libatk-bridge2.0-0 \
  libcups2 libdrm2 libgbm1 libgtk-3-0 libx11-xcb1 libxcomposite1 libxdamage1 \
  libxfixes3 libxrandr2 libxkbcommon0 libpangocairo-1.0-0 libpango-1.0-0 xdg-utils \
  && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copia apenas requirements.txt primeiro para usar cache do Docker
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do projeto
COPY . .

# Se você estiver usando Playwright
RUN pip install --no-cache-dir playwright
RUN playwright install chromium

# Variável de ambiente para Playwright/Pyppeteer localizar o Chromium
ENV PLAYWRIGHT_BROWSERS_PATH=/usr/bin

# Comando padrão para rodar a aplicação
CMD ["python", "-m", "app"]
