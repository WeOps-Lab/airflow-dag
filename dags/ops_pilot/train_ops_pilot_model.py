from datetime import datetime
from textwrap import dedent

from airflow import DAG
from airflow.hooks.base import BaseHook
from airflow.models import Param
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

conn = BaseHook.get_connection('minio')

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
            'minin_bucket': Param('/assert/assert.zip', type='string',
                                  title='语料包路径'),
            'rasa_model_name': Param('/assert/assert.zip', type='string',
                                     title='Rasa 模型路径'),
            'share_dir': Param('/data/nfs', type='string',
                               title='NFS文件夹路径'),
        }
) as dag:
    env = {'MINIO_HOST': f'{conn.host}:{conn.port}', 'MINIO_ACCESS_KEY': conn.login, 'MINIO_SECRET_KEY': conn.password}
    share_dir = dag.params.get('share_dir')
    train_job = DockerOperator(
        task_id='train_ops_pilot_model',
        image='ccr.ccs.tencentyun.com/megalab/mc',
        container_name='ops-pilot-train',
        api_version='auto',
        auto_remove=True,
        environment=env,
        mount_tmp_dir=False,
        mounts=[
            Mount(source=share_dir, target="/share_data", type="bind"),
        ],
        command='bash /apps/mc-tools.sh upload /share_data/compose-hub/support-files/swarm.md ops-pilot-assert/swarm.md',
        docker_url="unix://var/run/docker.sock",
    )

    train_job
