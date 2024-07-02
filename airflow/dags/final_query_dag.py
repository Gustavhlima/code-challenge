from datetime import datetime, timedelta

from airflow import DAG

from pipeline_tasks import run_final_query_task

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
    'final_query_results_dag',
    default_args=default_args,
    description='Resultado final desafio lighthouse',
    schedule=None,
    start_date=datetime(2024, 6, 28),
    catchup=False,
    tags=['Embulk', 'PostgreSQL'],
) as dag:
    # Cria a tarefa para executar a consulta final e salvar os resultados
    results = run_final_query_task()
