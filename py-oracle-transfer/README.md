# Data Transfer Script in Docker

This project contains a Python script designed to transfer data between two Oracle databases using `pandas` and `SQLAlchemy`. The script reads SQL data from a source database and writes it to a target database, handling large datasets in chunks to avoid memory issues. The project also includes a Docker setup for containerized execution.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Docker Usage](#docker-usage)

## Requirements

- Python 3.9+
- Docker
- Docker Compose (optional)

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject
   ```

2. **Install Python dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

## Configuration

1. **Create a configuration file:**

   Create a `config/config.yaml` file with the following structure:

   ```yaml
   stages:
     dev:
       source_conn_str: "oracle+oracledb://user1:password1@hostname1:port1/service_name1"
       target_conn_str: "oracle+oracledb://user2:password2@hostname2:port2/service_name2"
       query: "SELECT * FROM your_table"
       target_table: "your_target_table"
       mode: "append" # or 'replace'
     # Add more stages as needed
   ```

## Usage

Run the script directly with Python:

```sh
python main.py <stage>
```

Example:

```sh
python main.py dev
```

## Docker Usage

### Build the Docker image:

```sh
docker build -t your_image_name .
```

### Run the Docker container with the stage argument:

```sh
docker run --rm your_image_name <stage>
```

Example:

```sh
docker run --rm your_image_name dev
```

### Docker-Compose

Alternatively, use Docker Compose for easier management:

Update docker-compose.yml (if necessary):

The docker-compose.yml file is already set up to run the script with the dev stage.

```yaml
version: "3.8"

services:
  app:
    build: .
    command: ["python", "main.py", "dev"]
    volumes:
      - ./config:/usr/src/app/config
```

Build and run with Docker Compose:

```sh
docker-compose up --build
```
