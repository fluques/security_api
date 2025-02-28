FROM python:3.11
EXPOSE 5000
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --dev --system
 

CMD ["flask", "run", "--host", "0.0.0.0"]
