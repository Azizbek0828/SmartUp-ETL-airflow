from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "retries": 2,                         # xato bo'lsa, yana 2 marta urinib ko'radi
    "retry_delay": timedelta(minutes=1),  # urinishlar orasida 1 daqiqa kutadi
}

with DAG(
    dag_id="smartup_etl",
    start_date=datetime(2026, 10, 1),
    schedule=None,          # hozircha qo'lda ishga tushiramiz
    catchup=False,
    default_args=default_args,
) as dag:
    customers = BashOperator(
        task_id="customers",
        bash_command="cd /opt/airflow/dags/pipelines && python customers.py",
    )
    products = BashOperator(
        task_id="products",
        bash_command="cd /opt/airflow/dags/pipelines && python products.py",
    )
    orders = BashOperator(
        task_id="orders",
        bash_command="cd /opt/airflow/dags/pipelines && python orders.py",
    )
    # Tartib: avval customers va products (bir vaqtda), keyin orders
    [customers, products] >> orders