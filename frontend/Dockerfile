# Escolha uma imagem base do node que inclui o npm
FROM node:14-alpine

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie os arquivos necessários para a construção do projeto
COPY package.json .
COPY package-lock.json .
COPY public/ ./public/
COPY src/ ./src/

# Instale as dependências do projeto
RUN npm i

# Defina a porta que será exposta
EXPOSE 3000

# Comando que será executado quando o container for iniciado
CMD ["npm", "start"]
