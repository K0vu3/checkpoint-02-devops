FROM python:3.9-slim-buster

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências para dentro do container
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código fonte para dentro do container
COPY . .

# Define a porta que a aplicação irá utilizar
EXPOSE 8000

# Inicia a aplicação
CMD ["python", "app.py"]
