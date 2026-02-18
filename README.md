# Security app rest api

## Description.
Dockerized rest API to index pdf files into elasticsearch database. To search using Ollama embeddings with vectorial index or full text search with inverted index.

## Components
- [Docker](https://www.docker.com/)
- [Python](https://www.python.org/)
- [Nginx](https://nginx.org/)
- [Flask](https://flask.palletsprojects.com/en/stable/)
- [Postgres](https://www.postgresql.org/)


## Requirements
1. Docker and compose
    [Docker installation script](https://docs.docker.com/engine/install/ubuntu/)



## Installation
1. Clone the repository:
```bash
git clone https://github.com/fluques/security_api.git
```
2. Enter directory:
```bash
cd security_api
```
3. Set default settings:
```bash
cp .env.example .env
```
4. Run docker-compose file:
```bash
docker compose -f .\docker-compose.yml  up --build --force-recreate
```

## Running service on:
```bash
http://127.0.0.1:5000
```

