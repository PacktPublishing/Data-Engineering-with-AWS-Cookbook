
import boto3
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup
from botocore.exceptions import ClientError
import time

# Initialize AWS Glue client
glue_client = boto3.client('glue', region_name='us-east-1')

# Function to start Glue crawler


def start_crawler(crawler_name):
    try:
        response = glue_client.start_crawler(Name=crawler_name)
        print(f"Started crawler: {crawler_name}")
    except ClientError as e:
        print(f"Error starting crawler: {e}")
        raise

# Function to check the status of Glue crawler


def check_crawler_status(crawler_name):
    while True:
        response = glue_client.get_crawler(Name=crawler_name)
        crawler_status = response['Crawler']['State']
        if crawler_status == 'READY':
            print(f"Crawler {crawler_name} has completed.")
            break
        elif crawler_status == 'RUNNING':
            print(f"Crawler {crawler_name} is still running...")
            time.sleep(60)  # Wait for 1 minute before checking again
        else:
            raise Exception(
                f"Crawler {crawler_name} encountered an error: {crawler_status}")

# Function to start Glue ETL job


def start_glue_job(job_name):
    try:
        response = glue_client.start_job_run(JobName=job_name)
        job_run_id = response['JobRunId']
        print(f"Started Glue job: {job_name} with JobRunId: {job_run_id}")
        return job_run_id
    except ClientError as e:
        print(f"Error starting Glue job: {e}")
        raise

# Function to check Glue job status


def check_glue_job_status(job_name, job_run_id):
    while True:
        response = glue_client.get_job_run(JobName=job_name, RunId=job_run_id)
        job_status = response['JobRun']['JobRunState']
        if job_status == 'SUCCEEDED':
            print(f"Glue job {job_name} succeeded.")
            break
        elif job_status in ['STARTING', 'RUNNING']:
            print(f"Glue job {job_name} is still {job_status}...")
            time.sleep(60)  # Wait for 1 minute before checking again
        else:
            raise Exception(
                f"Glue job {job_name} failed with status: {job_status}")


# Define the DAG
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1
}

with DAG(
    dag_id='glue_crawler_etl_workflow',
    default_args=default_args,
    description='A simple MWAA DAG to trigger Glue Crawler and ETL Job',
    schedule_interval=None,  # Manual trigger for this workshop
    catchup=False
) as dag:

    # Task 1: Start Glue Crawler
    start_crawler_task = PythonOperator(
        task_id='start_crawler',
        python_callable=start_crawler,
        op_kwargs={'crawler_name': 'csvToCatalogCrawler'}
    )

    # Task 2: Check Glue Crawler Status
    check_crawler_task = PythonOperator(
        task_id='check_crawler_status',
        python_callable=check_crawler_status,
        op_kwargs={'crawler_name': 'csvToCatalogCrawler'}
    )

    # Task 3: Start Glue ETL Job
    start_glue_job_task = PythonOperator(
        task_id='start_glue_job',
        python_callable=start_glue_job,
        op_kwargs={'job_name': 'CsvToParquetJob'}
    )

    # Task 4: Check Glue ETL Job Status
    check_glue_job_task = PythonOperator(
        task_id='check_glue_job_status',
        python_callable=check_glue_job_status,
        op_kwargs={
            'job_name': 'your_glue_job_name',
            'job_run_id': '{{ ti.xcom_pull(task_ids="CsvToParquetJob") }}'
        }
    )

    # Task dependencies: DAG Flow
    start_crawler_task >> check_crawler_task >> start_glue_job_task >> check_glue_job_task
