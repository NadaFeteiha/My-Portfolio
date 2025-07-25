# Line 1: Use a slim base image to reduce size
FROM python:3.9-slim-buster

# Line 2: Set the working directory
WORKDIR /myportfolio

# Line 3: Copy requirements first to cache better
COPY requirements.txt .

# Line 4: Install dependencies
RUN pip install -r requirements.txt

# Line 5: Copy the rest of the project files
COPY . .
COPY ./app/ ./app/

CMD ["flask", "run", "--host=0.0.0.0"]

# Line 6: Expose port 5000
EXPOSE 5000
