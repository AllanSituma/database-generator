# Database Sample Data Generator

This project is a Python script that generates sample data for a database based on a YAML configuration file. It can be used to populate a database with sample data for testing or development purposes.

## Prerequisites

Before running the script, ensure you have the following installed:
- Python (version 3.9 or higher)
- Docker

## Getting Started

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/your_username/database-sample-data-generator.git
   ```

2. Navigate to the project directory:

   ```bash
   cd database-sample-data-generator
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

- Edit the `database_config.yaml` file to specify the database configuration and table definitions.
- Ensure that the YAML file contains the necessary information such as database host, user, password, database name, table names, columns, data types, and the number of records to generate.

## Running the Script

### Using Docker

1. Build the Docker image:

   ```bash
   docker build -t data-generator .
   ```

2. Run the Docker container:

   ```bash
   docker run --rm -v $(pwd)/database_config.yaml:/app/database_config.yaml data-generator
   ```

### Without Docker

1. Ensure that PostgreSQL is running on your local machine or update the database configuration in the YAML file to point to a remote database server.

2. Run the Python script:

   ```bash
   python python_script.py
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
