FROM python:3.8-slim

WORKDIR /server

# Install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv

# Copy project
COPY . /server/

# Install project dependencies
RUN pipenv install --dev

EXPOSE 8000