from airflow import DAG
from datetime import datetime
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

default_args = {
   'owner': 'aws',
   'depends_on_past': False,
   'start_date': datetime(2019, 2, 20),
   'provide_context': True
}

dag = DAG('kubernetes_pod_java', default_args=default_args, schedule_interval=None)

kube_config_path = '/usr/local/airflow/dags/kube_config.yaml'

podRun = KubernetesPodOperator(
                       namespace="ato-airflow", 
                       image="704533066374.dkr.ecr.eu-west-1.amazonaws.com/ato-airflow:airflw",
                       cmds=["java"],
                       arguments=["-jar", "app/airflow-java-1.0-SNAPSHOT.jar", "localhost", "customers", "select count(*);", "all-things-open-2023", "eu-west-1","arn:aws:secretsmanager:eu-west-1:704533066374:secret:ato-airflow-mysql-credentials-2QiMNR"],
                       labels={"foo": "bar"},
                       name="mwaa-pod-java",
                       task_id="pod-task",
                       get_logs=True,
                       dag=dag,
                       is_delete_operator_pod=False,
                       config_file=kube_config_path,
                       in_cluster=False,
                       cluster_context='aws'
                       )
