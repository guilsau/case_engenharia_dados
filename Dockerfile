# Imagem base
FROM python:3.11-slim

# Criar diretório de trabalho
WORKDIR /app

# Copiar arquivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY main.py .
COPY ingestao/ ./ingestao/
COPY transformacao/ ./transformacao/
COPY utils/ ./utils/
COPY data/ ./data/

CMD ["python", "main.py"]
