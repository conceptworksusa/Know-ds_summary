
FROM python:3.10.13
# FROM mcr.microsoft.com/azure-cli
#ARG SQL_SERVER_PASSWORD
#ENV SQL_SERVER_PASSWORD=${SQL_SERVER_PASSWORD}
#ENV AZURE_CLIENT_ID=${AZURE_CLIENT_ID}


WORKDIR /code

#RUN pip install azure-cli

#RUN az login --identity --username $AZURE_CLIENT_ID

COPY ./requirements.txt /code/requirements.txt

COPY ./src /code/src

# Install below for SQL Server ODBC Driver 17 for Linux
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential \
    curl \
    apt-utils \
    gnupg2 &&\
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip

RUN apt-get update
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN exit
RUN apt-get update
RUN env ACCEPT_EULA=Y apt-get install -y msodbcsql17



#RUN apt-get update -y && apt-get -y install unixodbc-dev msodbcsql17

# For local setup use torch which is compatible with CPU, Comment the line below if you want to use GPU
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu


# Pip install requirements from file
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
ENV PYTHONPATH="/code:{PYTHONPATH}"

# Move code form ./src to /code/src
COPY ./src /code/src

EXPOSE 8501

CMD ["streamlit","run", "src/ui/chat.py","--server.port=8501","--server.address=0.0.0.0"]
