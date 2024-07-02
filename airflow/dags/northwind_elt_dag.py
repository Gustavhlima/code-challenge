from datetime import datetime, timedelta

from airflow import DAG


from pipeline_tasks import (
    extract_order_details_task,
    extract_northwind_task,
    load_postgres_task
)
# Argumentos padrão para o DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
# Define o DAG
with DAG(
    'northwind_elt_dag',
    default_args=default_args,
    description='Pipeline desafio lighthouse',
    schedule="0 0 * * *",
    start_date=datetime(2024, 6, 28),
    catchup=False,
    tags=['ELT', 'Embulk', 'PostgreSQL'],
) as dag:

    # Lista de tabelas para extrair e carregar
    tables = [
        'categories',
        'customer_customer_demo',
        'customer_demographics',
        'customers',
        'employee_territories',
        'employees',
        'order_details',
        'orders',
        'products',
        'region',
        'shippers',
        'suppliers',
        'territories',
        'us_states',
    ]
    # Cria tarefas para cada tabela na lista
    for table in tables:
        # Escolhe a tarefa de extração com base no nome da tabela
        if table == "order_details":
            extract_task = extract_order_details_task(table)
        else:
            extract_task = extract_northwind_task(table)
        # Cria a tarefa de carregamento para a tabela
        load_task = load_postgres_task(table)
        # Define as dependências das tarefas: primeiro extrair, depois carregar
        extract_task >> load_task
