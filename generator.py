import psycopg2
import random
from datetime import datetime, timedelta
import yaml


# Function to read YAML configuration
def read_yaml_config(config_file):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config


# Function to create a PostgreSQL database and tables dynamically
def create_database(config):
    conn = psycopg2.connect(
        dbname=config['database']['name'],
        user=config['database']['user'],
        password=config['database']['password'],
        host=config['database']['host']
    )
    cursor = conn.cursor()

    for table_name, table_config in config['tables'].items():
        columns = ', '.join([f"{column['name']} {column['type']}" for column in table_config['columns']])
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        cursor.execute(create_table_query)

    conn.commit()
    conn.close()


# Function to generate sample data for each table
def generate_sample_data(config):
    data = {}
    for table_name, table_config in config['tables'].items():
        num_records = table_config['num_records']
        data[table_name] = []
        for _ in range(num_records):
            row = {}
            for column in table_config['columns']:
                column_name = column['name']
                column_type = column['type']
                row[column_name] = generate_sample_value(column_type, config, table_name, column_name)
            data[table_name].append(tuple(row.values()))
    return data


# Function to generate sample value based on column type
def generate_sample_value(column_type, config, table_name, column_name):
    if column_type.startswith("INT"):
        return random.randint(1, 100)
    elif column_type.startswith("DECIMAL"):
        return round(random.uniform(10, 1000), 2)
    elif column_type.startswith("VARCHAR"):
        return f'Sample {random.randint(1, 1000)}'
    elif column_type == "DATE":
        return datetime.now().strftime('%Y-%m-%d')
    elif column_type == "FLOAT":
        return round(random.uniform(1, 10), 1)
    else:
        return generate_foreign_key_value(config, table_name, column_name)


# Function to generate foreign key value
def generate_foreign_key_value(config, table_name, column_name):
    for foreign_key in config['tables'][table_name].get('foreign_keys', []):
        if foreign_key['column'] == column_name:
            ref_table = foreign_key['ref_table']
            ref_column = foreign_key['ref_column']
            ref_table_data = config['tables'][ref_table]
            return random.choice(range(1, ref_table_data['num_records'] + 1))  # Assuming IDs start from 1


if __name__ == "__main__":
    # Read database configuration from YAML
    config = read_yaml_config("database_config.yaml")

    # Create database and tables
    create_database(config)

    # Generate sample data for each table
    data = generate_sample_data(config)

    # Insert sample data into database
    conn = psycopg2.connect(
        dbname=config['database']['name'],
        user=config['database']['user'],
        password=config['database']['password'],
        host=config['database']['host']
    )
    cursor = conn.cursor()

    for table_name, table_data in data.items():
        columns = ', '.join([column['name'] for column in config['tables'][table_name]['columns']])
        placeholders = ', '.join(['%s'] * len(config['tables'][table_name]['columns']))
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.executemany(insert_query, table_data)

    conn.commit()
    conn.close()

    print("Sample entries generated successfully.")
