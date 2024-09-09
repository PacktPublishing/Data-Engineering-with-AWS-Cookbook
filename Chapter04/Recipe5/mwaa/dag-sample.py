from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import os 

with DAG(
        dag_id=os.path.basename(__file__).replace(".py", ""),
        # These args will get passed on to each operator
        default_args={
            # the number of retries that should be performed before failing the task
            'retries': 1
        },
        description='A simple DAG to print information on terminal',
        # Your schedule will start from following start_date, and run as per schedule_interval
        start_date=datetime(2022, 6, 1),
        schedule_interval=timedelta(seconds=60),
        #the scheduler creates a DAG run only for the latest interval
        catchup=False,
) as dag:

    # t1, t2 and t3 are examples of tasks created by instantiating operators
    task1 = BashOperator(
        task_id='print_date',
        bash_command='date'
    )

    task2 = BashOperator(
        task_id='print_text',
        depends_on_past=False,
        bash_command='echo HELLO',
        retries=3
    )

    def _my_func(**kwargs):
        print('current_datetime: {0}'.format(datetime.now() ))

    task3 = PythonOperator(
        task_id='python_task',
        python_callable=_my_func
    )
   
    task1 >> task2 >> task3
