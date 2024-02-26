FROM python:3.11.0

# Define o diretório de trabalho dentro do container
WORKDIR /usr/src/app

# Instala as dependências da aplicação
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos da sua aplicação para o diretório de trabalho
COPY . .

# Expõe a porta que o Gunicorn vai rodar
EXPOSE 8000

# Executa o Gunicorn com as configurações desejadas
CMD ["gunicorn", "-b", "0.0.0.0:8000", "meuprojeto.wsgi:application"]
