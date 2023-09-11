from datetime import datetime

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

with DAG(dag_id="virtualenv_example", start_date=datetime(2022, 1, 1), schedule=None) as dag:
    env = {}
    env['MINIO_HOST'] = 'http://10.11.25.50:9000'
    env['MINIO_ACCESS_KEY'] = 'minio'
    env['MINIO_SECRET_KEY'] = 'Megalab-X'

    train_job = DockerOperator(
        task_id='list_minio',
        image='minio/mc',
        container_name='mc',
        api_version='auto',
        auto_remove=True,
        environment=env,
        command=[
            'mc', 'alias', 'set', 'minio', '$MINIO_HOST', '$MINIO_ACCESS_KEY', '$MINIO_SECRET_KEY', '&&',
            'mc', 'ls', 'minio'
        ],
        docker_url="unix://var/run/docker.sock",
    )
