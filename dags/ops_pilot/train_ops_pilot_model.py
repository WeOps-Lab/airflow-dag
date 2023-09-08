from datetime import datetime
from textwrap import dedent

from airflow import DAG
from airflow.hooks.base import BaseHook
from airflow.models import Param
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator

# conn = BaseHook.get_connection('minio')

with DAG(
        'train_ops_pilot_model',
        default_args={
            'depends_on_past': False,
        },
        description='OpsPilot 模型训练任务',
        schedule=None,
        start_date=datetime(2021, 1, 1),
        catchup=False,
        tags=['ops_pilot'],
        params={
            'MINIO_BUCKET_NAME': Param('/assert/assert.zip', type='string',
                                       title='语料包路径'),
            'RASA_MODEL_NAME': Param('/assert/assert.zip', type='string',
                                     title='Rasa 模型路径'),
        }
) as dag:
    env = {}
    env['MINIO_HOST'] = 'minio'
    env['MINIO_ACCESS_KEY'] = 'minioadmin'
    env['MINIO_SECRET_KEY'] = 'minioadmin'
    train_job = DockerOperator(
        task_id='train_ops_pilot_model',
        image='ccr.ccs.tencentyun.com/megalab/ops-pilot',
        container_name='ops-pilot-train',
        api_version='auto',
        auto_remove=True,
        environment=env,
        command=['ls'],
        docker_url="unix://var/run/docker.sock",
    )

    train_job
