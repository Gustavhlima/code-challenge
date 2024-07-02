import pathlib
from airflow.operators.bash import BashOperator
import logging

# Define o diretório base do projeto e o caminho executável do Embulk
BASE_DIR = pathlib.Path(__file__).parent.parent.parent.resolve()
EMBULK_BIN = '~/.embulk/bin/embulk'

# Credenciais para o banco de dados PostgreSQL de origem
postgres_source_creds = {
    "host": "localhost",
    "user": "northwind_user",
    "password": "thewindisblowing",
    "database": "northwind",
    "port": "5432"
}

# Credenciais para o banco de dados PostgreSQL de destino
postgres_target_creds = {
    "host": "localhost",
    "user": "northwind_user",
    "password": "thewindisblowing",
    "database": "northwind_destino",
    "port": "5433"
}

# Função para extrair dados do banco de dados Northwind usando Embulk
def extract_northwind_task(table):

    # Define o caminho do arquivo de configuração do Embulk e o diretório de destino para os dados extraídos
    config_path = f'{BASE_DIR}/embulk_configs/extract_postgres.yaml.liquid'
    target_dir = f'{BASE_DIR}/data/postgres/{table}/{{{{ ds }}}}/'
    logging.info(f'Extracting {table} table from Northwind into {target_dir}')
    
    # Cria um BashOperator para executar o comando do Embulk
    return BashOperator(
        task_id=f'embulk_extract_{table}',
        bash_command=f'mkdir -p {target_dir} && {EMBULK_BIN} run {config_path}',
        env={
            "HOST": postgres_source_creds["host"],
            "USER": postgres_source_creds["user"],
            "PASSWORD": postgres_source_creds["password"],
            "DATABASE": postgres_source_creds["database"],
            "PORT": postgres_source_creds["port"],
            "TABLE": table,
            "OUT_PATH_PREFIX": target_dir
        }
    )

# Função para extrair dados de um arquivo CSV usando Embulk
def extract_order_details_task(table):
    config_path = f'{BASE_DIR}/embulk_configs/extract_csv.yaml.liquid'
    source_prefix = f'{BASE_DIR}/data/{table}'
    target_dir = f'{BASE_DIR}/data/csv/{{{{ ds }}}}/'
    target_prefix = f'{target_dir}/{table}' 

     # Cria um BashOperator para executar o comando do Embulk
    return BashOperator(
        task_id=f'embulk_extract_{table}',
        bash_command=f'mkdir -p {target_prefix} && {EMBULK_BIN} run {config_path}',
        env={
            "IN_PATH_PREFIX": source_prefix,
            "OUT_PATH_PREFIX": target_prefix
        }
    )

# Função para carregar dados no banco de dados PostgreSQL de destino usando Embulk
def load_postgres_task(table):

    # Define o caminho do arquivo de configuração do Embulk e o prefixo do caminho do arquivo para os dados de origem
    config_path = f'{BASE_DIR}/embulk_configs/{table}_to_postgres.yaml.liquid'
    if table == "order_details":
        file_path_prefix = f'{BASE_DIR}/data/csv/{{{{ ds }}}}'
    else:
        file_path_prefix = f'{BASE_DIR}/data/postgres/{table}/{{{{ ds }}}}'

    logging.info(f'Loading {table} table from {file_path_prefix}')

    # Cria um BashOperator para executar o comando do Embulk
    return BashOperator(
        task_id=f'embulk_load_{table}',
        bash_command=f'{EMBULK_BIN} run {config_path}',
        env={
            "IN_PATH_PREFIX": file_path_prefix,
            "HOST": postgres_target_creds["host"],
            "USER": postgres_target_creds["user"],
            "PASSWORD": postgres_target_creds["password"],
            "DATABASE": postgres_target_creds["database"],
            "PORT": postgres_target_creds["port"],
            "TABLE": table
        }
    )

# Função para executar a consulta final e salvar os resultados usando Embulk
def run_final_query_task():

    # Define o caminho do arquivo de configuração do Embulk e o diretório de destino para os resultados da consulta
    config_path = f'{BASE_DIR}/embulk_configs/final_query.yaml.liquid'
    target_dir = f'{BASE_DIR}/data/results/{{{{ ds }}}}/'
    logging.info(f'Generating file with final query results into {target_dir}')
    
     # Cria um BashOperator para executar o comando do Embulk
    return BashOperator(
        task_id=f'embulk_run_final_query',
        bash_command=f'mkdir -p {target_dir} && {EMBULK_BIN} run {config_path}',
        env={
            "HOST": postgres_target_creds["host"],
            "USER": postgres_target_creds["user"],
            "PASSWORD": postgres_target_creds["password"],
            "DATABASE": postgres_target_creds["database"],
            "PORT": postgres_target_creds["port"],
            "OUT_PATH_PREFIX": target_dir
        }
    )
